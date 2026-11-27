# Phase 2 — Step 5: Exact-span chunking with overlap

Build-order version: 1.0. Prepared: 27 November 2026 (India).
Prerequisite: Step 4 software, source evidence and Git checkpoints passed.
The author has now confirmed that both annual review notes match the visible
PDF pages. This closes the Step 4 source-review gate; the independent explanation
of concepts remains a learning reflection, not an invented answer.
Status: Step 5 instructions prepared; implementation and execution pending.

## Purpose and ELI5

We have canonical evidence records for 70 usable pages from two approved PDFs.
Each page retains its original extracted text, source/version, page address and
separate reviewed note. Now split a long page into smaller passages called chunks.

ELI5: cut a long reading sheet into overlapping reading cards. Number each card
with the book, page and where its words began and ended. Keep the reviewer's
sticky note separate from the copied words.

Why: a later search can retrieve a manageable passage, and a later model can
receive relevant passages instead of the entire report. Chunking itself does
not search, summarise, understand a table or generate an answer. This lesson
creates in-memory records; index storage is Step 6.

We start with a maximum of 1,800 characters and a target overlap of 250.
Prefer newline boundaries when available. Keep every chunk within one page.
Do not split on guessed subject categories or infer years/units from a whole page.

## What is a character offset?

Python string positions begin at zero. start_char is included; end_char is
excluded. For text "abcdefghijklmnopqrst", maximum 10 and overlap 3:

| Chunk | start_char | end_char | Exact text |
|---|---:|---:|---|
| 1 | 0 | 10 | abcdefghij |
| 2 | 7 | 17 | hijklmnopq |
| 3 | 14 | 20 | opqrst |

The first two chunks share "hij"; the next two share "opq".
The round-trip rule is: chunk text equals page text sliced from start_char up
to, but not including, end_char. We never strip, rewrite or join lines.

Offsets count Python Unicode string characters, not UTF-8 bytes, displayed
glyph widths or model tokens. A model's token limit is a separate constraint
to assess when choosing the model. Characters are our current transparent rule.

Overlap protects some boundary context, but cannot guarantee that every table
row includes its header, year or unit. Smaller context and answer quality will
need evaluation later. We keep full parent pages available for reference.

## Starting point, installations and exact edits

The inspected published branch is feature/phase2-guided at 53b9be4. It retains
the implementation commit 29795de and the completed documentation merge.
The assistant read the actual module, configuration and tests before preparing
these insertion instructions. No application file was edited by the assistant.

No new installation: reuse Python 3.11+, PyMuPDF 1.26.6 and the standard library.
No model, API key, cloud call, vector store or new source is introduced.

Work from D:\gacl-public-disclosure-pipeline and stay on feature/phase2-guided.
Read the lesson online; batch newer documentation synchronization at the next
implementation checkpoint rather than merging after every documentation update.

```powershell
git status --short --branch
git log -1 --oneline
```

Expected starting point: clean feature/phase2-guided, last verified at 53b9be4.
If your files have changed since the reviewed version, keep them and share the
difference before replacing the specified sections. Do not reset your work.

Only these three existing tracked files change:

| File | Edits |
|---|---|
| config/retrieval.json | Add two chunk settings; preserve reviewed notes |
| src/gacl_pipeline/retrieval.py | Add one version constant and four functions; replace only main |
| tests/test_retrieval.py | Extend imports/fixture; add 15 focused tests |

Do not create another module, duplicate main, remove existing tests or modify
config/sources.json. The inspector and original numerical pipeline stay intact.

## 1. Add two configuration settings

In config/retrieval.json, immediately after the existing min_alnum_chars line,
insert these two lines at the same indentation:

```text
    "max_chunk_chars": 1800,
    "overlap_chars": 250,
```

Leave schema_version, min_alnum_chars and reviewed_pages unchanged.
These are insertions inside the existing JSON object, not a complete JSON file.
Keep the commas. JSON has no comment syntax.

