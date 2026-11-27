# Phase 2 — Step 4B: Extract usable pages without mixing evidence and notes

Build-order version: 1.0. Prepared: 27 November 2026 (India).
Prerequisite: Step 4A execution passed and the author supplied the complete
122-line retrieval.py for review. Its contents match the Step 4A lesson.
Status: learner batch extraction, offline core regression and both software-test
runs and all four real-page metadata checks passed on Windows. Local checkpoint
commit and learner visual-review confirmation remain pending.
This finishes the second exercise within Step 4. Step 5 is still chunking.

## Recorded partial execution — 27 November

Author-supplied Windows output confirms 2 pinned PDFs, 71 physical / 70 usable
pages, monthly 20/21 and annual 50/50. Monthly physical page 1 is skipped with
zero alphanumeric characters and the configured no-OCR reason. Offline run
a8998693-ba1f-4044-b3b5-169b84456ca8 verifies cached PDFs and retains
18 extracted/loaded/stored observations with all four checks passing.
Git shows exactly the three intended untracked files on feature/phase2-guided.

The author then supplied 13 focused tests passing in 0.634 seconds and all
45 tests passing in 1.620 seconds, with no failures or skips shown. The full suite
includes the 13 retrieval tests and 32 existing tests. These synthetic-fixture
checks complement the real-source batch run; they do not replace visual review.
All four detailed metadata records have since been supplied: monthly labels 4/null,
unchanged monthly text hashes, and annual printed labels 43/79 with separate
reviewed notes. The learner's own visual comparison remains pending. A local
checkpoint commit can now save the verified implementation; its commit ID/clean
status, documentation synchronization and understanding discussion remain open.
See [the learning log](AI_LEARNING_LOG.md) for evidence. Successful tests need not
be repeated without a relevant code change.

## Purpose, ELI5 and boundaries

Step 4A returns one page in an evidence envelope. Step 4B prepares envelopes for
every usable page in the two approved reports. It opens each PDF once during a
batch, keeps the words unchanged, and records which pages it could not read.

ELI5: a librarian copies each readable page into its own envelope. The address
on the envelope identifies the book and page. If a person checked something
visually, their sticky note stays separate from the copied words. A blank or
picture-only page gets an entry in a skip list, not invented text.

Why now: chunking and retrieval need consistent evidence records. If we mix a
human interpretation into raw text, a later search cannot distinguish what the
PDF extractor read from what a reviewer added.

We still have 18 numerical observations. Text pages are a different unit of
work; 70 usable pages would not mean 70 measurements or 70 passing tests.
There is no model, OCR, search, index, database write or generated answer here.

## Installations and exact files

No new installation. Reuse Python 3.11+ and the installed PyMuPDF 1.26.6.
argparse, hashlib, json, pathlib, tempfile, io and unittest are standard-library
modules. No API key, cloud account, GPU or model download is needed.

All paths below are relative to `D:\gacl-public-disclosure-pipeline`.
Stay on `feature/phase2-guided`.

| File | Action |
|---|---|
| config/retrieval.json | Create the JSON file in the existing config folder |
| src/gacl_pipeline/retrieval.py | Replace the inspected Step 4A module with the complete version below |
| tests/test_retrieval.py | Create the focused test file in the existing tests folder |

The module replacement is intentional: shared helpers now serve both one-page
and all-page extraction without copying verification logic. The existing
extract_page(root, source_id, pdf_page) interface and `--source ... --page ...`
command remain. Page records gain reviewed_note and section fields. A page must
now meet the configured minimum readable-text threshold, not merely be nonempty.

Do not change config/sources.json or scripts/inspect_source_page.py. Do not
merge documentation, commit the partial lesson or create Step 5 files yet.
Read this lesson online while implementing; documentation synchronization will
be handled at the Step 4 checkpoint after inspecting the actual branch state.

First inspect status and confirm the new paths are absent:

