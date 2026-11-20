import json
import hashlib
import shutil
import sqlite3
import ssl
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import MagicMock, patch

from gacl_pipeline.pipeline import create_https_context, download, run
from gacl_pipeline.store import connect

ROOT = Path(__file__).resolve().parents[1]


def prepare(root):
    shutil.copytree(ROOT / "config", root / "config")
    shutil.copytree(ROOT / "data/examples", root / "data/examples")


class ReviewedExtractTests(unittest.TestCase):
    def test_no_network_no_pdfs_and_duplicate_safe(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepare(root)
            with patch("urllib.request.urlopen", side_effect=AssertionError("Network forbidden")):
                first = run(root, from_examples=True)
                second = run(root, from_examples=True)
            self.assertEqual((first["loaded_rows"], second["warehouse_rows"]), (18, 18))
            self.assertEqual(first["input_mode"], "reviewed_extracts")
            self.assertEqual(first["extracted_rows"], 0)
            self.assertFalse(first["pdfs_verified_this_run"])
            self.assertFalse((root / "data/raw").exists())
            db = sqlite3.connect(root / "data/warehouse/gacl.sqlite")
            try:
                modes = db.execute("SELECT DISTINCT input_mode FROM pipeline_runs").fetchall()
                self.assertEqual(modes, [("reviewed_extracts",)])
            finally:
                db.close()
            manifest = json.loads((root / "data/processed/run_manifest.json").read_text())
            self.assertFalse(manifest["pdfs_verified_this_run"])

    def test_modified_extract_fails_before_loading(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepare(root)
            path = root / "data/examples/monthly_site_observations.csv"
            path.write_text(path.read_text().replace("12540.8", "99999.9"))
            with self.assertRaisesRegex(ValueError, "checksum mismatch"):
                run(root, from_examples=True)
            db = sqlite3.connect(root / "data/warehouse/gacl.sqlite")
            try:
                self.assertEqual(db.execute("SELECT count(*) FROM observations").fetchone()[0], 0)
            finally:
                db.close()

    def test_selected_source_only(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepare(root)
            result = run(root, source_id="gacl_dahej_plot3_ec_2025_h1", from_examples=True)
            self.assertEqual(result["loaded_rows"], 6)
            self.assertEqual(result["warehouse_rows"], 6)

    def test_windows_crlf_uses_same_normalized_checksum(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepare(root)
            for path in (root / "data/examples").glob("*.csv"):
                path.write_bytes(path.read_text().replace("\n", "\r\n").encode())
            self.assertEqual(run(root, from_examples=True)["loaded_rows"], 18)

    def test_conflicting_modes_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "cannot be combined"):
            run(ROOT, offline=True, from_examples=True)


class CertificateTests(unittest.TestCase):
    def test_windows_uses_native_client_context(self):
        native = MagicMock()
        with patch("gacl_pipeline.pipeline.sys.platform", "win32"), patch.dict("sys.modules", {"truststore": native}):
            context = create_https_context()
        native.SSLContext.assert_called_once_with(ssl.PROTOCOL_TLS_CLIENT)
        self.assertIs(context, native.SSLContext.return_value)
        native.inject_into_ssl.assert_not_called()

    def test_other_platforms_require_verified_hostname(self):
        with patch("gacl_pipeline.pipeline.sys.platform", "linux"):
            context = create_https_context()
        self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)
        self.assertTrue(context.check_hostname)

    def test_download_passes_context_and_checks_document_hash(self):
        data = b"%PDF-test certificate context forwarding"
        source = {"source_id": "context-test", "url": "https://example.com/report.pdf",
                  "sha256": hashlib.sha256(data).hexdigest()}
        context = object()
        response = MagicMock()
        response.__enter__.return_value.read.return_value = data
        with tempfile.TemporaryDirectory() as directory:
            with patch("gacl_pipeline.pipeline.create_https_context", return_value=context), patch("urllib.request.urlopen", return_value=response) as call:
                path = download(source, directory)
            self.assertIs(call.call_args.kwargs["context"], context)
            self.assertEqual(path.read_bytes(), data)

    def test_certificate_failures_are_not_retried_or_bypassed(self):
        source = json.loads((ROOT / "config/sources.json").read_text())["sources"][0]
        for wrapped in (False, True):
            error = ssl.SSLCertVerificationError(1, "certificate has expired")
            if wrapped:
                error = urllib.error.URLError(error)
            with self.subTest(wrapped=wrapped), tempfile.TemporaryDirectory() as directory:
                with patch("urllib.request.urlopen", side_effect=error) as call, patch("time.sleep"):
                    with self.assertRaisesRegex(ValueError, "--from-examples"):
                        download(source, directory)
                    self.assertEqual(call.call_count, 1)


class MigrationTests(unittest.TestCase):
    def test_existing_run_history_survives_input_mode_migration(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "old.sqlite"
            db = sqlite3.connect(path)
            db.execute("""CREATE TABLE pipeline_runs
                (run_id TEXT PRIMARY KEY, started_at TEXT, ended_at TEXT,
                 status TEXT, selected_sources TEXT, row_count INTEGER, error TEXT)""")
            db.execute("INSERT INTO pipeline_runs VALUES ('old','time',NULL,'failed','[]',0,'SSL')")
            db.commit()
            db.close()
            migrated = connect(path)
            try:
                self.assertEqual(migrated.execute("SELECT status FROM pipeline_runs WHERE run_id='old'").fetchone()[0], "failed")
                self.assertIn("input_mode", {r[1] for r in migrated.execute("PRAGMA table_info(pipeline_runs)")})
            finally:
                migrated.close()
