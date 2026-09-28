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

    def test_sync_only_archives_unseen_items_within_three_years(self):
        feed_url = "https://example.org/feed"
        cutoff = archive.three_year_cutoff(datetime.now(timezone.utc))
        recent = format_datetime(datetime.now(timezone.utc))
        old = format_datetime(cutoff - timedelta(days=1))
        feed = f"""<rss><channel>
            <item><title>Recent</title><link>https://example.org/recent</link><pubDate>{recent}</pubDate></item>
            <item><title>Old</title><link>https://example.org/old</link><pubDate>{old}</pubDate></item>
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
        self.assertEqual(self.db.execute("SELECT count(*) FROM items").fetchone()[0], 1)
        self.assertIn('"skipped_old": 1', output.getvalue())
        self.assertIn('"skipped_undated": 1', output.getvalue())

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

    def test_mark_requires_issue_and_clears_pending(self):
        page = b"<html><body>Article</body></html>"
        with mock.patch.object(archive, "fetch", return_value=(page, "text/html", "https://example.org/a")):
            saved = archive.archive(self.db, self.root, {"url": "https://example.org/a", "title": "A"})
        issue = self.root / "issues" / "newsletter-20260927-1200.md"
        issue.write_text("# Newsletter", encoding="utf-8")
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