max_chunk_chars sets an upper bound, while overlap_chars is a target shared
suffix/prefix length. Reject bool, noninteger or nonpositive maxima; overlap
must be an integer from zero to maximum minus one. Equality would allow an
unmoving window and must fail. Large valid overlaps are also less efficient.

Schema version 1 remains compatible with existing page extraction. Step 4 calls
do not need these new settings. The new extract_chunks function requires and
validates them before reading PDFs. No silent defaults hide a missing key.

## 2. Add the chunking-version constant

Open src/gacl_pipeline/retrieval.py. Directly below the existing
EXTRACTION_VERSION assignment, add:

```python
# Bump this identifier when chunk-boundary or identity rules change.
CHUNKING_VERSION = "line-window-v1"
```

Keep EXTRACTION_VERSION unchanged: we are not changing how PDF text is read.
Chunking has its own version because its boundary rules are a separate method.

## 3. Insert four functions before main

Find def main() near the bottom of retrieval.py. Insert this complete block
immediately above it, at the left margin. Leave all earlier Step 4 functions
unchanged.

```python
def _validate_chunk_settings(max_chunk_chars: int, overlap_chars: int) -> None:
    """Reject invalid character-window settings before chunking.

    Parameters:
        max_chunk_chars: Positive maximum number of Python string characters.
        overlap_chars: Nonnegative target overlap, smaller than the maximum.
    Returns:
        None. Invalid values raise ValueError; bool is not accepted as int.
    """
    if not _positive_integer(max_chunk_chars):
        raise ValueError("max_chunk_chars must be a positive integer.")
    if type(overlap_chars) is not int or not 0 <= overlap_chars < max_chunk_chars:
        raise ValueError("overlap_chars must be an integer from 0 to max_chunk_chars - 1.")


def chunk_text(text: str, max_chunk_chars: int, overlap_chars: int) -> list[dict]:
    """Split one string into exact, overlapping spans without rewriting it.

    Parameters:
        text: Exact extracted text from one page.
        max_chunk_chars: Maximum characters per span.
        overlap_chars: Target shared characters between neighbouring spans.
    Returns:
        Dictionaries with start_char, exclusive end_char and exact text slices.
        An empty input string returns an empty list.
    """
    _validate_chunk_settings(max_chunk_chars, overlap_chars)
    if not isinstance(text, str):
        raise ValueError("Chunk text must be a string.")

    spans = []
    start = 0
    while start < len(text):
        limit = min(start + max_chunk_chars, len(text))
        end = limit

        # Prefer a newline in the latter part of a nonfinal window.
        # Looking past the overlap also prevents reusing the previous end.
        if limit < len(text):
            minimum = max(overlap_chars + 1, max_chunk_chars // 2)
            newline = text.rfind("\n", start + minimum, limit)
            if newline != -1:
                end = newline + 1  # Preserve the newline inside the exact slice.

        spans.append({
            "start_char": start,
            "end_char": end,
            "text": text[start:end],
        })
        if end == len(text):
            break  # Do not create an unnecessary trailing overlap-only chunk.

        next_start = end - overlap_chars
        if overlap_chars:
            # Prefer beginning after a newline within the proposed overlap.
            # Exclude the final newline so this does not collapse overlap to zero.
            newline = text.find("\n", next_start, end - 1)
            if newline != -1:
                next_start = newline + 1

        # The boundary rules above guarantee start < next_start <= end.
        start = next_start
    return spans


def chunk_page(page: dict, max_chunk_chars: int, overlap_chars: int) -> list[dict]:
    """Attach provenance and deterministic IDs to spans of one verified page.

    Parameters:
        page: A complete evidence record returned by extract_page/document helpers.
        max_chunk_chars: Maximum characters per chunk.
        overlap_chars: Target overlap before optional newline alignment.
    Returns:
        Chunk dictionaries whose text round-trips to the original page offsets.
        The input page dictionary is not modified.
    """
    text = page["text"]
    if not isinstance(text, str):
        raise ValueError("Page text must be a string.")
    actual_text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if actual_text_hash != page["text_sha256"]:
        raise ValueError("Page text SHA-256 mismatch.")

    # Copy explicit provenance fields; do not infer years, units or headings.
    metadata_keys = (
        "source_id", "document_sha256", "source_url", "reporting_scope",
        "pdf_page", "printed_page", "page_count", "reviewed_note", "section",
        "extraction_version", "pymupdf_version", "citation_url",
    )
    chunks = []
    for span in chunk_text(text, max_chunk_chars, overlap_chars):
        chunk = {key: page[key] for key in metadata_keys}
        chunk.update({
            "page_text_sha256": page["text_sha256"],
            "start_char": span["start_char"],
            "end_char": span["end_char"],
            "text": span["text"],
            "text_sha256": hashlib.sha256(span["text"].encode("utf-8")).hexdigest(),
            "chunking_version": CHUNKING_VERSION,
            "max_chunk_chars": max_chunk_chars,
            "overlap_chars": overlap_chars,
        })

        # Canonical JSON gives the same bytes for the same values/key contents.
        # Include metadata, offsets, versions and parameters in identity.
        identity = json.dumps(
            chunk, sort_keys=True, ensure_ascii=False, separators=(",", ":")
        )
        chunk["chunk_id"] = hashlib.sha256(identity.encode("utf-8")).hexdigest()
        chunks.append(chunk)
    return chunks


def extract_chunks(root: Path, source_id: str | None = None) -> dict:
    """Verify selected PDFs, extract their pages and collect in-memory chunks.

    Parameters:
        root: Repository directory containing configuration and cached PDFs.
        source_id: Optional approved-source filter; None selects both sources.
    Returns:
        Source/page/chunk counts and document results with pages and chunks.
        No index, file, database, model request or network call is created.
    """
    project_root, sources, settings = _read_inputs(root)
    max_chunk_chars = settings.get("max_chunk_chars")
    overlap_chars = settings.get("overlap_chars")
    _validate_chunk_settings(max_chunk_chars, overlap_chars)

    selected = [
        source for source in sources
        if source_id is None or source["source_id"] == source_id
    ]
    if not selected:
        raise ValueError(f"Unknown source ID: {source_id}")

    documents = []
    for source in selected:
        # Reuse Step 4B: read/hash/open each selected PDF once in this batch.
        document = _extract_document(project_root, source, settings)
        chunks = []
        for page in document["pages"]:
            chunks.extend(chunk_page(page, max_chunk_chars, overlap_chars))
        document["chunks"] = chunks
        document["chunk_count"] = len(chunks)
        documents.append(document)

    return {
        "source_count": len(documents),
        "physical_pages": sum(item["page_count"] for item in documents),
        "usable_pages": sum(item["usable_pages"] for item in documents),
        "skipped_page_count": sum(len(item["skipped_pages"]) for item in documents),
        "chunk_count": sum(item["chunk_count"] for item in documents),
        "chunking_version": CHUNKING_VERSION,
        "max_chunk_chars": max_chunk_chars,
        "overlap_chars": overlap_chars,
        "documents": documents,
    }
```

