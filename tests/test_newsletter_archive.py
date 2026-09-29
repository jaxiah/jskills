import contextlib
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock
from urllib.request import Request


SCRIPT = Path(__file__).resolve().parents[1] / "newsletter" / "scripts" / "archive.py"
SPEC = importlib.util.spec_from_file_location("newsletter_archive", SCRIPT)
archive = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(archive)


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = archive.initialize(self.root)

    def tearDown(self):
        self.db.close()
        self.temp.cleanup()

    def issue(self, saved_items, name="newsletter.md"):
        overview = "Related work " + " ".join(f"[{i}](#{i}-article)" for i, item in enumerate(saved_items, 1))
        summaries = []
        for i, item in enumerate(saved_items, 1):
            summaries.append(f'''### {i}. Article

\u6587\u7ae0\u8bf4\u660e\u4e86\u95ee\u9898\u548c\u65b9\u6cd5. A self-contained description of the problem and the reported method.

[Original]({item['url']}) [Archive](../materials/{item['id']}/source.html)
''')
        issue = self.root / "issues" / name
        issue.write_text("# Newsletter\n\n## Theme Overview\n\n" + overview + "\n\n## Individual Summaries\n\n"
                         + "\n".join(summaries), encoding="utf-8")
        return issue

    def articles(self, count):
        def fetch(url, limit):
            return b"<html><body>Article</body></html>", "text/html", url
        with mock.patch.object(archive, "fetch", side_effect=fetch):
            return [archive.archive(self.db, self.root, {"url": f"https://example.org/{i}", "title": f"Article {i}"})
                    for i in range(count)]

    def test_rss_and_atom_duplicate_is_archived_once(self):
        rss = b"""<rss><channel><item><title>Example</title>
            <link>https://example.org/article?utm_source=feed</link>
            <pubDate>Mon, 21 Sep 2026 00:00:00 GMT</pubDate>
            </item></channel></rss>"""
        atom = b"""<feed xmlns="http://www.w3.org/2005/Atom"><entry>
            <title>Example again</title><link href="https://example.org/article" />
            </entry></feed>"""
        items = archive.parse_feed(rss, "https://example.org/rss")
        items += archive.parse_feed(atom, "https://example.org/atom")
        page = b"<html><body><article><h1>Example</h1><p>Full article text.</p></article></body></html>"
        with mock.patch.object(archive, "fetch", return_value=(page, "text/html", "https://example.org/article")) as fetch:
            saved = archive.archive(self.db, self.root, items[0])
            self.assertIsNone(archive.archive(self.db, self.root, items[1]))
            fetch.assert_called_once()
        folder = Path(saved["archive_dir"])
        self.assertEqual((folder / "source.html").read_bytes(), page)
        self.assertIn("Full article text.", (folder / "readable.txt").read_text(encoding="utf-8"))
        self.assertEqual(self.db.execute("SELECT count(*) FROM items").fetchone()[0], 1)

    def test_arxiv_versions_share_key_and_archive_pdf(self):
        url = "https://rss.arxiv.org/abs/2609.29421v2"
        page = b"<html><body>Abstract</body></html>"
        pdf = b"%PDF-1.7\nexample"
        def fetch(url, limit):
            if url.endswith("/pdf/2609.29421"):
                return pdf, "application/pdf", url
            return page, "text/html", url
        with mock.patch.object(archive, "fetch", side_effect=fetch):
            saved = archive.archive(self.db, self.root, {"url": url, "title": "Paper"})
        self.assertEqual(saved["url"], "https://arxiv.org/abs/2609.29421")
        self.assertEqual((Path(saved["archive_dir"]) / "paper.pdf").read_bytes(), pdf)
        self.assertIsNone(archive.archive(self.db, self.root, {"url": "https://arxiv.org/pdf/2609.29421v3", "title": "Paper"}))

    def test_failed_archive_is_not_marked_seen(self):
        with mock.patch.object(archive, "fetch", side_effect=OSError("offline")):
            with self.assertRaises(OSError):
                archive.archive(self.db, self.root, {"url": "https://example.org/missing", "title": "Missing"})
        self.assertEqual(self.db.execute("SELECT count(*) FROM items").fetchone()[0], 0)

    def test_redirected_feed_link_is_skipped_before_download(self):
        item = {"url": "http://example.org/a?utm_source=feed", "title": "A"}
        page = b"<html><body>Article</body></html>"
        with mock.patch.object(archive, "fetch", return_value=(page, "text/html", "https://example.org/a")) as fetch:
            self.assertIsNotNone(archive.archive(self.db, self.root, item))
            self.assertIsNone(archive.archive(self.db, self.root, item))
            fetch.assert_called_once()

    def test_sync_only_archives_unseen_items_within_one_year(self):
        feed_url = "https://example.org/feed"
        cutoff = archive.one_year_cutoff(datetime.now(timezone.utc))
        recent = format_datetime(datetime.now(timezone.utc))
        old = format_datetime(cutoff - timedelta(days=1))
        feed = f"""<rss><channel>
            <item><title>Recent</title><link>https://example.org/recent</link><pubDate>{recent}</pubDate></item>
            <item><title>Old</title><link>https://example.org/old</link><pubDate>{old}</pubDate></item>
            <item><title>Future</title><link>https://example.org/future</link><pubDate>{format_datetime(datetime.now(timezone.utc) + timedelta(days=1))}</pubDate></item>
            <item><title>Undated</title><link>https://example.org/undated</link></item>
            </channel></rss>""".encode()
        (self.root / "feeds.txt").write_text(feed_url + "\n", encoding="utf-8")
        requests = []

        def fetch(url, limit):
            requests.append(url)
            if url == feed_url:
                return feed, "application/rss+xml", url
            return b"<html><body>Recent content</body></html>", "text/html", url

        argv = ["archive.py", "--root", str(self.root), "sync"]
        output = io.StringIO()
        with mock.patch.object(archive, "fetch", side_effect=fetch), mock.patch.object(sys, "argv", argv):
            with contextlib.redirect_stdout(output):
                self.assertEqual(archive.main(), 0)
                self.assertEqual(archive.main(), 0)
        self.assertEqual(requests.count("https://example.org/recent"), 1)
        self.assertNotIn("https://example.org/old", requests)
        self.assertNotIn("https://example.org/undated", requests)
        self.assertNotIn("https://example.org/future", requests)
        self.assertEqual(self.db.execute("SELECT count(*) FROM items").fetchone()[0], 1)
        self.assertIn('"skipped_old": 1', output.getvalue())
        self.assertIn('"skipped_undated": 1', output.getvalue())
        self.assertIn('"skipped_future": 1', output.getvalue())

    def test_one_year_cutoff_handles_leap_day(self):
        reference = datetime(2024, 2, 29, 12, 30, tzinfo=timezone.utc)
        self.assertEqual(archive.one_year_cutoff(reference), datetime(2023, 2, 28, 12, 30, tzinfo=timezone.utc))
        self.assertEqual(archive.one_year_cutoff(datetime(2026, 9, 28, tzinfo=timezone.utc)),
                         datetime(2025, 9, 28, tzinfo=timezone.utc))

    def test_atom_prefers_original_published_date_over_updated(self):
        data = b'''<feed xmlns="http://www.w3.org/2005/Atom"><entry>
            <title>A</title><link href="https://example.org/a"/>
            <updated>2026-09-28T00:00:00Z</updated><published>2024-09-28T00:00:00Z</published>
            </entry></feed>'''
        self.assertEqual(archive.parse_feed(data, "https://example.org/feed")[0]["published"], "2024-09-28T00:00:00Z")

    def test_feed_pdf_enclosure_is_preserved(self):
        feed = b"""<rss><channel><item><title>Paper</title>
            <link>https://example.org/paper</link>
            <enclosure url="https://example.org/paper.pdf" type="application/pdf" />
            </item></channel></rss>"""
        item = archive.parse_feed(feed, "https://example.org/feed")[0]

        def fetch(url, limit):
            if url.endswith(".pdf"):
                return b"%PDF-1.7\nfull paper", "application/pdf", url
            return b"<html><body>Abstract</body></html>", "text/html", url

        with mock.patch.object(archive, "fetch", side_effect=fetch):
            saved = archive.archive(self.db, self.root, item)
        self.assertEqual((Path(saved["archive_dir"]) / "paper.pdf").read_bytes(), b"%PDF-1.7\nfull paper")

    def test_hf_daily_papers_use_original_publication_date(self):
        source = "https://huggingface.co/api/daily_papers?limit=100"
        records = [{
            "publishedAt": "2026-09-24T20:00:00.000Z",
            "paper": {"id": "2609.28654", "title": "Object Permanence", "publishedAt": "2026-09-23T00:00:00.000Z"},
        }]
        entries = archive.parse_hf_daily(json.dumps(records).encode(), source)
        self.assertEqual(entries[0]["url"], "https://arxiv.org/abs/2609.28654")
        self.assertEqual(entries[0]["published"], "2026-09-23T00:00:00.000Z")
        self.assertEqual(entries[0]["featured_at"], "2026-09-24T20:00:00.000Z")
        self.assertEqual(archive.source_url_for_date(source, "2026-09-25"),
                         source + "&date=2026-09-25")

    def test_hf_daily_json_preserves_metadata(self):
        source = "https://huggingface.co/api/daily_papers?limit=100"
        records = [{"publishedAt": "2026-09-25T00:00:00Z", "paper": {
            "id": "2609.28654", "title": 'A "quoted" title & evidence',
            "publishedAt": "2026-09-23T00:00:00Z", "summary": "Author abstract"}}]
        expected = archive.parse_hf_daily(json.dumps(records).encode(), source)
        self.assertEqual(expected[0]["title"], records[0]["paper"]["title"])
        self.assertEqual(expected[0]["summary"], "Author abstract")
        for wrapper in ("papers", "dailyPapers"):
            self.assertEqual(archive.parse_hf_daily(json.dumps({wrapper: records}).encode(), source), expected)

    def test_hf_daily_url_matching_is_api_only(self):
        for url in ("https://huggingface.co/api/daily_papers?limit=100",
                    "https://huggingface.co/api/daily_papers/", "https://www.huggingface.co/api/daily_papers"):
            with self.subTest(url=url):
                self.assertTrue(archive.is_hf_daily(url))
        for url in ("https://huggingface.co/papers", "https://huggingface.co/papers/",
                    "https://huggingface.co/papers/date/2026-09-25",
                    "https://huggingface.co/papers/2609.28654", "https://example.org/api/daily_papers"):
            with self.subTest(url=url):
                self.assertFalse(archive.is_hf_daily(url))
                self.assertEqual(archive.source_url_for_date(url, "2026-09-25"), url)
        source = "https://huggingface.co/api/daily_papers?date=2026-09-24&limit=100"
        self.assertEqual(archive.source_url_for_date(source, "2026-09-25"),
                         "https://huggingface.co/api/daily_papers?date=2026-09-25&limit=100")

    def test_empty_dated_api_does_not_fall_back_to_a_webpage(self):
        source = "https://huggingface.co/api/daily_papers?limit=100"
        with mock.patch.object(archive, "fetch", return_value=(b"[]", "application/json", source)) as fetch:
            self.assertEqual(archive.source_entries(source, "2026-09-25"), [])
        fetch.assert_called_once_with(source + "&date=2026-09-25", 8 * 1024 * 1024)

    def test_api_html_response_is_an_error_without_fallback(self):
        source = "https://huggingface.co/api/daily_papers"
        with mock.patch.object(archive, "fetch", return_value=(b"<html>Unavailable</html>", "text/html", source)) as fetch:
            with self.assertRaisesRegex(ValueError, "Expected JSON"):
                archive.source_entries(source, None)
        fetch.assert_called_once_with(source, 8 * 1024 * 1024)

    def test_api_network_error_is_not_replaced_by_scraping(self):
        source = "https://huggingface.co/api/daily_papers"
        with mock.patch.object(archive, "fetch", side_effect=OSError("offline")) as fetch:
            with self.assertRaisesRegex(OSError, "offline"):
                archive.source_entries(source, None)
        fetch.assert_called_once_with(source, 8 * 1024 * 1024)

    def test_source_schema_changes_are_errors_not_empty_feeds(self):
        for data in (b"{}", b"[null]", b'[{"paper": {"id": "not-an-id"}}]', b"<html>Changed layout</html>"):
            with self.subTest(data=data), self.assertRaises(ValueError):
                archive.parse_hf_daily(data, "https://huggingface.co/api/daily_papers")

    def test_webpages_and_unadapted_json_apis_require_agent_handling(self):
        for source, data, media_type in (
            ("https://example.org/index", b"<html>Blog index</html>", "text/html"),
            ("https://huggingface.co/papers", b'<div data-target="DailyPapers" data-props=\'{"dailyPapers": []}\'></div>', "text/html"),
            ("https://example.org/api/articles", b'[{"url": "https://example.org/article"}]', "application/json"),
        ):
            with self.subTest(source=source), mock.patch.object(archive, "fetch", return_value=(data, media_type, source)) as fetch:
                with self.assertRaisesRegex(ValueError, "Ordinary webpages require agent-led handling"):
                    archive.source_entries(source, None)
                fetch.assert_called_once_with(source, 8 * 1024 * 1024)

    def test_sync_handles_mixed_rss_and_hf_api_sources(self):
        rss_url = "https://example.org/feed"
        hf_url = "https://huggingface.co/api/daily_papers?limit=100"
        published = datetime.now(timezone.utc).isoformat()
        rss = f'<rss><channel><item><title>Blog</title><link>https://example.org/blog</link><pubDate>{published}</pubDate></item></channel></rss>'.encode()
        hf = json.dumps([{"paper": {"id": "2609.28654", "title": "Paper", "publishedAt": published}}]).encode()
        (self.root / "feeds.txt").write_text(rss_url + "\n" + hf_url + "\n", encoding="utf-8")

        def fetch(url, limit):
            if url == rss_url:
                return rss, "application/rss+xml", url
            if url == hf_url:
                return hf, "application/json", url
            if "/pdf/" in url:
                return b"%PDF-1.7\noriginal", "application/pdf", url
            return b"<html><body>Original</body></html>", "text/html", url

        with mock.patch.object(archive, "fetch", side_effect=fetch), contextlib.redirect_stdout(io.StringIO()):
            with mock.patch.object(sys, "argv", ["archive.py", "--root", str(self.root), "sync"]):
                self.assertEqual(archive.main(), 0)
        self.assertEqual(self.db.execute("SELECT count(*) FROM current_items").fetchone()[0], 2)

    def test_sync_reports_webpage_gap_and_keeps_valid_feed_items(self):
        page_url = "https://example.org/index"
        feed_url = "https://example.org/feed"
        published = format_datetime(datetime.now(timezone.utc))
        feed = f'<rss><channel><item><title>Article</title><link>https://example.org/article</link><pubDate>{published}</pubDate></item></channel></rss>'.encode()
        (self.root / "feeds.txt").write_text(page_url + "\n" + feed_url + "\n", encoding="utf-8")

        def fetch(url, limit):
            if url == feed_url:
                return feed, "application/rss+xml", url
            return b"<html><body>Original</body></html>", "text/html", url

        output = io.StringIO()
        with mock.patch.object(archive, "fetch", side_effect=fetch), contextlib.redirect_stdout(output):
            with mock.patch.object(sys, "argv", ["archive.py", "--root", str(self.root), "sync"]):
                self.assertEqual(archive.main(), 1)
        result = json.loads(output.getvalue().splitlines()[-1])
        self.assertEqual(result["new"], 1)
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn(page_url, result["errors"][0])
        self.assertIn("agent-led handling", result["errors"][0])
        self.assertEqual(self.db.execute("SELECT count(*) FROM current_items").fetchone()[0], 1)

    def test_issue_check_accepts_20_articles_and_rejects_21(self):
        items = self.articles(21)
        self.assertEqual(archive.check_issue(self.db, self.root, self.issue(items[:20])), [item["id"] for item in items[:20]])
        with self.assertRaisesRegex(ValueError, "at most 20"):
            archive.check_issue(self.db, self.root, self.issue(items))

    def test_issue_check_rejects_duplicate_articles_and_missing_citations(self):
        items = self.articles(2)
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            archive.check_issue(self.db, self.root, self.issue([items[0], items[0]]))
        issue = self.issue(items)
        issue.write_text(issue.read_text(encoding="utf-8").replace("[2](#2-article)", ""), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "cite every summary"):
            archive.check_issue(self.db, self.root, issue)

    def test_issue_check_rejects_broken_original_and_local_links(self):
        items = self.articles(1)
        for old, new, error in ((items[0]["url"], "https://example.org/wrong", "original URL"),
                                ("source.html", "missing.html", "local archive link"),
                                (items[0]["id"], "0" * 20, "Unknown material")):
            issue = self.issue(items)
            issue.write_text(issue.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")
            with self.subTest(error=error), self.assertRaisesRegex(ValueError, error):
                archive.check_issue(self.db, self.root, issue)

    def test_heading_fragments_keep_chinese_and_remove_punctuation(self):
        for title, fragment in (("1. BudgetKV: KV Cache", "1-budgetkv-kv-cache"),
                                ("2. KV Cache: \u4fdd\u7559\u7b56\u7565", "2-kv-cache-\u4fdd\u7559\u7b56\u7565"),
                                ("3. Long-context / model_v2", "3-long-context--model_v2"),
                                ("4. Cafe\u0301", "4-cafe\u0301")):
            with self.subTest(title=title):
                self.assertEqual(archive.heading_fragment(title), fragment)

    def test_issue_check_accepts_heading_links_without_html_anchors(self):
        items = self.articles(1)
        issue = self.issue(items)
        text = issue.read_text(encoding="utf-8").replace("1. Article", "1. KV Cache: \u4fdd\u7559\u7b56\u7565")
        text = text.replace("#1-article", "#1-kv-cache-%E4%BF%9D%E7%95%99%E7%AD%96%E7%95%A5")
        issue.write_text(text, encoding="utf-8")
        self.assertNotIn("<a ", text)
        self.assertEqual(archive.check_issue(self.db, self.root, issue), [items[0]["id"]])

    def test_issue_check_rejects_changed_or_duplicate_heading_targets(self):
        items = self.articles(2)
        for old, new, error in (("1. Article", "1. Renamed article", "expected targets"),
                                ("2. Article", "1. Article!", "unique"),
                                ("reported method.", "reported method. [Related](#missing)", "Broken internal")):
            issue = self.issue(items)
            issue.write_text(issue.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")
            with self.subTest(error=error), self.assertRaisesRegex(ValueError, error):
                archive.check_issue(self.db, self.root, issue)

    def test_issue_check_identifies_material_from_local_link_not_other_source_links(self):
        items = self.articles(2)
        issue = self.issue(items[:1])
        text = issue.read_text(encoding="utf-8") + f"\n[Related paper]({items[1]['url']})\n"
        issue.write_text(text, encoding="utf-8")
        self.assertEqual(archive.check_issue(self.db, self.root, issue), [items[0]["id"]])
        issue.write_text(text + f"[Other archive](../materials/{items[1]['id']}/source.html)\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "exactly one material"):
            archive.check_issue(self.db, self.root, issue)

    def test_issue_check_accepts_translated_author_abstract_as_plain_paragraphs(self):
        items = self.articles(1)
        issue = self.issue(items)
        original = "A self-contained description of the problem and the reported method."
        abstract = "\u6211\u4eec\u63d0\u51fa\u4e00\u79cd\u65b9\u6cd5.\n\n\u541e\u5410\u91cf\u63d0\u9ad8\u5230 1.8 \u500d."
        issue.write_text(issue.read_text(encoding="utf-8").replace(original, abstract), encoding="utf-8")
        self.assertEqual(archive.check_issue(self.db, self.root, issue), [items[0]["id"]])

    def test_issue_check_rejects_quoted_or_untranslated_summaries(self):
        items = self.articles(1)
        original = "\u6587\u7ae0\u8bf4\u660e\u4e86\u95ee\u9898\u548c\u65b9\u6cd5. A self-contained description of the problem and the reported method."
        for body, error in (("> \u4f5c\u8005\u6458\u8981\u7684\u4e2d\u6587\u8bd1\u6587.", "not blockquotes"),
                            ("We propose a method. It achieves 1.8x throughput.", "Chinese prose"),
                            ("[\u539f\u59cb\u8bba\u6587](https://example.org/0)", "Chinese prose")):
            issue = self.issue(items)
            issue.write_text(issue.read_text(encoding="utf-8").replace(original, body), encoding="utf-8")
            with self.subTest(body=body), self.assertRaisesRegex(ValueError, error):
                archive.check_issue(self.db, self.root, issue)

    def test_issue_check_ignores_fenced_examples(self):
        issue = self.issue(self.articles(1))
        with issue.open("a", encoding="utf-8") as handle:
            handle.write("\n```markdown\n## Example\n### Not an article\n```\n")
        self.assertEqual(len(archive.check_issue(self.db, self.root, issue)), 1)

    def test_mark_is_per_issue_and_rejects_other_materials(self):
        items = self.articles(21)
        issue = self.issue(items[:20], "part-01.md")
        argv = ["archive.py", "--root", str(self.root), "mark", "used", items[20]["id"], "--issue", str(issue)]
        with mock.patch.object(sys, "argv", argv), self.assertRaisesRegex(ValueError, "present"):
            archive.main()
        self.assertEqual(self.db.execute("SELECT count(*) FROM items WHERE status = 'done'").fetchone()[0], 0)
        for part, selected in ((issue, items[:20]), (self.issue(items[20:], "part-02.md"), items[20:])):
            argv = ["archive.py", "--root", str(self.root), "mark", "used", *[item["id"] for item in selected], "--issue", str(part)]
            with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(archive.main(), 0)
        counts = self.db.execute("SELECT issue_path, count(*) FROM items GROUP BY issue_path").fetchall()
        self.assertEqual(sorted(row[1] for row in counts), [1, 20])

    def test_issue_check_cli_reports_article_ids_without_marking(self):
        items = self.articles(2)
        issue = self.issue(items)
        output = io.StringIO()
        argv = ["archive.py", "--root", str(self.root), "check", str(issue)]
        with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(output):
            self.assertEqual(archive.main(), 0)
        self.assertEqual(json.loads(output.getvalue())["articles"], [item["id"] for item in items])
        self.assertEqual(self.db.execute("SELECT count(*) FROM items WHERE status = 'done'").fetchone()[0], 0)

    def test_unverified_material_can_remain_pending_in_saved_issue(self):
        items = self.articles(2)
        issue = self.issue(items)
        argv = ["archive.py", "--root", str(self.root), "mark", "used", items[0]["id"], "--issue", str(issue)]
        with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(archive.main(), 0)
        row = self.db.execute("SELECT status FROM items WHERE id = ?", (items[1]["id"],)).fetchone()
        self.assertEqual(row["status"], "pending")

    def test_mark_requires_issue_and_clears_pending(self):
        page = b"<html><body>Article</body></html>"
        with mock.patch.object(archive, "fetch", return_value=(page, "text/html", "https://example.org/a")):
            saved = archive.archive(self.db, self.root, {"url": "https://example.org/a", "title": "A"})
        issue = self.issue([saved])
        argv = ["archive.py", "--root", str(self.root), "mark", "used", saved["id"], "--issue", str(issue)]
        with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(archive.main(), 0)
        with mock.patch.object(archive, "fetch") as fetch:
            self.assertIsNone(archive.archive(self.db, self.root, {"url": "https://example.org/a", "title": "A"}))
            fetch.assert_not_called()
        row = self.db.execute("SELECT status, decision, issue_path FROM items").fetchone()
        self.assertEqual(tuple(row), ("done", "used", str(issue)))
        pending_output = io.StringIO()
        with mock.patch.object(sys, "argv", ["archive.py", "--root", str(self.root), "pending"]):
            with contextlib.redirect_stdout(pending_output):
                self.assertEqual(archive.main(), 0)
        self.assertEqual(pending_output.getvalue(), "")
        output = io.StringIO()
        with mock.patch.object(sys, "argv", ["archive.py", "--root", str(self.root), "processed"]):
            with contextlib.redirect_stdout(output):
                self.assertEqual(archive.main(), 0)
        self.assertIn(saved["id"], output.getvalue())
        self.assertEqual(json.loads(output.getvalue())["archive_dir"], saved["archive_dir"])

    def test_private_urls_and_redirects_are_rejected(self):
        with self.assertRaises(ValueError):
            archive.safe_url("http://127.0.0.1/private")
        with self.assertRaises(ValueError):
            archive.CheckedRedirect().redirect_request(
                Request("https://example.org/a"), None, 302, "Found", {}, "http://localhost/private")

    def test_mark_cannot_skip_materials_or_omit_issue(self):
        page = b"<html><body>Article</body></html>"
        with mock.patch.object(archive, "fetch", return_value=(page, "text/html", "https://example.org/a")):
            saved = archive.archive(self.db, self.root, {"url": "https://example.org/a", "title": "A"})
        for decision in ("skipped", "used"):
            argv = ["archive.py", "--root", str(self.root), "mark", decision, saved["id"]]
            with self.subTest(decision=decision), mock.patch.object(sys, "argv", argv):
                with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
                    archive.main()
                self.assertEqual(error.exception.code, 2)
                row = self.db.execute("SELECT status, decision FROM items WHERE id = ?", (saved["id"],)).fetchone()
                self.assertEqual(tuple(row), ("pending", None))

    def test_sync_reuses_only_source_selected_cache_after_database_reset(self):
        page = b"<html><body>Abstract</body></html>"
        pdf = b"%PDF-1.7\noriginal paper"
        first = {"url": "https://arxiv.org/abs/2609.28654", "title": "First"}
        second = {"url": "https://arxiv.org/abs/2609.29444", "title": "Second"}

        def download(url, limit):
            return (pdf, "application/pdf", url) if "/pdf/" in url else (page, "text/html", url)

        with mock.patch.object(archive, "fetch", side_effect=download):
            saved = archive.archive(self.db, self.root, first)
            other = archive.archive(self.db, self.root, second)
        folder = Path(saved["archive_dir"])
        metadata = (folder / "metadata.json").read_bytes()
        with self.db:
            self.db.execute("UPDATE items SET status = 'done', decision = 'used'")
        self.db.close()
        (self.root / "state.sqlite").unlink()
        (self.root / "issues").rmdir()
        self.db = archive.initialize(self.root)
        self.assertEqual(self.db.execute("SELECT count(*) FROM items").fetchone()[0], 0)
        source = "https://huggingface.co/api/daily_papers?limit=100"
        (self.root / "feeds.txt").write_text(source + "\n", encoding="utf-8")
        records = [{"paper": {"id": "2609.28654", "title": "Updated title",
                              "publishedAt": datetime.now(timezone.utc).isoformat()}}]
        output = io.StringIO()
        argv = ["archive.py", "--root", str(self.root), "sync"]
        with mock.patch.object(archive, "fetch", return_value=(json.dumps(records).encode(), "application/json", source)) as fetch:
            with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(output):
                self.assertEqual(archive.main(), 0)
            fetch.assert_called_once_with(source, 8 * 1024 * 1024)
        row = self.db.execute("SELECT id, title, feed_url, status, issue_path FROM items").fetchone()
        self.assertEqual(tuple(row), (saved["id"], "Updated title", source, "pending", None))
        self.assertEqual(self.db.execute("SELECT count(*) FROM items").fetchone()[0], 1)
        self.assertEqual(self.db.execute("SELECT id FROM current_items").fetchone()[0], saved["id"])
        self.assertTrue(Path(other["archive_dir"]).is_dir())
        self.assertEqual((folder / "metadata.json").read_bytes(), metadata)
        self.assertEqual((folder / "paper.pdf").read_bytes(), pdf)
        summary = json.loads(output.getvalue().splitlines()[-1])
        self.assertEqual((summary["new"], summary["downloaded"], summary["reused"]), (1, 0, 1))

    def test_pending_follows_latest_source_selection(self):
        source = "https://example.org/feed"
        (self.root / "feeds.txt").write_text(source + "\n", encoding="utf-8")
        selected = "a"

        def fetch(url, limit):
            if url == source:
                feed = f"""<rss><channel><item><title>{selected}</title>
                    <link>https://example.org/{selected}</link>
                    <pubDate>{format_datetime(datetime.now(timezone.utc))}</pubDate>
                    </item></channel></rss>""".encode()
                return feed, "application/rss+xml", url
            return b"<html><body>Article</body></html>", "text/html", url

        sync = ["archive.py", "--root", str(self.root), "sync"]
        with mock.patch.object(archive, "fetch", side_effect=fetch):
            for selected in ("a", "b"):
                with mock.patch.object(sys, "argv", sync), contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(archive.main(), 0)
        pending = ["archive.py", "--root", str(self.root), "pending"]
        output = io.StringIO()
        with mock.patch.object(sys, "argv", pending), contextlib.redirect_stdout(output):
            self.assertEqual(archive.main(), 0)
        self.assertEqual(json.loads(output.getvalue())["canonical_url"], "https://example.org/b")
        self.assertEqual(self.db.execute("SELECT count(*) FROM items WHERE status = 'pending'").fetchone()[0], 2)
        (self.root / "feeds.txt").write_text("# No sources\n", encoding="utf-8")
        with mock.patch.object(archive, "fetch") as fetch:
            with mock.patch.object(sys, "argv", sync), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(archive.main(), 0)
            fetch.assert_not_called()
        self.assertEqual(self.db.execute("SELECT count(*) FROM current_items").fetchone()[0], 0)

    def test_cached_redirect_rehydrates_without_download(self):
        item = {"url": "http://example.org/old?utm_source=feed", "title": "Article"}
        page = b"<html><body>Cached</body></html>"
        with mock.patch.object(archive, "fetch", return_value=(page, "text/html", "https://example.org/final")):
            saved = archive.archive(self.db, self.root, item)
        with self.db:
            self.db.execute("DELETE FROM items")
            self.db.execute("DELETE FROM current_items")
        with mock.patch.object(archive, "fetch") as fetch:
            restored = archive.archive(self.db, self.root, item)
            fetch.assert_not_called()
        self.assertEqual(restored["id"], saved["id"])
        self.assertFalse(restored["downloaded"])

    def test_new_redirect_reuses_cached_destination(self):
        item = {"url": "https://arxiv.org/abs/2609.28654", "title": "Paper"}
        page = b"<html><body>Cached</body></html>"
        pdf = b"%PDF-1.7\ncached paper"
        with mock.patch.object(archive, "fetch", side_effect=[(page, "text/html", item["url"]),
                                                            (pdf, "application/pdf", "https://arxiv.org/pdf/2609.28654")]):
            saved = archive.archive(self.db, self.root, item)
        with self.db:
            self.db.execute("DELETE FROM items")
            self.db.execute("DELETE FROM current_items")
        with mock.patch.object(archive, "fetch", return_value=(page, "text/html", item["url"])) as fetch:
            restored = archive.archive(self.db, self.root, {"url": "https://example.org/new-short-link", "title": "Paper"})
            fetch.assert_called_once()
        self.assertEqual(restored["id"], saved["id"])
        self.assertEqual((Path(saved["archive_dir"]) / "paper.pdf").read_bytes(), pdf)

    def test_cached_missing_pdf_downloads_only_missing_file(self):
        item = {"url": "https://arxiv.org/abs/2609.28654", "title": "Paper"}
        page = b"<html><body>Cached</body></html>"
        pdf_url = "https://arxiv.org/pdf/2609.28654"
        pdf = b"%PDF-1.7\npaper"
        with mock.patch.object(archive, "fetch", side_effect=[(page, "text/html", item["url"]),
                                                            (pdf, "application/pdf", pdf_url)]):
            saved = archive.archive(self.db, self.root, item)
        folder = Path(saved["archive_dir"])
        (folder / "paper.pdf").unlink()
        with self.db:
            self.db.execute("DELETE FROM items")
            self.db.execute("DELETE FROM current_items")
        with mock.patch.object(archive, "fetch", return_value=(pdf, "application/pdf", pdf_url)) as fetch:
            restored = archive.archive(self.db, self.root, item)
            fetch.assert_called_once_with(pdf_url, 64 * 1024 * 1024)
        self.assertTrue(restored["downloaded"])
        self.assertEqual((folder / "source.html").read_bytes(), page)
        self.assertEqual((folder / "paper.pdf").read_bytes(), pdf)

    def test_invalid_cache_is_not_overwritten_or_registered(self):
        item = {"url": "https://example.org/a", "title": "A"}
        page = b"<html><body>Original</body></html>"
        with mock.patch.object(archive, "fetch", return_value=(page, "text/html", item["url"])):
            saved = archive.archive(self.db, self.root, item)
        folder = Path(saved["archive_dir"])
        (folder / "metadata.json").write_text("{}", encoding="utf-8")
        with self.db:
            self.db.execute("DELETE FROM items")
            self.db.execute("DELETE FROM current_items")
        with mock.patch.object(archive, "fetch") as fetch:
            with self.assertRaises(ValueError):
                archive.archive(self.db, self.root, item)
            fetch.assert_not_called()
        self.assertEqual((folder / "source.html").read_bytes(), page)
        self.assertEqual(self.db.execute("SELECT count(*) FROM items").fetchone()[0], 0)

    def test_cached_missing_source_reuses_existing_pdf(self):
        item = {"url": "https://arxiv.org/abs/2609.28654", "title": "Paper"}
        page = b"<html><body>Abstract</body></html>"
        pdf = b"%PDF-1.7\noriginal paper"
        with mock.patch.object(archive, "fetch", side_effect=[(page, "text/html", item["url"]),
                                                            (pdf, "application/pdf", "https://arxiv.org/pdf/2609.28654")]):
            saved = archive.archive(self.db, self.root, item)
        folder = Path(saved["archive_dir"])
        (folder / "source.html").unlink()
        with self.db:
            self.db.execute("DELETE FROM items")
            self.db.execute("DELETE FROM current_items")
        with mock.patch.object(archive, "fetch", return_value=(page, "text/html", item["url"])) as fetch:
            self.assertIsNotNone(archive.archive(self.db, self.root, item))
            fetch.assert_called_once_with(item["url"], 64 * 1024 * 1024)
        self.assertEqual((folder / "paper.pdf").read_bytes(), pdf)

    def test_cached_direct_pdf_with_generic_content_type_is_reused(self):
        item = {"url": "https://example.org/paper.pdf", "title": "Paper"}
        pdf = b"%PDF-1.7\noriginal paper"
        with mock.patch.object(archive, "fetch", return_value=(pdf, "application/octet-stream", item["url"])):
            saved = archive.archive(self.db, self.root, item)
        with self.db:
            self.db.execute("DELETE FROM items")
            self.db.execute("DELETE FROM current_items")
        with mock.patch.object(archive, "fetch") as fetch:
            restored = archive.archive(self.db, self.root, item)
            fetch.assert_not_called()
        self.assertEqual(restored["id"], saved["id"])
        self.assertFalse(restored["downloaded"])


if __name__ == "__main__":
    unittest.main()
