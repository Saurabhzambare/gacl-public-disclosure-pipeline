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

from gacl_pipeline.retrieval import (
    chunk_page,
    chunk_text,
    extract_chunks,
    extract_documents,
    extract_page,
    main,
)

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
            "max_chunk_chars": 1800,  # Maximum characters in each chunk.
            "overlap_chars": 250,    # Target shared characters between chunks.
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

    def test_chunk_batch_keeps_page_lineage(self) -> None:
        """Every batch chunk must point to an exact span in its own parent page."""
        result = extract_chunks(self.root)
        self.assertEqual(result["usable_pages"], 2)
        self.assertEqual(result["chunk_count"], 2)  # Both synthetic pages are short.
        document = result["documents"][0]
        pages = {page["pdf_page"]: page for page in document["pages"]}
        for chunk in document["chunks"]:
            page = pages[chunk["pdf_page"]]
            self.assertEqual(chunk["text"], page["text"][chunk["start_char"]:chunk["end_char"]])
            self.assertEqual(chunk["page_text_sha256"], page["text_sha256"])
            self.assertEqual(chunk["citation_url"], page["citation_url"])
            self.assertEqual(chunk["reviewed_note"], page["reviewed_note"])

    def test_chunk_cli_summary(self) -> None:
        """The new chunk command must show counts without dumping text bodies."""
        output = io.StringIO()
        arguments = ["retrieval", "--root", str(self.root), "--chunks", "--summary"]
        with patch("sys.argv", arguments), redirect_stdout(output):
            main()
        result = json.loads(output.getvalue())
        self.assertEqual(result["chunk_count"], 2)
        self.assertNotIn("pages", result["documents"][0])
        self.assertNotIn("chunks", result["documents"][0])

    def test_invalid_chunk_settings_fail_before_pdf_read(self) -> None:
        """Bad window settings must fail before any cached PDF is needed."""
        self.settings["overlap_chars"] = self.settings["max_chunk_chars"]
        self.write_config()
        self.pdf_path.unlink()  # A missing PDF would otherwise raise OSError.
        with self.assertRaisesRegex(ValueError, "overlap_chars"):
            extract_chunks(self.root)