### What each function does

| Function | Inputs | Output / responsibility |
|---|---|---|
| _validate_chunk_settings | Maximum and overlap | Raises ValueError for invalid window settings |
| chunk_text | One string and window settings | Exact text spans with character offsets |
| chunk_page | One complete page record and settings | Spans with source metadata, hashes and stable chunk IDs |
| extract_chunks | Repository path and optional source ID | Verified pages/chunks with aggregate and per-document counts |

No new application class is needed. The underscore convention marks an internal
helper; it is not an access-control mechanism.

spans stores small text/offset dictionaries. metadata_keys lists the parent fields
to preserve. identity is the serialized string used for hashing. append adds one
record to a list; extend adds every record from another list. documents groups
results by report, and sum adds the per-document counts.

start is the current window's first character. limit is its maximum allowed end.
end may move backwards to a newline in the latter part of a nonfinal window.
minimum keeps that end past the overlap as well as the midpoint, preventing a
repeated boundary. next_start begins near end minus the target overlap.
An optional newline alignment can move it forward, reducing actual overlap.

If no suitable newline exists, use the bounded character window. A very long
line can therefore be split midword; this is character/line chunking, not
sentence-aware or semantic chunking. A final short chunk is valid. Empty text
returns no spans; nonempty whitespace is preserved by the pure function.
Actual unusable PDF pages are filtered earlier by Step 4.

