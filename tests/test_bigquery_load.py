"""Cloud-boundary tests use the real SDK types and a mocked remote client."""
import contextlib
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

try:
    from google.cloud import bigquery
except ImportError:
    bigquery = None

from gacl_pipeline.bigquery_load import main
from gacl_pipeline.examples import load_examples

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipIf(bigquery is None, 'Install ".[cloud]" for cloud-boundary tests')
class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        shutil.copytree(ROOT / "config", self.root / "config")
        shutil.copytree(ROOT / "data/examples", self.root / "data/examples")
        sources = json.loads((self.root / "config/sources.json").read_text())["sources"]
        self.rows = load_examples(self.root, {s["source_id"] for s in sources})
        self.path = self.root / "data/processed/observations.json"
        self.path.parent.mkdir()
        self.path.write_text(json.dumps(self.rows))
        self.args = ["--root", str(self.root), "--project", "example-project",
                     "--mode", "snapshot"]
        self.sdk = self.enterContext(patch("google.cloud.bigquery.Client"))
        self.client = self.sdk.return_value
        self.client.get_dataset.return_value.location = "asia-south1"
        self.client.get_table.return_value = SimpleNamespace(num_rows=18, expires=None)
        self.job = self.client.load_table_from_json.return_value
        self.job.job_id = "test-load-job"
        self.output = self.enterContext(contextlib.redirect_stdout(io.StringIO()))

    def test_full_snapshot_reruns_use_replacement_without_dml(self):
        for _ in range(2):
            self.assertEqual(main(self.args), 0)
        self.assertEqual(self.client.load_table_from_json.call_count, 2)
        for call in self.client.load_table_from_json.call_args_list:
            self.assertEqual(len(call.args[0]), 18)
            self.assertEqual(call.args[1], "example-project.gacl_public_disclosures.observations")
            config = call.kwargs["job_config"]
            self.assertEqual(config.write_disposition, "WRITE_TRUNCATE")
            self.assertEqual(config.max_bad_records, 0)
            self.assertFalse(config.ignore_unknown_values)
        self.client.query.assert_not_called()
        self.client.delete_table.assert_not_called()
        self.client.create_table.assert_not_called()
        summary = json.loads((self.root / "logs/bigquery_latest_run.json").read_text())
        self.assertEqual((summary["load_mode"], summary["warehouse_rows"]), ("snapshot", 18))
        self.assertEqual(summary["job_id"], "test-load-job")

    def test_incomplete_or_invalid_snapshot_never_contacts_cloud(self):
        variants = [[], self.rows[:-1],
                    [r for r in self.rows if r["frequency"] == "monthly"],
                    [r for r in self.rows if r["frequency"] == "annual"],
                    self.rows + [self.rows[0]],
                    [dict(r, unit="wrong") for r in self.rows]]
        for rows in variants:
            with self.subTest(count=len(rows)):
                self.path.write_text(json.dumps(rows))
                with self.assertRaisesRegex(ValueError, "Refusing cloud load"):
                    main(self.args)
                self.sdk.assert_not_called()

    def test_location_mismatch_stops_before_upload(self):
        self.client.get_dataset.return_value.location = "US"
        with self.assertRaisesRegex(ValueError, "location differs"):
            main(self.args)
        self.client.load_table_from_json.assert_not_called()

    def test_failed_batch_job_has_no_delete_or_success_record(self):
        self.job.result.side_effect = RuntimeError("remote load rejected")
        with self.assertRaisesRegex(RuntimeError, "remote load rejected"):
            main(self.args)
        self.client.delete_table.assert_not_called()
        self.client.query.assert_not_called()
        self.assertFalse((self.root / "logs/bigquery_latest_run.json").exists())

    def test_row_count_mismatch_is_not_reported_as_success(self):
        self.client.get_table.return_value.num_rows = 17
        with self.assertRaisesRegex(ValueError, "row count differs"):
            main(self.args)
        self.assertFalse((self.root / "logs/bigquery_latest_run.json").exists())

    def test_explicit_merge_keeps_original_staging_and_cleanup(self):
        args = list(self.args)
        args[-1] = "merge"
        self.assertEqual(main(args), 0)
        staging = self.client.load_table_from_json.call_args.args[1]
        self.assertIn("._load_", staging)
        self.assertIn("MERGE", self.client.query.call_args.args[0])
        self.client.delete_table.assert_called_once_with(staging, not_found_ok=True)

    def test_load_mode_is_required_before_cloud_access(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            main(self.args[:-2])
        self.sdk.assert_not_called()