```powershell
Set-Location "D:\gacl-public-disclosure-pipeline"
git status --short --branch
Test-Path .\config\retrieval.json
Test-Path .\tests\test_retrieval.py
```

Expected starting status: only the existing untracked retrieval.py. If either
new path already exists, inspect its contents before replacing it. Keep any
unexpected changes and share them for review.

## 1. Create config/retrieval.json

Configuration contains choices and reviewed metadata. It does not contain the
extracted page text. JSON has no comments, so the explanations follow the block.

```json
{
  "schema_version": 1,
  "min_alnum_chars": 30,
  "reviewed_pages": [
    {
      "source_id": "gacl_brsr_2025_26",
      "document_sha256": "9fa0d33a69af711744590ad564145b93b2891e77f2e86004084bb89ba3390230",
      "pdf_page": 1,
      "printed_page": 43,
      "reviewed_note": "Visual-review note (assistant, 24 November 2026): Section A, item 13 states that the reporting boundary is standalone. Item 9 gives the financial year as 1 April 2025 to 31 March 2026. These labels are incomplete in embedded text extraction."
    },
    {
      "source_id": "gacl_brsr_2025_26",
      "document_sha256": "9fa0d33a69af711744590ad564145b93b2891e77f2e86004084bb89ba3390230",
      "pdf_page": 37,
      "printed_page": 79,
      "reviewed_note": "Visual-review note (assistant, 24 November 2026): FY 2024-25 disclosures are recalculated comparatives aligned with the FY 2025-26 reporting boundary and methodology. The note attributes higher FY 2025-26 annual water consumption to increased production. These notes are incomplete in embedded text extraction."
    }
  ]
}
```

| Setting | Why it exists |
|---|---|
| schema_version | Identifies the supported configuration layout; this lesson accepts integer 1 |
| min_alnum_chars | Requires at least 30 letters/digits in extracted text; whitespace and punctuation do not count |
| reviewed_pages | Explicit additions from visual review, separate from raw text |
| document_sha256 | Ties each review to the exact approved PDF version |
| pdf_page / printed_page | Physical address and reviewed printed label; no guessed offset |
| reviewed_note | Labelled interpretation, never appended to text |

Thirty characters is a transparent initial quality filter, not proof that a
page is correctly understood. A scanned page with a small text footer may also
fail it. A page above the threshold can still contain extraction errors.
Required source/reference pages must pass; other pages below it are reported
as skipped. We do not claim that every skipped page is necessarily image-only.

The two notes reuse the assistant's recorded visual review of the pinned
annual report on 24 November. They are not new learner review attestations.
Open the cached annual PDF and personally compare physical pages 1 and 37 with
these notes before using them. Physical page 1 carries printed label 43.
The source register's existing page-37 mapping agrees with printed page 79.
If a note or label disagrees with the document, stop and share the discrepancy.
Do not invent a new approved PDF hash to bypass the check.

The production explanation concerns annual company water consumption only.
It does not explain the monthly site's declining daily-average rate.
Monthly physical page 6 remains unmapped; the new file does not add a label to it.

## 2. Replace src/gacl_pipeline/retrieval.py

Select the complete contents of that inspected file and replace them with this
complete block. Do not append it underneath the old main() function.

