"""Sync source-selected items, reuse local originals, and track newsletter state."""

from __future__ import annotations

import argparse
import hashlib
import html
from html.parser import HTMLParser
import ipaddress
import json
from pathlib import Path
import re
import shutil
import sqlite3
import tempfile
import unicodedata
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import parse_qsl, unquote, urlencode, urljoin, urlsplit, urlunsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
import xml.etree.ElementTree as ET


DEFAULT_ROOT = Path("D:/newsletters")
FEEDS_TEMPLATE = """# One source URL per line. Lines beginning with # are ignored.
# Supported: RSS/Atom and Hugging Face Daily Papers pages or API URLs.
# Add feeds here before running sync. Examples:
# https://rss.arxiv.org/rss/cs.CL
# https://huggingface.co/blog/feed.xml
# https://huggingface.co/papers
"""
MAX_ISSUE_ITEMS = 20
ARXIV_ID = re.compile(r"^/(?:abs|pdf|html)/(\d{4}\.\d{4,5})(?:v\d+)?(?:\.pdf)?/?$", re.I)
TRACKING_KEYS = {"fbclid", "gclid", "mc_cid", "mc_eid"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def published_at(value: str) -> datetime | None:
    try:
        result = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        try:
            result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except (AttributeError, ValueError):
            return None
    return result.replace(tzinfo=timezone.utc) if result.tzinfo is None else result.astimezone(timezone.utc)


def one_year_cutoff(reference: datetime) -> datetime:
    try:
        return reference.replace(year=reference.year - 1)
    except ValueError:
        return reference.replace(year=reference.year - 1, day=28)


def safe_url(url: str) -> str:
    parts = urlsplit(url.strip())
    if parts.scheme not in {"http", "https"} or not parts.hostname:
        raise ValueError(f"Expected an HTTP(S) URL: {url}")
    host = parts.hostname.lower()
    if host == "localhost" or host.endswith(".local"):
        raise ValueError(f"Local URL not allowed: {url}")
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        address = None
    if address and not address.is_global:
        raise ValueError(f"Non-public address not allowed: {url}")
    return url.strip()


def canonical_url(url: str) -> str:
    parts = urlsplit(safe_url(url))
    host = parts.hostname.lower()
    match = ARXIV_ID.fullmatch(parts.path) if host == "arxiv.org" or host.endswith(".arxiv.org") else None
    if match:
        return f"https://arxiv.org/abs/{match.group(1)}"
    query = urlencode(sorted((k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
                             if not k.lower().startswith("utm_") and k.lower() not in TRACKING_KEYS))
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path or "/", query, ""))


class CheckedRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        safe_url(urljoin(req.full_url, newurl))
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url: str, limit: int) -> tuple[bytes, str, str]:
    request = Request(safe_url(url), headers={"User-Agent": "jskills-newsletter/1.0"})
    with build_opener(CheckedRedirect).open(request, timeout=30) as response:
        final_url = safe_url(response.geturl())
        media_type = response.headers.get_content_type()
        body = response.read(limit + 1)
    if len(body) > limit:
        raise ValueError(f"Response exceeds {limit} bytes: {url}")
    return body, media_type, final_url


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def child_text(node: ET.Element, *names: str) -> str:
    for name in names:
        for child in node:
            if local_name(child.tag) != name:
                continue
            value = "".join(child.itertext()).strip()
            if value:
                return html.unescape(value)
    return ""


def parse_feed(data: bytes, feed_url: str) -> list[dict[str, str]]:
    root = ET.fromstring(data)
    kind = local_name(root.tag)
    if kind not in {"rss", "RDF", "feed"}:
        raise ValueError(f"Not an RSS or Atom feed: {feed_url}")
    entries = []
    for node in root.iter():
        if local_name(node.tag) not in {"item", "entry"}:
            continue
        link = child_text(node, "link")
        if not link:
            for candidate in node:
                if local_name(candidate.tag) == "link" and candidate.attrib.get("rel", "alternate") == "alternate":
                    link = candidate.attrib.get("href", "")
                    if link:
                        break
        if not link:
            link = child_text(node, "id", "guid")
        if not link:
            continue
        url = urljoin(feed_url, link)
        try:
            safe_url(url)
        except ValueError:
            continue
        pdf_url = ""
        for candidate in node:
            if local_name(candidate.tag) in {"link", "enclosure"} and candidate.attrib.get("type") == "application/pdf":
                candidate_url = candidate.attrib.get("url") or candidate.attrib.get("href")
                if candidate_url:
                    pdf_url = urljoin(feed_url, candidate_url)
                    break
        entries.append({
            "url": url,
            "title": child_text(node, "title") or url,
            "published": child_text(node, "published", "pubDate", "updated", "date"),
            "feed_url": feed_url,
            "pdf_url": pdf_url,
        })
    return entries


