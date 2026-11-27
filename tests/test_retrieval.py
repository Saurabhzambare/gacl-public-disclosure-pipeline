"""Check page provenance and failure boundaries using temporary synthetic PDFs."""

import hashlib
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import fitz

from gacl_pipeline.retrieval import extract_documents, extract_page, main


class PageEvidenceTests(unittest.TestCase):
    """Give each test an isolated repository-shaped directory and small PDF."""

    def setUp(self) -> None:
        """Create three pages: blank, reviewed text and unmapped text."""
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)  # Run even when an assertion fails.
        self.root = Path(temporary.name)
        (self.root / "config").mkdir()
        (self.root / "data" / "raw").mkdir(parents=True)

        with fitz.open() as document:
            document.new_page()  # Optional blank page should be reported as skipped.
            reviewed = document.new_page()
            reviewed.insert_text((72, 72), "Verified sample evidence for water and energy reporting.")
            unmapped = document.new_page()
            unmapped.insert_text((72, 72), "Another readable page whose printed label is not configured.")
            pdf_bytes = document.tobytes()
        self.pdf_path = self.root / "data" / "raw" / "sample.pdf"
        self.pdf_path.write_bytes(pdf_bytes)
        self.document_hash = hashlib.sha256(pdf_bytes).hexdigest()
        self.source = {
            "source_id": "sample",
            "url": "https://example.test/sample.pdf",
            "sha256": self.document_hash,
            "reporting_scope": "synthetic_test_scope",
            "pages": [{"pdf_page": 2, "printed_page": 10}],
        }
        self.settings = {
            "schema_version": 1,
            "min_alnum_chars": 30,
            "reviewed_pages": [{
                "source_id": "sample",
                "document_sha256": self.document_hash,
                "pdf_page": 2,
                "printed_page": 10,
                "reviewed_note": "REVIEW_ONLY_SENTINEL: separate synthetic reviewer note.",
            }],
        }
        self.write_config()

    def write_config(self) -> None:
        """Save this test's source/settings dictionaries into its temporary root."""
        (self.root / "config" / "sources.json").write_text(
            json.dumps({"sources": [self.source]}), encoding="utf-8"
        )
        (self.root / "config" / "retrieval.json").write_text(
            json.dumps(self.settings), encoding="utf-8"
        )

    def test_exact_text_hash_and_separate_review(self) -> None:
        """Raw extraction must round-trip exactly; notes must not enter text."""
        evidence = extract_page(self.root, "sample", 2)
        with fitz.open(self.pdf_path) as document:
            expected = document.load_page(1).get_text("text", sort=True)
        self.assertEqual(evidence["text"], expected)
        self.assertEqual(evidence["text_sha256"], hashlib.sha256(expected.encode("utf-8")).hexdigest())
        self.assertEqual(evidence["document_sha256"], self.document_hash)
        self.assertEqual(evidence["printed_page"], 10)
        self.assertEqual(evidence["reporting_scope"], "synthetic_test_scope")
        self.assertEqual(evidence["citation_url"], self.source["url"] + "#page=2")
        self.assertEqual(evidence["reviewed_note"], self.settings["reviewed_pages"][0]["reviewed_note"])
        self.assertNotIn("REVIEW_ONLY_SENTINEL", evidence["text"])
        self.assertIsNone(evidence["section"])

    def test_unknown_label_stays_none(self) -> None:
        """A nearby known page label must not create an inferred offset."""
        evidence = extract_page(self.root, "sample", 3)
        self.assertIsNone(evidence["printed_page"])
        self.assertIsNone(evidence["reviewed_note"])

    def test_batch_counts_and_explicit_skip(self) -> None:
        """Two readable pages plus one optional blank page must be accounted for."""
        result = extract_documents(self.root)
        self.assertEqual((result["source_count"], result["physical_pages"]), (1, 3))
        self.assertEqual((result["usable_pages"], result["skipped_page_count"]), (2, 1))
        document = result["documents"][0]
        self.assertEqual([page["pdf_page"] for page in document["pages"]], [2, 3])
        self.assertEqual(document["skipped_pages"][0]["pdf_page"], 1)
        self.assertEqual(document["skipped_pages"][0]["reason"], "insufficient_embedded_text_no_ocr")

    def test_changed_pdf_fails_hash_check(self) -> None:
        """Changed cached bytes must fail before they are parsed."""
        self.pdf_path.write_bytes(b"changed cached PDF")
        with self.assertRaisesRegex(ValueError, "checksum mismatch"):
            extract_documents(self.root)

    def test_stale_review_fails(self) -> None:
        """A review for a different document version must not be reused."""
        self.settings["reviewed_pages"][0]["document_sha256"] = "0" * 64
        self.write_config()
        with self.assertRaisesRegex(ValueError, "Reviewed-note document hash"):
            extract_documents(self.root)

    def test_conflicting_labels_fail(self) -> None:
        """A retrieval review cannot silently replace the register's label."""
        self.settings["reviewed_pages"][0]["printed_page"] = 99
        self.write_config()
        with self.assertRaisesRegex(ValueError, "Conflicting printed-page"):
            extract_documents(self.root)

    def test_duplicate_review_fails(self) -> None:
        """Duplicate annotations are ambiguous even if their contents match."""
        self.settings["reviewed_pages"].append(dict(self.settings["reviewed_pages"][0]))
        self.write_config()
        with self.assertRaisesRegex(ValueError, "Duplicate reviewed-page"):
            extract_documents(self.root)

    def test_invalid_threshold_fails(self) -> None:
        """Reject bool and invalid numeric threshold settings."""
        for threshold in (True, 0, -1, 1.5):
            with self.subTest(threshold=threshold):
                self.settings["min_alnum_chars"] = threshold
                self.write_config()
                with self.assertRaisesRegex(ValueError, "min_alnum_chars"):
                    extract_documents(self.root)

    def test_required_blank_page_fails(self) -> None:
        """An unreadable required reference must not disappear into the skip list."""
        self.source["pages"].append({"pdf_page": 1, "printed_page": None})
        self.write_config()
        with self.assertRaisesRegex(ValueError, "page 1 has insufficient"):
            extract_documents(self.root)

    def test_required_page_outside_document_fails(self) -> None:
        """A required reference beyond the actual PDF length is an error."""
        self.source["pages"].append({"pdf_page": 4, "printed_page": None})
        self.write_config()
        with self.assertRaisesRegex(ValueError, "outside the PDF page range"):
            extract_documents(self.root)

    def test_invalid_page_selection_fails(self) -> None:
        """Reject invalid human page inputs and an out-of-range positive page."""
        for selection in (True, 0, -1, 1.5):
            with self.subTest(selection=selection):
                with self.assertRaisesRegex(ValueError, "positive integer"):
                    extract_page(self.root, "sample", selection)
        with self.assertRaisesRegex(ValueError, "only 3 pages"):
            extract_page(self.root, "sample", 4)

    def test_unknown_source_fails(self) -> None:
        """The source argument must not select an unregistered path or report."""
        with self.assertRaisesRegex(ValueError, "Unknown source ID"):
            extract_documents(self.root, "unknown")

    def test_existing_page_cli_and_batch_summary(self) -> None:
        """Keep the old page command and verify the new summary display."""
        selections = (["--source", "sample", "--page", "2"], ["--all-pages", "--summary"])
        for selection in selections:
            with self.subTest(selection=selection):
                output = io.StringIO()
                arguments = ["retrieval", "--root", str(self.root), *selection]
                with patch("sys.argv", arguments), redirect_stdout(output):
                    main()
                result = json.loads(output.getvalue())
                if "--page" in selection:
                    self.assertEqual(result["pdf_page"], 2)
                else:
                    self.assertEqual(result["usable_pages"], 2)
                    self.assertNotIn("pages", result["documents"][0])


if __name__ == "__main__":
    unittest.main()