```python
"""Extract verified page evidence; keep reviewed notes separate from raw text."""

import argparse
import hashlib
import json
from pathlib import Path

import fitz  # Existing PyMuPDF dependency; no new installation.


# The raw-text extraction method is unchanged from Step 4A.
EXTRACTION_VERSION = "pymupdf-page-text-sort-v1"


def _positive_integer(value: object) -> bool:
    """Return whether value is an integer above zero, excluding bool."""
    return type(value) is int and value > 0


def _read_inputs(root: Path) -> tuple[Path, list[dict], dict]:
    """Read approved sources and validate this lesson's retrieval settings.

    Parameters:
        root: Repository directory containing the two configuration files.
    Returns:
        Resolved directory, source dictionaries and retrieval settings.
    Raises:
        OSError or ValueError for unreadable JSON or invalid settings.
    """
    project_root = Path(root).resolve()
    manifest = json.loads(
        (project_root / "config" / "sources.json").read_text(encoding="utf-8")
    )
    settings = json.loads(
        (project_root / "config" / "retrieval.json").read_text(encoding="utf-8")
    )
    sources = manifest["sources"]  # Existing, approved source-register layout.
    source_by_id = {source["source_id"]: source for source in sources}
    if not sources or len(source_by_id) != len(sources):
        raise ValueError("The source register must have unique source IDs.")

    # Reject bool here too: True == 1 in Python, but it is not a schema version.
    if type(settings.get("schema_version")) is not int or settings["schema_version"] != 1:
        raise ValueError("Unsupported retrieval schema_version; expected 1.")
    if not _positive_integer(settings.get("min_alnum_chars")):
        raise ValueError("min_alnum_chars must be a positive integer.")
    reviews = settings.get("reviewed_pages")
    if not isinstance(reviews, list):
        raise ValueError("reviewed_pages must be a list.")

    # Check every review, even when the command selects a different source.
    seen = set()
    for review in reviews:
        if not isinstance(review, dict):
            raise ValueError("Each reviewed-page entry must be an object.")
        source_id = review.get("source_id")
        if not isinstance(source_id, str) or source_id not in source_by_id:
            raise ValueError("A reviewed page names an unknown source.")
        if review.get("document_sha256") != source_by_id[source_id]["sha256"]:
            raise ValueError("Reviewed-note document hash does not match the register.")
        if not _positive_integer(review.get("pdf_page")):
            raise ValueError("A reviewed PDF page must be a positive integer.")
        printed = review.get("printed_page")
        if printed is not None and not _positive_integer(printed):
            raise ValueError("A reviewed printed page must be positive or null.")
        note = review.get("reviewed_note")
        if not isinstance(note, str) or not note.strip():
            raise ValueError("A reviewed note must contain text.")
        key = (source_id, review["pdf_page"])
        if key in seen:
            raise ValueError("Duplicate reviewed-page entry.")
        seen.add(key)
    return project_root, sources, settings


def _page_metadata(source: dict, settings: dict, page_count: int) -> dict:
    """Combine explicit page labels and reviews, rejecting conflicts.

    Parameters:
        source: Approved source entry; settings: validated retrieval settings.
        page_count: Actual physical page count of the verified PDF.
    Returns:
        Physical-page keys mapped to printed labels and separate notes.
        Every returned key identifies a required page during batch extraction.
    """
    metadata = {}
    for mapping in source.get("pages", []):
        pdf_page = mapping["pdf_page"]
        printed = mapping["printed_page"]
        if not _positive_integer(pdf_page):
            raise ValueError("A configured PDF page must be a positive integer.")
        if printed is not None and not _positive_integer(printed):
            raise ValueError("A configured printed page must be positive or null.")
        if pdf_page in metadata:
            raise ValueError("Duplicate source page mapping.")
        metadata[pdf_page] = {"printed_page": printed, "reviewed_note": None}

    for review in settings["reviewed_pages"]:
        if review["source_id"] != source["source_id"]:
            continue
        pdf_page = review["pdf_page"]
        entry = metadata.setdefault(
            pdf_page, {"printed_page": None, "reviewed_note": None}
        )
        reviewed_label = review.get("printed_page")
        existing_label = entry["printed_page"]
        if existing_label is not None and reviewed_label is not None:
            if existing_label != reviewed_label:
                raise ValueError("Conflicting printed-page mappings.")
        if reviewed_label is not None:
            entry["printed_page"] = reviewed_label
        entry["reviewed_note"] = review["reviewed_note"]

    # A configured reference outside the actual document is a failure, not a skip.
    if any(pdf_page > page_count for pdf_page in metadata):
        raise ValueError("A required page is outside the PDF page range.")
    return metadata


def _extract_document(
    root: Path, source: dict, settings: dict, pdf_page: int | None = None
) -> dict:
    """Verify/open one PDF once and collect all pages or one requested page.

    Parameters:
        root: Resolved repository path; source: selected approved source.
        settings: Validated settings; pdf_page: one-based selection or None.
    Returns:
        A document result with page records and explicit skipped-page reasons.
    """
    pdf_path = root / "data" / "raw" / f"{source['source_id']}.pdf"
    pdf_bytes = pdf_path.read_bytes()
    document_hash = hashlib.sha256(pdf_bytes).hexdigest()
    if document_hash != source["sha256"]:
        raise ValueError("PDF checksum mismatch. Stop and review the source.")

    records = []
    skipped = []
    with fitz.open(stream=pdf_bytes, filetype="pdf") as document:
        if document.needs_pass:
            raise ValueError("Encrypted PDFs are not supported.")
        page_count = len(document)
        metadata = _page_metadata(source, settings, page_count)
        if pdf_page is not None and pdf_page > page_count:
            raise ValueError(f"This PDF has only {page_count} pages.")
        selected = [pdf_page] if pdf_page is not None else range(1, page_count + 1)

        for number in selected:
            # Convert the human page address only at the library boundary.
            text = document.load_page(number - 1).get_text("text", sort=True)
            alnum_count = sum(character.isalnum() for character in text)
            if alnum_count < settings["min_alnum_chars"]:
                if pdf_page is not None or number in metadata:
                    raise ValueError(f"PDF page {number} has insufficient embedded text.")
                skipped.append({
                    "pdf_page": number,
                    "reason": "insufficient_embedded_text_no_ocr",
                    "alnum_chars": alnum_count,
                })
                continue

            # Unknown labels/notes remain None; never derive a printed-page offset.
            details = metadata.get(number, {})
            records.append({
                "source_id": source["source_id"],
                "document_sha256": document_hash,
                "source_url": source["url"],
                "reporting_scope": source["reporting_scope"],
                "pdf_page": number,
                "printed_page": details.get("printed_page"),
                "page_count": page_count,
                "text": text,  # Preserve the exact string, including whitespace.
                "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                "reviewed_note": details.get("reviewed_note"),
                "section": None,  # Heading detection is not implemented.
                "extraction_version": EXTRACTION_VERSION,
                "pymupdf_version": fitz.VersionBind,
                "citation_url": source["url"] + f"#page={number}",
            })

    return {
        "source_id": source["source_id"],
        "document_sha256": document_hash,
        "page_count": page_count,
        "usable_pages": len(records),
        "skipped_pages": skipped,
        "pages": records,
    }


def extract_page(root: Path, source_id: str, pdf_page: int) -> dict:
    """Return one evidence record; retain the Step 4A calling interface.

    Parameters:
        root: Repository path; source_id: approved ID; pdf_page: physical page.
    Returns:
        Exact extracted text with version, page, scope and separate review data.
    Raises:
        OSError or ValueError for missing inputs, invalid selection or evidence.
    """
    if not _positive_integer(pdf_page):
        raise ValueError("PDF page must be a positive integer.")
    project_root, sources, settings = _read_inputs(root)
    source = next((item for item in sources if item["source_id"] == source_id), None)
    if source is None:
        raise ValueError(f"Unknown source ID: {source_id}")
    return _extract_document(project_root, source, settings, pdf_page)["pages"][0]


def extract_documents(root: Path, source_id: str | None = None) -> dict:
    """Return usable pages from all approved sources or one selected source.

    Parameters:
        root: Repository directory; source_id: optional approved-source filter.
    Returns:
        Aggregate counts and document results, including pages and skip lists.
        Nothing is written to disk or returned partially after an error.
    """
    project_root, sources, settings = _read_inputs(root)
    selected = [item for item in sources if source_id is None or item["source_id"] == source_id]
    if not selected:
        raise ValueError(f"Unknown source ID: {source_id}")
    documents = [_extract_document(project_root, item, settings) for item in selected]
    return {
        "source_count": len(documents),
        "physical_pages": sum(item["page_count"] for item in documents),
        "usable_pages": sum(item["usable_pages"] for item in documents),
        "skipped_page_count": sum(len(item["skipped_pages"]) for item in documents),
        "documents": documents,
    }


def main() -> None:
    """Parse page/batch selections and display JSON; summary omits page text."""
    parser = argparse.ArgumentParser(description="Extract verified PDF-page evidence.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository directory.")
    parser.add_argument("--source", help="Approved source ID; optional for all pages.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--page", type=int, help="One-based physical PDF page.")
    mode.add_argument("--all-pages", action="store_true", help="Read all usable pages.")
    parser.add_argument("--summary", action="store_true", help="Omit pages from batch JSON.")
    arguments = parser.parse_args()
    if arguments.page is not None and not arguments.source:
        parser.error("--page requires --source.")
    if arguments.summary and not arguments.all_pages:
        parser.error("--summary requires --all-pages.")

    try:
        if arguments.all_pages:
            evidence = extract_documents(arguments.root, arguments.source)
            if arguments.summary:
                # Build display dictionaries without altering canonical page records.
                evidence["documents"] = [
                    {key: value for key, value in item.items() if key != "pages"}
                    for item in evidence["documents"]
                ]
        else:
            evidence = extract_page(arguments.root, arguments.source, arguments.page)
    except (OSError, ValueError) as error:
        parser.exit(status=1, message=f"Error: {error}\n")
    print(json.dumps(evidence, indent=2, ensure_ascii=False))


# Imports expose functions; only direct module execution runs the CLI.
if __name__ == "__main__":
    main()
```