def is_hf_daily(url: str) -> bool:
    parts = urlsplit(url)
    return parts.hostname in {"huggingface.co", "www.huggingface.co"} and (
        parts.path.rstrip("/") in {"/api/daily_papers", "/papers"}
        or re.fullmatch(r"/papers/date/\d{4}-\d{2}-\d{2}/?", parts.path) is not None)


class HFDailyPage(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.records = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        props = dict(attrs)
        if props.get("data-target") == "DailyPapers" and props.get("data-props"):
            data = json.loads(props["data-props"])
            if isinstance(data, dict):
                self.records = data.get("dailyPapers")


def parse_hf_daily(data: bytes, feed_url: str) -> list[dict[str, str]]:
    if data.lstrip().startswith(b"<"):
        page = HFDailyPage()
        page.feed(data.decode("utf-8-sig"))
        records = page.records
    else:
        records = json.loads(data)
        if isinstance(records, dict):
            records = records.get("dailyPapers", records.get("papers"))
    if not isinstance(records, list):
        raise ValueError(f"Unexpected Hugging Face Daily Papers schema: {feed_url}")
    entries = []
    for record in records:
        if not isinstance(record, dict) or not isinstance(record.get("paper"), dict):
            raise ValueError(f"Invalid Hugging Face paper record: {feed_url}")
        paper = record.get("paper", {})
        paper_id = paper.get("id", "")
        if not isinstance(paper_id, str) or not re.fullmatch(r"\d{4}\.\d{4,5}", paper_id):
            raise ValueError(f"Invalid Hugging Face paper ID: {paper_id!r}")
        entries.append({
            "url": f"https://arxiv.org/abs/{paper_id}",
            "title": paper.get("title") or record.get("title") or paper_id,
            "published": paper.get("publishedAt", ""),
            "featured_at": record.get("publishedAt", ""),
            "summary": paper.get("summary", ""),
            "feed_url": feed_url,
            "pdf_url": "",
        })
    return entries


def source_url_for_date(url: str, date: str | None) -> str:
    if not date or not is_hf_daily(url):
        return url
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query))
    if parts.path.rstrip("/") == "/api/daily_papers":
        query["date"] = date
        path = parts.path
    else:
        query.pop("date", None)
        path = f"/papers/date/{date}"
    return urlunsplit((parts.scheme, parts.netloc, path, urlencode(query), ""))


def source_entries(url: str, date: str | None) -> list[dict[str, str]]:
    request_url = source_url_for_date(url, date)
    data, _, final_url = fetch(request_url, 8 * 1024 * 1024)
    if is_hf_daily(url) or is_hf_daily(final_url):
        entries = parse_hf_daily(data, request_url)
        # A dated API and the public edition page can disagree; check the page
        # rather than interpreting an empty API response as a verified empty edition.
        if not entries and date and urlsplit(request_url).path.rstrip("/") == "/api/daily_papers":
            page_url = f"https://huggingface.co/papers/date/{date}"
            page, _, _ = fetch(page_url, 8 * 1024 * 1024)
            entries = parse_hf_daily(page, page_url)
        return entries
    try:
        return parse_feed(data, final_url)
    except (ET.ParseError, ValueError) as exc:
        raise ValueError(f"Unsupported or malformed source: {url}. Expected RSS/Atom or a supported Daily Papers URL") from exc