The loop must advance and terminate. A next start stays beyond the old start
and no later than the old end. Each next end adds new characters. This ensures
no gaps, bounded size and no overlap-only final record.

chunk_page assumes the complete page schema from Step 4, checks its text hash
and creates new dictionaries. It does not mutate the input or re-open its PDF.
extract_chunks provides the actual PDF verification route. A matching page text
hash alone is not independent proof that arbitrary caller-supplied data came
from an approved PDF.

### Three hashes and one deterministic identity

| Field | Describes |
|---|---|
| document_sha256 | Original verified PDF bytes |
| page_text_sha256 | Parent page's complete extracted text |
| text_sha256 in a chunk | Only that chunk's exact text |
| chunk_id | Canonically serialized chunk content, offsets, provenance, versions, settings and review metadata |

sort_keys=True gives a fixed key order. separators removes optional JSON spaces.
ensure_ascii=False keeps Unicode characters in the serialized text. Encoding that
string as UTF-8 produces the bytes passed to SHA-256. The chunk_id is added after
hashing to avoid trying to include itself in its own identity.

The same page, metadata, settings and method versions give the same IDs.
Changing a reviewed note can change chunk IDs while leaving raw text hashes
unchanged. Repeated text at different offsets has different identity.
IDs are identifiers, not ranking scores, confidence values or security signatures.
Full configuration/index freshness fingerprints are additional Step 6 work.

Reviewed notes are copied into their own field; they are never appended to
chunk text. A note describes a parent-page review, not necessarily something
supported by every small chunk. A later answer must inspect the appropriate
evidence rather than assume that sharing a page proves a claim.

## 4. Replace only main()

In retrieval.py replace the existing def main() function, from its definition
through its final print statement, with this block. Keep the existing bottom
comment and if __name__ == "__main__": main() guard, once.

```python
def main() -> None:
    """Display page, all-page or chunk results; summary omits long text bodies."""
    parser = argparse.ArgumentParser(description="Extract verified PDF-page evidence.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository directory.")
    parser.add_argument("--source", help="Approved source ID; optional for batch modes.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--page", type=int, help="One-based physical PDF page.")
    mode.add_argument("--all-pages", action="store_true", help="Read all usable pages.")
    mode.add_argument("--chunks", action="store_true", help="Read and chunk usable pages.")
    parser.add_argument("--summary", action="store_true", help="Omit batch page/chunk bodies.")
    arguments = parser.parse_args()
    if arguments.page is not None and not arguments.source:
        parser.error("--page requires --source.")
    if arguments.summary and arguments.page is not None:
        parser.error("--summary requires --all-pages or --chunks.")

    try:
        if arguments.chunks:
            evidence = extract_chunks(arguments.root, arguments.source)
        elif arguments.all_pages:
            evidence = extract_documents(arguments.root, arguments.source)
        else:
            evidence = extract_page(arguments.root, arguments.source, arguments.page)

        if arguments.summary:
            # Keep counts/skip reasons while omitting page and chunk text records.
            evidence["documents"] = [
                {
                    key: value for key, value in item.items()
                    if key not in {"pages", "chunks"}
                }
                for item in evidence["documents"]
            ]
    except (OSError, ValueError) as error:
        parser.exit(status=1, message=f"Error: {error}\n")
    print(json.dumps(evidence, indent=2, ensure_ascii=False))
```