### Understand the functions before running

| Function | Responsibility |
|---|---|
| _positive_integer | Reusable input rule; bool is rejected even though Python treats it as an int subclass |
| _read_inputs | Reads JSON once per public call; rejects unsupported settings, unknown/stale/duplicate reviews |
| _page_metadata | Combines explicit mappings; rejects conflicting labels and references beyond document length |
| _extract_document | Reads and hashes the same bytes it parses; opens one PDF once; keeps pages or records skips |
| extract_page | Preserves the callable single-page interface |
| extract_documents | Collects one or both approved PDFs and totals their page counts |
| main | Validates terminal options and converts returned Python dictionaries to display JSON |

The underscore prefix convention marks helpers as internal; it does not enforce
access control. Public functions are intended for later callers and tests.
No application class is needed for this responsibility.

`str | None` means a source filter may be a string or absent. `list[dict]` is
a list of dictionary records. Type hints aid readers; they do not replace the
runtime checks. A set stores seen review keys to catch duplicate entries.
The list/dictionary comprehensions build collections; sum adds page counts.
`next(..., None)` selects a matching approved source, returning None if absent.

The minimum-character rule is applied to text alone, before consulting a note.
A long review cannot rescue an unreadable page. A missing or unreadable required
page fails extraction; an optional unreadable page has an explicit skip reason.
An exception stops the batch before a result is returned. This is not an atomic
index build: no index exists yet and no output artifact is written.