class TextExtractor(HTMLParser):
    BLOCKS = {"article", "blockquote", "br", "div", "h1", "h2", "h3", "h4", "li", "p", "section"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.ignored: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript"}:
            self.ignored = tag
        elif not self.ignored and tag in self.BLOCKS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag == self.ignored:
            self.ignored = None
        elif not self.ignored and tag in self.BLOCKS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.ignored:
            self.parts.append(data)

    def text(self) -> str:
        lines = [" ".join(line.split()) for line in "".join(self.parts).splitlines()]
        return "\n".join(line for line in lines if line)


def initialize(root: Path) -> sqlite3.Connection:
    root.mkdir(parents=True, exist_ok=True)
    (root / "materials").mkdir(exist_ok=True)
    (root / "issues").mkdir(exist_ok=True)
    feeds = root / "feeds.txt"
    if not feeds.exists():
        feeds.write_text(FEEDS_TEMPLATE, encoding="utf-8")
    db = sqlite3.connect(root / "state.sqlite", timeout=15)
    db.row_factory = sqlite3.Row
    db.execute("""CREATE TABLE IF NOT EXISTS items (
        id TEXT PRIMARY KEY, canonical_url TEXT UNIQUE NOT NULL, source_url TEXT NOT NULL,
        title TEXT NOT NULL, feed_url TEXT, published TEXT, archived_at TEXT NOT NULL,
        archive_dir TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'pending',
        decision TEXT, processed_at TEXT, issue_path TEXT
    )""")
    db.execute("CREATE TABLE IF NOT EXISTS current_items (id TEXT PRIMARY KEY)")
    db.commit()
    return db


def material_id(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:20]


def cache_index(root: Path) -> dict[str, Path]:
    index = {}
    for path in (root / "materials").glob("*/metadata.json"):
        if not path.resolve().is_relative_to((root / "materials").resolve()):
            continue
        try:
            metadata = json.loads(path.read_text(encoding="utf-8"))
            for key in ("canonical_url", "url"):
                if metadata.get(key):
                    index[canonical_url(metadata[key])] = path.parent
        except (OSError, ValueError, AttributeError, TypeError):
            continue
    return index


def paper_url(canonical: str, item: dict[str, str]) -> str:
    if canonical.startswith("https://arxiv.org/abs/"):
        return f"https://arxiv.org/pdf/{canonical.rsplit('/', 1)[-1]}"
    return item.get("pdf_url", "")


def reuse_cached(destination: Path, item: dict[str, str]) -> tuple[str, str, bool]:
    metadata = json.loads((destination / "metadata.json").read_text(encoding="utf-8"))
    try:
        canonical = canonical_url(metadata["canonical_url"])
        media_type = metadata["content_type"]
        archived_at = metadata["archived_at"]
    except (KeyError, TypeError) as exc:
        raise ValueError(f"Invalid cache metadata: {destination}") from exc
    source_names = {"application/pdf": "source.pdf", "text/html": "source.html",
                    "application/xhtml+xml": "source.html", "text/plain": "source.txt"}
    source_name = metadata.get("source_name") or source_names.get(media_type)
    if source_name is None and (destination / "source.pdf").is_file():
        source_name = "source.pdf"
    if source_name not in {"source.pdf", "source.html", "source.txt"}:
        raise ValueError(f"Unsupported cached content type: {destination}")
    source = destination / source_name
    is_pdf = source_name == "source.pdf"
    downloaded = False
    if not source.is_file():
        body, fetched_type, _ = fetch(canonical, 64 * 1024 * 1024)
        fetched_name = "source.pdf" if body.startswith(b"%PDF-") else source_names.get(fetched_type)
        if fetched_name != source.name:
            raise ValueError(f"Cached source content type changed: {canonical}")
        if source.suffix == ".pdf" and not body.startswith(b"%PDF-"):
            raise ValueError(f"PDF unavailable: {canonical}")
        source.write_bytes(body)
        downloaded = True
    if not source.stat().st_size:
        raise ValueError(f"Empty cached source: {source}")
    pdf_url = paper_url(canonical, item) or metadata.get("pdf_url", "")
    pdf = source if is_pdf else destination / "paper.pdf"
    if pdf_url and not is_pdf and not pdf.is_file():
        body, _, _ = fetch(pdf_url, 64 * 1024 * 1024)
        if not body.startswith(b"%PDF-"):
            raise ValueError(f"PDF unavailable: {pdf_url}")
        pdf.write_bytes(body)
        downloaded = True
    if is_pdf or pdf_url:
        with pdf.open("rb") as handle:
            if handle.read(5) != b"%PDF-":
                raise ValueError(f"Invalid cached PDF: {pdf}")
    return canonical, archived_at, downloaded


def select_item(db: sqlite3.Connection, item_id: str) -> None:
    with db:
        db.execute("INSERT OR IGNORE INTO current_items (id) VALUES (?)", (item_id,))


def record_archive(db: sqlite3.Connection, item: dict[str, str], requested: str,
                   canonical: str, destination: Path, archived_at: str,
                   downloaded: bool) -> dict[str, str | bool]:
    item_id = material_id(canonical)
    with db:
        db.execute("""INSERT INTO items
            (id, canonical_url, source_url, title, feed_url, published, archived_at, archive_dir)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (
            item_id, canonical, requested, item["title"], item.get("feed_url", ""),
            item.get("published", ""), archived_at, str(destination)))
        db.execute("INSERT OR IGNORE INTO current_items (id) VALUES (?)", (item_id,))
    return {"id": item_id, "title": item["title"], "url": canonical,
            "archive_dir": str(destination), "downloaded": downloaded}


def archive(db: sqlite3.Connection, root: Path, item: dict[str, str],
            cache: dict[str, Path] | None = None) -> dict[str, str | bool] | None:
    requested = canonical_url(item["url"])
    existing = db.execute("SELECT id FROM items WHERE canonical_url = ? OR source_url = ?",
                          (requested, requested)).fetchone()
    if existing:
        select_item(db, existing["id"])
        return None
    if cache is None:
        cache = cache_index(root)
    destination = cache.get(requested)
    if destination:
        canonical, archived_at, downloaded = reuse_cached(destination, item)
        existing = db.execute("SELECT id FROM items WHERE canonical_url = ?", (canonical,)).fetchone()
        if existing:
            select_item(db, existing["id"])
            return None
        return record_archive(db, item, requested, canonical, destination, archived_at, downloaded)
    destination = root / "materials" / material_id(requested)
    if destination.exists():
        raise ValueError(f"Cache metadata missing or invalid: {destination}")
    body, media_type, final_url = fetch(requested, 64 * 1024 * 1024)
    canonical = canonical_url(final_url)
    existing = db.execute("SELECT id FROM items WHERE canonical_url = ?", (canonical,)).fetchone()
    if existing:
        select_item(db, existing["id"])
        return None
    if canonical in cache:
        destination = cache[canonical]
        canonical, archived_at, _ = reuse_cached(destination, item)
        cache[requested] = destination
        return record_archive(db, item, requested, canonical, destination, archived_at, True)
    is_pdf = body.startswith(b"%PDF-") or media_type == "application/pdf"
    if not is_pdf and media_type not in {"text/html", "application/xhtml+xml", "text/plain"}:
        raise ValueError(f"Unsupported content type {media_type}: {canonical}")
    paper_pdf = None
    pdf_url = paper_url(canonical, item)
    if pdf_url and not is_pdf:
        paper_pdf, _, _ = fetch(pdf_url, 64 * 1024 * 1024)
        if not paper_pdf.startswith(b"%PDF-"):
            raise ValueError(f"PDF unavailable: {pdf_url}")
    item_id = material_id(canonical)
    destination = root / "materials" / item_id
    if destination.exists():
        raise FileExistsError(f"Archive directory exists without database record: {destination}")
    staging = Path(tempfile.mkdtemp(prefix=".staging-", dir=root / "materials")).resolve()
    if not staging.is_relative_to((root / "materials").resolve()):
        raise ValueError("Staging directory escaped data root")
    try:
        source_name = "source.pdf" if is_pdf else "source.html" if media_type != "text/plain" else "source.txt"
        (staging / source_name).write_bytes(body)
        if paper_pdf:
            (staging / "paper.pdf").write_bytes(paper_pdf)
        if source_name == "source.html":
            extractor = TextExtractor()
            extractor.feed(body.decode("utf-8", errors="replace"))
            (staging / "readable.txt").write_text(extractor.text(), encoding="utf-8")
        metadata = {**item, "canonical_url": canonical, "archived_at": now(),
                    "content_type": media_type, "source_name": source_name}
        (staging / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
        staging.rename(destination)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    cache[requested] = cache[canonical] = destination
    return record_archive(db, item, requested, canonical, destination, metadata["archived_at"], True)


def read_feeds(root: Path) -> list[str]:
    lines = (root / "feeds.txt").read_text(encoding="utf-8").splitlines()
    return [safe_url(line) for line in lines if line.strip() and not line.lstrip().startswith("#")]


def heading_fragment(title: str) -> str:
    # Newsletter headings are plain text; keep Unicode letters, marks, and numbers.
    return "".join(char for char in title.strip().lower()
                   if char in " -_" or unicodedata.category(char)[0] in "LMN").replace(" ", "-")


def check_issue(db: sqlite3.Connection, root: Path, issue: Path) -> list[str]:
    issue = issue.resolve()
    if not issue.is_file() or not issue.is_relative_to((root / "issues").resolve()):
        raise ValueError("Issue must be an existing Markdown file inside the issues directory")
    if issue.suffix.lower() != ".md":
        raise ValueError("Issue must be Markdown")
    text = issue.read_text(encoding="utf-8-sig")
    # Ignore fenced examples when inspecting actual headings and citations.
    text = re.sub(r"(?ms)^ {0,3}(`{3,}|~{3,})[^\n]*\n.*?^ {0,3}\1[ \t]*$", "", text)
    sections = list(re.finditer(r"(?m)^## [^\n]+$", text))
    articles = list(re.finditer(r"(?m)^### ([^\n]+)$", text))
    if len(sections) != 2 or not articles or any(h.start() < sections[1].end() for h in articles):
        raise ValueError("Expected two H2 sections: theme overview, then H3 individual summaries")
    if len(articles) > MAX_ISSUE_ITEMS:
        raise ValueError(f"An issue may contain at most {MAX_ISSUE_ITEMS} articles; found {len(articles)}")
    if re.search(r"(?m)^#{4,6} ", text):
        raise ValueError("Do not add lower-level headings inside summaries")
    fragments = [heading_fragment(re.sub(r"[ \t]+#+[ \t]*$", "", heading.group(1)))
                 for heading in re.finditer(r"(?m)^#{1,3} ([^\n]+)$", text)]
    if not all(fragments) or len(set(fragments)) != len(fragments):
        raise ValueError("Use unique, nonempty plain-text headings for predictable Markdown links")
    article_fragments = {heading_fragment(re.sub(r"[ \t]+#+[ \t]*$", "", article.group(1)))
                         for article in articles}
    links = re.compile(r"\[[^\]\n]+\]\((?:<([^>]+)>|([^\s)]+))\)")

    def targets(value: str) -> list[str]:
        return [a or b for a, b in links.findall(value)]

    overview = text[sections[0].end():sections[1].start()]
    citations = {unquote(link[1:]) for link in targets(overview) if link.startswith("#")}
    if citations != article_fragments:
        raise ValueError("Overview must cite every summary and only summaries in this issue; expected targets: "
                         + ", ".join("#" + fragment for fragment in sorted(article_fragments)))
    all_targets = targets(text)
    if any(link.startswith("#") and unquote(link[1:]) not in fragments for link in all_targets):
        raise ValueError("Broken internal article citation")
    ids = []
    for index, article in enumerate(articles):
        end = articles[index + 1].start() if index + 1 < len(articles) else len(text)
        body = text[article.end():end]
        if re.search(r"(?m)^ {0,3}>", body):
            raise ValueError("Write individual summaries as ordinary paragraphs, not blockquotes")
        if not re.search(r"[\u3400-\u4dbf\u4e00-\u9fff]", links.sub("", body)):
            raise ValueError("Each individual summary needs Chinese prose; translate non-Chinese abstracts")
        summary_links = targets(body)
        local_links = [unquote(urlsplit(link).path) for link in summary_links if link.startswith("../materials/")]
        local_ids = {match.group(1) for link in local_links
                     if (match := re.fullmatch(r"\.\./materials/([a-f0-9]{20})/[^/]+", link))}
        if len(local_ids) != 1:
            raise ValueError("Each summary needs a local archive link to exactly one material")
        item_id = local_ids.pop()
        if item_id in ids:
            raise ValueError("Duplicate article in issue")
        row = db.execute("SELECT canonical_url, source_url, archive_dir FROM items WHERE id = ?", (item_id,)).fetchone()
        if row is None:
            raise ValueError(f"Unknown material: {item_id}")
        original = {row["canonical_url"], row["source_url"]}
        if not any(link in original for link in summary_links):
            raise ValueError(f"Missing original URL in summary: {item_id}")
        archive_dir = Path(row["archive_dir"]).resolve()
        local = [(issue.parent / link).resolve() for link in local_links]
        if not any(path.parent == archive_dir and path.is_file() and path.suffix.lower() in {".pdf", ".html", ".txt"}
                   for path in local):
            raise ValueError(f"Missing or broken local archive link in summary: {item_id}")
        ids.append(item_id)
    return ids


def emit(value: object) -> None:
    print(json.dumps(value, ensure_ascii=False))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    sync = sub.add_parser("sync")
    sync.add_argument("--date", help="Hugging Face Daily Papers date (YYYY-MM-DD)")
    sub.add_parser("pending")
    sub.add_parser("processed")
    add = sub.add_parser("add", help="Archive one direct article or paper URL")
    add.add_argument("url")
    check = sub.add_parser("check", help="Check issue size, heading links, and source links (not factual accuracy)")
    check.add_argument("issue", type=Path)
    mark = sub.add_parser("mark", help="Mark items covered in a newsletter as used")
    mark.add_argument("decision", choices=("used",))
    mark.add_argument("ids", nargs="+")
    mark.add_argument("--issue", type=Path)
    args = parser.parse_args()
    root = args.root.expanduser().resolve()
    db = initialize(root)
    try:
        if args.command == "init":
            emit({"root": str(root), "feeds": str(root / "feeds.txt")})
        elif args.command == "sync":
            if args.date:
                try:
                    datetime.strptime(args.date, "%Y-%m-%d")
                except ValueError:
                    parser.error("--date must be YYYY-MM-DD")
            feeds = read_feeds(root)
            with db:
                db.execute("DELETE FROM current_items")
            if not feeds:
                emit({"new": 0, "errors": [], "note": f"Add RSS or Atom URLs to {root / 'feeds.txt'}"})
                return 0
            count, downloaded, reused, old, undated, future, errors = 0, 0, 0, 0, 0, 0, []
            cache = cache_index(root)
            reference = datetime.now(timezone.utc)
            cutoff = one_year_cutoff(reference)
            for feed_url in feeds:
                try:
                    entries = source_entries(feed_url, args.date)
                except Exception as exc:
                    errors.append(f"{feed_url}: {exc}")
                    continue
                for item in entries:
                    published = published_at(item["published"])
                    if published is None:
                        undated += 1
                        continue
                    if published < cutoff:
                        old += 1
                        continue
                    if published > reference:
                        future += 1
                        continue
                    try:
                        saved = archive(db, root, item, cache)
                        if saved:
                            emit(saved)
                            count += 1
                            downloaded += int(saved["downloaded"])
                            reused += int(not saved["downloaded"])
                    except Exception as exc:
                        errors.append(f"{item['url']}: {exc}")
            emit({"new": count, "downloaded": downloaded, "reused": reused,
                  "skipped_old": old, "skipped_undated": undated, "skipped_future": future, "errors": errors})
            return 1 if errors else 0
        elif args.command == "add":
            saved = archive(db, root, {"url": args.url, "title": args.url, "published": "", "feed_url": ""})
            emit(saved or {"already_archived": canonical_url(args.url)})
        elif args.command == "pending":
            rows = db.execute("""SELECT id, title, canonical_url, published, archive_dir
                FROM items WHERE status = 'pending' AND id IN (SELECT id FROM current_items)
                ORDER BY archived_at, id""").fetchall()
            for row in rows:
                emit(dict(row))
        elif args.command == "processed":
            rows = db.execute("""SELECT id, title, canonical_url, archive_dir, decision, processed_at, issue_path
                FROM items WHERE status = 'done' ORDER BY processed_at DESC, id""").fetchall()
            for row in rows:
                emit(dict(row))
        elif args.command == "check":
            emit({"articles": check_issue(db, root, args.issue), "issue": str(args.issue.resolve())})
        elif args.command == "mark":
            if not args.issue:
                parser.error("--issue is required for used items")
            issue = args.issue.resolve()
            ids = check_issue(db, root, issue)
            if len(set(args.ids)) != len(args.ids) or not set(args.ids).issubset(ids):
                raise ValueError("Mark only unique article IDs present in this issue")
            with db:
                for item_id in args.ids:
                    changed = db.execute("""UPDATE items SET status = 'done', decision = ?,
                        processed_at = ?, issue_path = ? WHERE id = ? AND status = 'pending'""",
                        (args.decision, now(), str(issue), item_id)).rowcount
                    if not changed:
                        raise ValueError(f"Unknown or already processed item: {item_id}")
            emit({"marked": len(args.ids), "decision": args.decision})
        return 0
    finally:
        db.close()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, ET.ParseError) as exc:
        raise SystemExit(str(exc)) from exc