The mutually exclusive argument group now accepts exactly one of --page,
--all-pages or --chunks. --source is required for one page and optional for
batch modes. --summary works with either batch mode, omitting pages/chunks
from display while keeping counts. Extraction still happens in full.

Existing page/all-page commands stay valid. A --chunks command returns both
canonical parent pages and their chunks in memory. Summary display omits their
long bodies; it does not create a stored index or call a model.

## 5. Extend the test imports and existing fixture

Open tests/test_retrieval.py. Replace its current single-line import from
gacl_pipeline.retrieval with:

```python
from gacl_pipeline.retrieval import (
    chunk_page,
    chunk_text,
    extract_chunks,
    extract_documents,
    extract_page,
    main,
)
```

Inside PageEvidenceTests.setUp(), find self.settings. Immediately after its
min_alnum_chars entry, insert:

```text
            "max_chunk_chars": 1800,
            "overlap_chars": 250,
```

This changes only synthetic test configuration. Keep the existing source/PDF
fixture and all 13 Step 4B tests unchanged.

## 6. Add three integration tests inside PageEvidenceTests

Insert these methods after the existing test_existing_page_cli_and_batch_summary
method and before the class ends. Keep the four-space indentation shown.
They belong inside PageEvidenceTests and use that class's existing setUp.

```python
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
```

The first test connects chunks back to fixture pages. The second tests the new
CLI summary while existing tests protect the earlier command. The third removes
the fixture PDF after making the settings invalid, proving validation happens
before a PDF read: ValueError must appear before a missing-file OSError.

## 7. Add a new test class below PageEvidenceTests

After the preceding methods, insert this new class at the left margin, before
the file's final if __name__ == "__main__": unittest.main() guard.
Do not put ChunkSpanTests inside PageEvidenceTests. Keep the bottom guard once.

```python
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
```

self still means the current test object. make_page creates synthetic metadata
for string-level tests; it is not a real GACL observation or report.
assert_coverage checks useful invariants across every span: exact slicing,
bounded length, no gap and progress to the final character. zip pairs adjacent
spans for the progress check. The tests do not rely on arbitrary chunk-ID strings.

These 12 string/identity tests plus the three integration tests add 15 methods.
Expected focused total: 28 (13 existing retrieval plus 15 new).
Expected complete suite: 60 (45 previous plus 15 new).
The counts are expected results, not claims that the new code has run.

## 8. Run focused and full software tests

Save all three files, then run:

```powershell
# New chunk tests plus existing retrieval tests.
.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_retrieval.py" -v

# Full regression suite.
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Expected: 28 focused tests and 60 full-suite tests, all passing without skips.
If a command fails, share the traceback before treating the step as complete.
Do not remove a test to obtain a passing summary.

## 9. Run the real PDFs and inspect chunk coverage

```powershell
# Existing batch mode still works.
.\.venv\Scripts\python.exe -m gacl_pipeline.retrieval --all-pages --summary

# New mode: extract and chunk both approved PDFs, then display counts.
.\.venv\Scripts\python.exe -m gacl_pipeline.retrieval --chunks --summary
```

Expected unchanged coverage: two sources, 71 physical pages, 70 usable pages
and one skipped monthly cover. The new summary should report line-window-v1,
maximum 1800, target overlap 250, total chunk_count and per-document counts.
Record the actual chunk total. It is not fixed in this lesson; boundaries affect
the count. Every usable page has at least one chunk, so it must be at least 70.

Now verify exact spans, full page coverage, inherited metadata and repeatable
IDs using this read-only PowerShell block. It calls the implemented functions;
it creates no script/output file and prints no full report passages.

```powershell
@'
"""Check real-page chunk coverage and stable IDs without writing files."""

import json
from pathlib import Path
from gacl_pipeline.retrieval import extract_chunks

# Read the approved PDFs and chunk the canonical page strings.
root = Path.cwd()
batch = extract_chunks(root)
chunk_ids = []
seen = set()
page_count = 0