Page SHA-256 hashes still describe only the exact extracted UTF-8 text.
Changing a reviewed note will not change text_sha256. Later chunk/index identity
must also account for configuration and metadata changes; text hashes alone
are insufficient for that purpose. That storage work comes in Steps 5–6.

This lesson uses the existing trusted source-register structure. It is not a
general JSON-schema validator or a parser for arbitrary external manifests.
sort=True helps text reading order, not table reconstruction or OCR. The two
approved cached PDFs are the only actual documents this lesson accepts.

## 3. Create tests/test_retrieval.py

These are small, synthetic PDF fixtures created in a temporary folder. They
are software-test evidence, not additional GACL reports or measurements.
They do not read your cached PDFs, warehouse or network. Real-source checks
follow the tests and answer a different question.

```python
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
```

The class groups related tests; unittest creates a fresh fixture with setUp for
each test method. self stores that test's paths and dictionaries. TemporaryDirectory
is removed via addCleanup, including after failures. assertEqual checks an exact
expected value; assertRaisesRegex checks both the exception and useful wording.
subTest labels several input variations inside one test method; these are not
separate entries in unittest's headline test count. patch replaces terminal
arguments temporarily; redirect_stdout captures JSON for inspection.

Thirteen new test methods are supplied. They exercise evidence preservation and
failure boundaries; they do not establish real-source page coverage. The existing
32 tests continue to protect Phase 1. Actual run results remain to be reviewed.