class ChunkSpanTests(unittest.TestCase):
    """Check exact spans, boundary behaviour and chunk identities using small strings."""

    def make_page(self, text: str = "abcdefghijklmnopqrst") -> dict:
        """Return a synthetic page record with all required provenance fields."""
        return {
            "source_id": "synthetic",
            "document_sha256": "a" * 64,
            "source_url": "https://example.test/sample.pdf",
            "reporting_scope": "synthetic_test_scope",
            "pdf_page": 2,
            "printed_page": None,
            "page_count": 3,
            "text": text,
            "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "reviewed_note": "REVIEW_ONLY_SENTINEL",
            "section": None,
            "extraction_version": "synthetic-extraction-v1",
            "pymupdf_version": fitz.VersionBind,
            "citation_url": "https://example.test/sample.pdf#page=2",
        }

    def assert_coverage(self, text: str, spans: list[dict], maximum: int) -> None:
        """Check exact slices, full coverage, bounded size and advancing ends."""
        if not text:
            self.assertEqual(spans, [])
            return
        self.assertEqual(spans[0]["start_char"], 0)
        covered_until = 0
        for span in spans:
            start, end = span["start_char"], span["end_char"]
            self.assertLessEqual(start, covered_until)  # No gap in page coverage.
            self.assertGreater(end, covered_until)  # Each chunk adds new content.
            self.assertLess(start, end)
            self.assertLessEqual(end - start, maximum)
            self.assertEqual(span["text"], text[start:end])
            covered_until = end
        self.assertEqual(covered_until, len(text))

    def test_empty_short_and_whitespace_text(self) -> None:
        """Keep nonempty whitespace exactly; empty text produces no spans."""
        for text in ("", "short", " \n\t "):
            with self.subTest(text=text):
                spans = chunk_text(text, 10, 3)
                self.assert_coverage(text, spans, 10)
                if text:
                    self.assertEqual(len(spans), 1)

    def test_exact_limit_has_one_chunk(self) -> None:
        """A page exactly at the limit must not produce a redundant tail."""
        spans = chunk_text("abcdefghij", 10, 3)
        self.assertEqual(len(spans), 1)
        self.assertEqual((spans[0]["start_char"], spans[0]["end_char"]), (0, 10))

    def test_long_line_offsets_and_overlap(self) -> None:
        """Without newlines, use bounded windows and the exact target overlap."""
        text = "abcdefghijklmnopqrst"
        spans = chunk_text(text, 10, 3)
        self.assertEqual(
            [(span["start_char"], span["end_char"]) for span in spans],
            [(0, 10), (7, 17), (14, 20)],
        )
        self.assert_coverage(text, spans, 10)

    def test_newline_preference_makes_overlap_approximate(self) -> None:
        """Line alignment may reduce the overlap while preserving full coverage."""
        text = "abcd\n" * 12
        spans = chunk_text(text, 20, 8)
        self.assertEqual(spans[0]["end_char"], 20)
        self.assertEqual(spans[1]["start_char"], 15)
        self.assertEqual(spans[0]["end_char"] - spans[1]["start_char"], 5)
        self.assert_coverage(text, spans, 20)

    def test_zero_overlap_reconstructs_text(self) -> None:
        """With zero overlap, concatenating chunks must recover the page."""
        text = "abcdefghijklmnopqrs"
        spans = chunk_text(text, 6, 0)
        self.assertEqual("".join(span["text"] for span in spans), text)
        self.assert_coverage(text, spans, 6)

    def test_large_valid_overlap_still_advances(self) -> None:
        """An overlap one character below the maximum must terminate."""
        text = "abcdef" * 5
        spans = chunk_text(text, 5, 4)
        self.assertEqual(len(spans), 26)
        self.assertTrue(all(
            later["start_char"] > earlier["start_char"]
            for earlier, later in zip(spans, spans[1:])
        ))
        self.assert_coverage(text, spans, 5)

    def test_invalid_text_and_parameters(self) -> None:
        """Reject invalid types, bool, negative overlap and overlap at/above size."""
        settings = ((0, 0), (-1, 0), (True, 0), (10, True), (10, -1), (10, 10), (10, 11), (10, 1.5))
        for maximum, overlap in settings:
            with self.subTest(maximum=maximum, overlap=overlap):
                with self.assertRaises(ValueError):
                    chunk_text("sample", maximum, overlap)
        with self.assertRaisesRegex(ValueError, "must be a string"):
            chunk_text(None, 10, 3)

    def test_unicode_character_offsets(self) -> None:
        """Offsets are Python character positions, not UTF-8 byte positions."""
        text = "जल 💧 café\n" * 8
        spans = chunk_text(text, 17, 4)
        self.assert_coverage(text, spans, 17)
        self.assertNotEqual(len(text), len(text.encode("utf-8")))

    def test_ids_are_stable_and_page_is_unchanged(self) -> None:
        """Repeated chunking must reproduce IDs without modifying the input."""
        page = self.make_page()
        original = dict(page)
        first = chunk_page(page, 10, 3)
        second = chunk_page(page, 10, 3)
        self.assertEqual(first, second)
        self.assertEqual(page, original)
        self.assertEqual(len({chunk["chunk_id"] for chunk in first}), len(first))

    def test_identity_changes_with_content_metadata_or_settings(self) -> None:
        """Chunk identity must cover page version, review metadata and settings."""
        page = self.make_page()
        original_id = chunk_page(page, 10, 3)[0]["chunk_id"]
        for key, value in (
            ("document_sha256", "b" * 64),
            ("printed_page", 44),
            ("reporting_scope", "different_synthetic_scope"),
            ("reviewed_note", "Changed reviewed note"),
            ("extraction_version", "synthetic-extraction-v2"),
        ):
            with self.subTest(key=key):
                changed = dict(page)
                changed[key] = value
                self.assertNotEqual(chunk_page(changed, 10, 3)[0]["chunk_id"], original_id)
        changed = dict(page)
        changed["text"] += "!"
        changed["text_sha256"] = hashlib.sha256(changed["text"].encode("utf-8")).hexdigest()
        self.assertNotEqual(chunk_page(changed, 10, 3)[0]["chunk_id"], original_id)
        self.assertNotEqual(chunk_page(page, 11, 3)[0]["chunk_id"], original_id)
        self.assertNotEqual(chunk_page(page, 10, 2)[0]["chunk_id"], original_id)

    def test_tampered_page_text_hash_fails(self) -> None:
        """A page string changed after extraction must fail its stored text hash."""
        page = self.make_page()
        page["text"] += "changed"
        with self.assertRaisesRegex(ValueError, "Page text SHA-256 mismatch"):
            chunk_page(page, 10, 3)

    def test_chunk_records_keep_citations_and_separate_notes(self) -> None:
        """Retain parent provenance while hashing only the exact chunk text."""
        page = self.make_page()
        for chunk in chunk_page(page, 10, 3):
            self.assertEqual(chunk["citation_url"], page["citation_url"])
            self.assertEqual(chunk["printed_page"], page["printed_page"])
            self.assertEqual(chunk["reviewed_note"], page["reviewed_note"])
            self.assertEqual(chunk["page_text_sha256"], page["text_sha256"])
            self.assertEqual(
                chunk["text_sha256"],
                hashlib.sha256(chunk["text"].encode("utf-8")).hexdigest(),
            )
            self.assertNotIn("REVIEW_ONLY_SENTINEL", chunk["text"])


if __name__ == "__main__":
    unittest.main()