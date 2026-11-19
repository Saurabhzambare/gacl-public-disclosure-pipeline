import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from gacl_pipeline.extract import observation, parse_number
from gacl_pipeline.pipeline import download, run
from gacl_pipeline.store import connect, load
from gacl_pipeline.validate import reconcile, validate_rows

ROOT = Path(__file__).resolve().parents[1]
SOURCES = json.loads((ROOT / "config/sources.json").read_text())["sources"]
METRICS = json.loads((ROOT / "config/metrics.json").read_text())


def sample():
    return observation(SOURCES[0], "freshwater_average_daily", "2025-04-01",
                       "2025-04-30", "monthly", "monthly_average_daily_rate",
                       "KL/day", "12540.8", 5, 4)


class NumberTests(unittest.TestCase):
    def test_indian_number_preserves_decimal(self):
        self.assertEqual(str(parse_number("18,26,958.988")), "1826958.988")

    def test_missing_is_not_zero(self):
        self.assertIsNone(parse_number("NA"))
        self.assertIsNone(parse_number("-"))
        self.assertEqual(parse_number("0"), 0)

    def test_malformed_and_nonfinite_rejected(self):
        for value in ("1,2,34", "NaN", "Infinity", "12abc"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_number(value)


class ContractTests(unittest.TestCase):
    def test_valid_observation(self):
        valid, bad = validate_rows([sample()], METRICS, SOURCES)
        self.assertEqual(len(valid), 1)
        self.assertEqual(bad, [])

    def test_unit_scope_and_period_rejected(self):
        for key, value in (("unit", "KL"), ("reporting_scope", "gacl_standalone"),
                           ("period_end", "2025-04-29"), ("pdf_page", 99),
                           ("value", "-2")):
            row = sample()
            row[key] = value
            with self.subTest(key=key):
                self.assertTrue(validate_rows([row], METRICS, SOURCES)[1])

    def test_duplicate_is_quarantined(self):
        row = sample()
        valid, rejected = validate_rows([row, copy.deepcopy(row)], METRICS, SOURCES)
        self.assertEqual((len(valid), len(rejected)), (1, 1))

    def test_edited_normalized_value_is_rejected(self):
        row = dict(sample(), value="999")
        self.assertIn("raw_value_mismatch", validate_rows([row], METRICS, SOURCES)[1][0]["reasons"])

    def test_edited_identity_is_rejected(self):
        row = dict(sample(), observation_id="incorrect")
        self.assertIn("invalid_observation_identity", validate_rows([row], METRICS, SOURCES)[1][0]["reasons"])

    def test_missing_months_fail_coverage(self):
        self.assertFalse(reconcile([sample()], {SOURCES[0]["source_id"]})[0]["passed"])

    def test_rounding_tolerance_and_real_mismatch(self):
        rows = []
        for metric, val in (("energy_total", "11085192.06"),
                            ("energy_renewable_total", "1826958.988"),
                            ("energy_nonrenewable_total", "9258233.07")):
            rows.append({"source_id": SOURCES[1]["source_id"], "period_start": "2024-04-01",
                         "metric_id": metric, "value": val})
        checks = reconcile(rows, {SOURCES[1]["source_id"]})
        self.assertTrue(next(c for c in checks if c["check_id"].endswith("2024-04-01"))["passed"])
        rows[0]["value"] = "11085199"
        checks = reconcile(rows, {SOURCES[1]["source_id"]})
        self.assertFalse(next(c for c in checks if c["check_id"].endswith("2024-04-01"))["passed"])


class StorageTests(unittest.TestCase):
    def test_rerun_is_idempotent_and_versions_are_retained(self):
        with tempfile.TemporaryDirectory() as directory:
            db = connect(Path(directory) / "test.sqlite")
            row = sample()
            load(db, [row])
            load(db, [row])
            self.assertEqual(db.execute("SELECT count(*) FROM observations").fetchone()[0], 1)
            revised = dict(row, document_sha256="new_version")
            load(db, [revised])
            self.assertEqual(db.execute("SELECT count(*) FROM observations").fetchone()[0], 2)
            db.close()


class DownloadTests(unittest.TestCase):
    def test_changed_source_does_not_overwrite_cache(self):
        with tempfile.TemporaryDirectory() as directory:
            cached = Path(directory) / (SOURCES[0]["source_id"] + ".pdf")
            cached.write_bytes(b"existing document")
            fake_response = unittest.mock.MagicMock()
            fake_response.__enter__.return_value.read.return_value = b"%PDF changed bytes"
            with patch("urllib.request.urlopen", return_value=fake_response):
                with self.assertRaisesRegex(ValueError, "Source changed"):
                    download(SOURCES[0], directory, refresh=True)
            self.assertEqual(cached.read_bytes(), b"existing document")

    def test_transient_download_has_bounded_retries(self):
        import urllib.error
        with tempfile.TemporaryDirectory() as directory, patch("urllib.request.urlopen", side_effect=urllib.error.URLError("temporary")) as call, patch("time.sleep"):
            with self.assertRaises(urllib.error.URLError):
                download(SOURCES[0], directory)
            self.assertEqual(call.call_count, 3)


class FailureTests(unittest.TestCase):
    def test_offline_missing_source_records_failed_run(self):
        import shutil
        with tempfile.TemporaryDirectory() as directory:
            shutil.copytree(ROOT / "config", Path(directory) / "config")
            with self.assertRaisesRegex(ValueError, "Offline source missing"):
                run(directory, offline=True)
            latest = json.loads((Path(directory) / "logs/latest_run.json").read_text())
            self.assertEqual(latest["status"], "failed")

    def test_unknown_source_and_conflicting_options(self):
        with self.assertRaisesRegex(ValueError, "Unknown source"):
            run(ROOT, source_id="not-a-source", offline=True)
        with self.assertRaisesRegex(ValueError, "cannot be combined"):
            run(ROOT, offline=True, refresh=True)


if __name__ == "__main__":
    unittest.main()