## 4. Run focused tests, then regression tests

Save all three files first. Run from the repository root:

```powershell
# Only the new file: fast feedback on this lesson.
.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_retrieval.py" -v

# All tests, including the unchanged Phase 1 suite.
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Expected with the unchanged baseline: 13 focused tests and 45 total tests, all
passing without skips. This is a target to verify, not a recorded successful run.
If a test fails, share the traceback and stop before treating later checks as a
completed gate. Do not delete a test or change a source hash just to make it pass.

## 5. Run the real PDFs and review the page evidence

```powershell
# Existing one-page command remains valid.
.\.venv\Scripts\python.exe -m gacl_pipeline.retrieval --source gacl_dahej_plot3_ec_2025_h1 --page 5

# Unknown printed label must still be null.
.\.venv\Scripts\python.exe -m gacl_pipeline.retrieval --source gacl_dahej_plot3_ec_2025_h1 --page 6

# Inspect the two version-pinned reviews separately from text.
.\.venv\Scripts\python.exe -m gacl_pipeline.retrieval --source gacl_brsr_2025_26 --page 1
.\.venv\Scripts\python.exe -m gacl_pipeline.retrieval --source gacl_brsr_2025_26 --page 37

# Read both approved PDFs; display counts/skip reasons rather than all page text.
.\.venv\Scripts\python.exe -m gacl_pipeline.retrieval --all-pages --summary
```

The summary still performs extraction; it only removes the page bodies from the
display. Omitting --summary displays the complete batch, which is unnecessary
for this checkpoint. Do not commit full extracted passages or terminal dumps.

Expected reference counts, subject to the learner's actual run:

| Source | Physical pages | Usable pages | Skipped pages |
|---|---:|---:|---|
| Monthly Dahej Plot 3 | 21 | 20 | Physical page 1, insufficient embedded text |
| Annual BRSR | 50 | 50 | None |
| Total | 71 | 70 | 1 |

Verify the actual summary, including hashes, per-document counts and skip reason.
If counts differ, investigate the page and threshold rather than hard-coding 70.
Review page 5's six freshwater rows and KL/day context. Its raw text hash should
remain 1975b4bd411905133835f961efe30c7ffbfb600bfe37390e783306943ba6abd8
with the same PDF, PyMuPDF version and extraction method as the reported 4A run.
Page 6 should still have printed_page=null and reviewed_note=null.
Annual page 1 should have printed_page=43; page 37 should have printed_page=79.
Both should display a reviewed_note separately from text. Compare those notes
with the actual PDF pages, rather than interpreting test success as source review.

Finally confirm original numerical extraction and Git scope:

```powershell
# Checks cached PDF versions and the 18 numerical facts; no download/cloud upload.
.\.venv\Scripts\python.exe -m gacl_pipeline --offline

# Generated local outputs should remain ignored.
git status --short --branch
git diff --stat
```

Expected core output: success, cached_pdfs, pdfs_verified_this_run=true,
18 extracted/loaded/stored and four passing dataset checks. These are not the
same counts as page records or unittest tests. No BigQuery/dbt rerun is needed
because their code and inputs have not changed.

Expected new application paths are exactly config/retrieval.json,
src/gacl_pipeline/retrieval.py and tests/test_retrieval.py. On the last verified
branch all three will be untracked. git diff --stat does not show untracked-file
contents; use status and file inspection. The previous inspector remains intact.

## Optional compact display for the remaining real-page checks

If the earlier page commands have already run, share only their requested
metadata fields. Otherwise this read-only PowerShell block calls the existing
extract_page function for the same four pages and displays compact JSON.
It creates no script or output artifact, performs no download and does not
change the implementation. Run from the repository root.

```powershell
@'
"""Display selected page metadata without changing project files."""