for document in batch["documents"]:
    pages = {page["pdf_page"]: page for page in document["pages"]}
    covered_until = {number: 0 for number in pages}
    page_count += len(pages)

    for chunk in document["chunks"]:
        parent = pages[chunk["pdf_page"]]
        start, end = chunk["start_char"], chunk["end_char"]

        # Check exact text, valid offsets, full coverage and bounded length.
        assert 0 <= start < end <= len(parent["text"])
        assert start <= covered_until[chunk["pdf_page"]] < end
        assert chunk["text"] == parent["text"][start:end]
        assert end - start <= batch["max_chunk_chars"]
        assert chunk["page_text_sha256"] == parent["text_sha256"]
        covered_until[chunk["pdf_page"]] = end

        # Preserve source/citation/review metadata without adding it to raw text.
        for field in (
            "source_id", "document_sha256", "reporting_scope",
            "printed_page", "citation_url", "reviewed_note",
        ):
            assert chunk[field] == parent[field]

        assert chunk["chunk_id"] not in seen
        seen.add(chunk["chunk_id"])
        chunk_ids.append(chunk["chunk_id"])

    # Every usable page must be covered right through its last character.
    for number, page in pages.items():
        assert covered_until[number] == len(page["text"])

# Run a second batch against the same verified inputs to check repeatability.
again = extract_chunks(root)
second_ids = [
    chunk["chunk_id"]
    for document in again["documents"]
    for chunk in document["chunks"]
]
assert chunk_ids == second_ids
assert len(chunk_ids) == batch["chunk_count"]

print(json.dumps({
    "covered_pages": page_count,
    "verified_chunks": len(chunk_ids),
    "exact_spans_and_coverage": "passed",
    "stable_ids_across_two_runs": True,
}, indent=2))
'@ | .\.venv\Scripts\python.exe -
```

Expected: covered_pages 70, verified_chunks matching your summary, exact-span
checks passed and stable_ids_across_two_runs true. These checks validate text
handling, not whether an AI answer would be correct. That requires later retrieval
and answer evaluations.

## 10. Confirm original facts and Git scope

```powershell
# Keep original numerical extraction and its checks working.
.\.venv\Scripts\python.exe -m gacl_pipeline --offline

# Inspect which tracked files changed.
git status --short --branch
git diff --stat
git diff --check
```

Expected offline output: success, cached_pdfs, PDFs verified, 18 extracted,
18 loaded, 18 stored and all four dataset checks passed. No BigQuery/dbt or
Power BI rerun is required for this local chunking exercise.

Expected modified tracked paths: config/retrieval.json,
src/gacl_pipeline/retrieval.py and tests/test_retrieval.py.
Generated raw PDFs/databases/outputs stay ignored. git diff --check should
report no whitespace errors. Do not stage unrelated files or full PDF passages.

## Stop and share the results

Share focused/full test summaries, the new real chunk summary, the coverage/ID
verification output, the offline numerical summary and Git status/diff summary.
Share any failure traceback rather than claiming a partial run passed.
Keep the work uncommitted until the implementation and results are reviewed.

For understanding: explain why the end offset is exclusive, why actual overlap
may be below 250, and why a chunk may still lack table context. Distinguish
1,800 characters from model tokens. Show how a chunk's page offsets recover its
exact text and why reviewed notes remain separate.

After review, record the actual Step 5 evidence and create a local checkpoint,
then batch documentation synchronization. Step 6 will persist pages/chunks in
a separate replaceable index. It is not part of the current implementation.

References: [Python string slicing](https://docs.python.org/3.11/tutorial/introduction.html#strings),
[string methods](https://docs.python.org/3.11/library/stdtypes.html#string-methods),
[json](https://docs.python.org/3.11/library/json.html),
[hashlib](https://docs.python.org/3.11/library/hashlib.html),
[unittest](https://docs.python.org/3.11/library/unittest.html).