import json
from pathlib import Path
from gacl_pipeline.retrieval import extract_page

# Use the current repository folder and the four existing reference pages.
root = Path.cwd()
pages_to_check = [
    ("gacl_dahej_plot3_ec_2025_h1", 5),
    ("gacl_dahej_plot3_ec_2025_h1", 6),
    ("gacl_brsr_2025_26", 1),
    ("gacl_brsr_2025_26", 37),
]

# Display only the fields needed for this checkpoint, excluding raw page text.
fields = ("source_id", "pdf_page", "printed_page", "text_sha256", "reviewed_note")
for source_id, pdf_page in pages_to_check:
    evidence = extract_page(root, source_id, pdf_page)
    summary = {field: evidence[field] for field in fields}
    print(json.dumps(summary, indent=2, ensure_ascii=False))
'@ | .\.venv\Scripts\python.exe -
```

root is the current repository path. pages_to_check is a list of source/page
pairs. fields chooses which returned values to display. Each loop iteration
verifies and reads one selected source page, then constructs summary from its
metadata. The actual raw text is neither changed nor printed here.

Check monthly page 5 against the recorded 4A text hash above; page 6 should
retain printed_page=null and reviewed_note=null. Annual pages 1 and 37 should
show printed labels 43 and 79 and the separate review notes. Open those annual
PDF pages and state whether the notes agree with the visible report. Printed
labels in JSON alone do not establish that visual comparison.

## Review and local checkpoint

The author has now supplied passing software tests, batch/core results and the
four detailed page records. The earlier temporary hold on committing can end:
save the verified implementation in a local checkpoint while retaining the
remaining visual-review confirmation explicitly.

In GitHub Desktop, keep exactly these three files selected: config/retrieval.json,
src/gacl_pipeline/retrieval.py and tests/test_retrieval.py. Enter this summary:

```text
feat: add verified PDF page evidence extraction
```

Click Commit 3 files to feature/phase2-guided. A local commit saves a version on
the laptop; it does not publish the feature branch or merge code into public main.
The screenshot's CRLF/LF notice is normal text normalization, not a PDF change.

After committing, share:

```powershell
git status --short --branch
git log -1 --oneline
```

Expected: clean feature/phase2-guided and a new commit carrying the chosen message.
The hash cannot be predicted; record the actual output. Do not pull/merge newer
documentation into unexplained changes. Synchronization will use the inspected
branch state after the local checkpoint.

Also confirm whether the separate notes agree with annual physical pages 1 and
37 in the actual PDF. Outputting a configured note does not establish this
comparison. If any source discrepancy appears, record it and correct the note
in a subsequent reviewed change before Step 5. Full PDF text dumps are unnecessary.

In your own words explain: why can a reviewed note not count as extracted text,
and why do we fail on an unreadable required page while recording an optional
unreadable page as skipped? Also distinguish 18 observations, 70 expected usable
pages and 45 expected software tests.

After results are reviewed, finish the Step 4 commit and documentation merge
using the actual branch state. Step 5 then introduces exact-span chunks and
overlap. No chunker, search index or model is introduced by this lesson.

References: [PyMuPDF page API](https://pymupdf.readthedocs.io/en/latest/page.html),
[document API](https://pymupdf.readthedocs.io/en/latest/document.html),
[Python unittest](https://docs.python.org/3.11/library/unittest.html),
[argparse](https://docs.python.org/3.11/library/argparse.html),
[tempfile](https://docs.python.org/3.11/library/tempfile.html).
