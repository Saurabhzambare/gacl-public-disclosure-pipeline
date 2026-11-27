# Phase 2 — Step 6: Build a separate, replaceable SQLite search index

Build-order version: 1.0. Prepared: 27 November 2026 (India).
Prerequisite: Step 5 checks and published-source review passed. The author has
also merged/pushed documentation at 98c14ec, with clean tracking status.
Status: Step 6 instructions prepared; learner implementation/execution pending.
This lesson adds storage and readiness inspection. Keyword retrieval is Step 7.

## Preparation checks versus your execution

The assistant checked the proposed Python syntax and SQL/FTS schema, then ran
the 40 retrieval tests from the lesson's assembled examples in an isolated
Linux/Python 3.12.14 process with PyMuPDF 1.26.6. All 40 passed in 0.392 seconds.
The source was loaded in memory; only temporary synthetic test fixtures were
created and cleaned up. No learner source file or real index was changed.

This checks the examples, not your Windows implementation. Your acceptance
results remain 40 retrieval / 72 full tests plus the real-PDF persistence,
warehouse-preservation and rebuild checks below.

## Purpose and ELI10

Step 5 produces 136 chunks covering 70 usable pages. Those records exist in
memory during the command. A new command currently has to extract them again.
Store the canonical pages/chunks once in a local catalogue, ready for later queries.

ELI10: we made reading cards; now give them a filing cabinet. Keep the original
number ledger in its own cabinet. When rebuilding the card cabinet, prepare a
new cabinet, check it, then swap it into place. If preparation fails, keep the old
one. Put a label on the cabinet saying which books and settings created it.

A search index is stored information organised for efficient retrieval.
This step prepares SQLite FTS5 data; it does not expose a question-search API,
rank answers, invoke a model or change the validated 18 observations.
No BigQuery, dbt, Power BI or cloud work is needed.

## What is new?

| Concept | Meaning here |
|---|---|
| Persistence | Records survive after Python exits |
| Schema | Named database tables, columns, keys and constraints |
| Primary key | A record's unique identifier |
| Foreign key | A relationship that must point to an existing source/page |
| FTS5 | SQLite's full-text indexing extension, preparing word lookup |
| Tokenizer | Rules for turning searchable text into terms |
| Manifest | Build receipt: inputs, versions, counts and UTC timestamp |
| Fingerprint | SHA-256 of consistently serialized input metadata |
| Atomic replacement | Publish the completed file in one filesystem replacement |
| Read-only URI | Open an existing SQLite file without creating/writing it |

The full-text table uses the fixed porter unicode61 tokenizer. It handles text
terms with English stemming; it is a lexical preparation, not embeddings or a
trained model. Search behaviour and BM25 ranking will be introduced/tested in
Step 7. Creating an FTS5 table is not a retrieval-quality evaluation.

## Starting point and installations

The assistant inspected the actual published files on feature/phase2-guided:
implementation 42c9ceb, followed by documentation merge 98c14ec. The latter changes
only Markdown compared with 42c9ceb. The user supplied clean tracking status.
Read this lesson online and keep working on that feature branch; later
documentation synchronization is batched at the next implementation checkpoint.

No new installation. Reuse the existing PyMuPDF and Python 3.11+ environment.
sqlite3, tempfile, os, sys, contextlib and datetime come with Python. The earlier
Windows readiness check already demonstrated FTS5. The new tests also exercise
the actual extension in temporary databases.

Start from D:\gacl-public-disclosure-pipeline:

```powershell
git status --short --branch
git log -1 --oneline
```

Expected: clean feature/phase2-guided at the last verified merge 98c14ec.
Preserve unexpected changes and inspect them before applying these exact edits.

Only three existing tracked files change:

| File | Action |
|---|---|
| .gitignore | Add the generated index directory |
| src/gacl_pipeline/retrieval.py | Add storage helpers; share chunk collection; extend CLI |
| tests/test_retrieval.py | Add imports and 12 index tests inside the existing fixture class |

Reuse the fixed self.settings dictionary from Step 5 unchanged.
config/retrieval.json requires no new setting here. The target path and tokenizer
are explicit code constants for this first storage interface.

## 1. Ignore generated artifacts before creating them

Open the root .gitignore file. Add this on a new line:

```text
data/retrieval/
```

It covers the local SQLite index and temporary build files in that directory.
It does not hide application/configuration/test code. Verify the rule:

```powershell
git check-ignore -v -- data/retrieval/index.sqlite
```

Expected: Git identifies the .gitignore line containing data/retrieval/.
If nothing is printed, check the rule before building the real index.
No database should be committed.

The two separate paths are:

| Purpose | Path |
|---|---|
| Existing authoritative numerical warehouse | data/warehouse/gacl.sqlite |
| New derived text catalogue | data/retrieval/index.sqlite |

The catalogue can be rebuilt from approved cached PDFs and configuration.
The builder has no arbitrary destination-path argument and never opens the
observation warehouse. A focused test checks that an existing warehouse file
remains byte-for-byte unchanged during a catalogue build.

## 2. Extend retrieval.py imports and constants

At the top of src/gacl_pipeline/retrieval.py, replace the standard-library import
block from import argparse through from pathlib import Path with:

```python
import argparse
import hashlib
import json
import os
import sqlite3
import sys
import tempfile
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
```

Keep import fitz beneath those imports. Directly below CHUNKING_VERSION, add:

```python
# Index storage has its own schema, independent of the PDF/chunk method versions.
INDEX_SCHEMA_VERSION = 1
FTS5_TOKENIZER = "porter unicode61"
INDEX_RELATIVE_PATH = Path("data") / "retrieval" / "index.sqlite"
```

Index schema version, text-extraction version and chunking version are separate:
changing stored-table layout is different from changing how PDF text is read or
where it is split. The relative Path constant is resolved against the explicit
repository root, including temporary roots in tests.

## 3. Share the existing chunk-collection implementation

Find the current def extract_chunks(...) function. Replace only that complete
function, ending immediately before def main(), with the following two functions.
Do not remove chunk_text, chunk_page or earlier extraction functions.

```python
def _collect_chunks(
    project_root: Path, sources: list[dict], settings: dict,
    source_id: str | None = None,
) -> dict:
    """Collect chunks from one already-read, consistent configuration snapshot.

    Parameters:
        project_root: Resolved repository path.
        sources/settings: Approved dictionaries read together by _read_inputs.
        source_id: Optional source filter; None selects the complete register.
    Returns:
        The existing Step 5 in-memory batch layout.
    """
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


def extract_chunks(root: Path, source_id: str | None = None) -> dict:
    """Retain the Step 5 public interface; read settings once before collection.

    Parameters:
        root: Repository directory; source_id: optional approved-source filter.
    Returns:
        The unchanged Step 5 in-memory page/chunk batch and counts.
    """
    project_root, sources, settings = _read_inputs(root)
    return _collect_chunks(project_root, sources, settings, source_id)
```

This preserves the public extract_chunks(root, source_id=None) interface and
return layout. Existing Step 5 tests continue to apply.

Why introduce _collect_chunks? An index must record the exact settings used to
create its records. Reading the files once for a manifest and then independently
re-reading them for extraction could mix two configurations if someone edits
the files between those reads. The shared collector uses the captured dictionaries.
The builder checks current configuration again before publishing.

## 4. Add the storage and status helpers before main()

Insert this block after the preceding functions and before main(), at the left
margin. It creates nothing during import; writes occur only when build_index
is called.

```python
def _canonical_json(value: object) -> str:
    """Serialize a JSON-compatible value with fixed key/spacing conventions."""
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _json_sha256(value: object) -> str:
    """Return a fingerprint of canonical JSON encoded as UTF-8."""
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _index_inputs(sources: list[dict], settings: dict) -> dict:
    """Describe the source/settings/runtime versions an index depends on.

    Parameters:
        sources: The complete approved source register.
        settings: Retrieval configuration, including reviewed metadata.
    Returns:
        A JSON-compatible snapshot; formatting-only JSON edits do not change it.
    """
    _validate_chunk_settings(
        settings.get("max_chunk_chars"), settings.get("overlap_chars")
    )
    return {
        "index_schema_version": INDEX_SCHEMA_VERSION,
        "sources": sources,
        "retrieval_settings": settings,
        "extraction_version": EXTRACTION_VERSION,
        "chunking_version": CHUNKING_VERSION,
        "pymupdf_version": fitz.VersionBind,
        "python_version": sys.version.split()[0],
        "sqlite_version": sqlite3.sqlite_version,
        "fts_tokenizer": FTS5_TOKENIZER,
    }


def _write_index_database(
    connection: sqlite3.Connection, batch: dict, manifest: dict
) -> None:
    """Create/populate tables on the temporary connection supplied by the builder.

    Parameters:
        connection: New temporary database; never the observation warehouse.
        batch: Verified Step 5 pages/chunks for the complete approved register.
        manifest: Versioned inputs, their fingerprint, counts and build timestamp.
    Returns:
        None. The caller commits/closes or discards this temporary database.
    """
    # Schema names are fixed code. Document values use SQL parameters below.
    connection.executescript(f"""
        CREATE TABLE manifest (
            singleton INTEGER PRIMARY KEY CHECK (singleton = 1),
            manifest_json TEXT NOT NULL
        );
        CREATE TABLE documents (
            source_id TEXT NOT NULL PRIMARY KEY,
            document_sha256 TEXT NOT NULL,
            page_count INTEGER NOT NULL CHECK (page_count > 0),
            document_json TEXT NOT NULL
        );
        CREATE TABLE pages (
            source_id TEXT NOT NULL,
            pdf_page INTEGER NOT NULL CHECK (pdf_page > 0),
            text TEXT NOT NULL,
            text_sha256 TEXT NOT NULL,
            page_json TEXT NOT NULL,
            PRIMARY KEY (source_id, pdf_page),
            FOREIGN KEY (source_id) REFERENCES documents(source_id)
        );
        CREATE TABLE chunks (
            chunk_id TEXT NOT NULL PRIMARY KEY,
            source_id TEXT NOT NULL,
            pdf_page INTEGER NOT NULL,
            reporting_scope TEXT NOT NULL,
            start_char INTEGER NOT NULL CHECK (start_char >= 0),
            end_char INTEGER NOT NULL CHECK (end_char > start_char),
            text TEXT NOT NULL,
            reviewed_note TEXT,
            chunk_json TEXT NOT NULL,
            FOREIGN KEY (source_id, pdf_page) REFERENCES pages(source_id, pdf_page)
        );
        CREATE INDEX chunks_by_page ON chunks(source_id, pdf_page, start_char);
        CREATE VIRTUAL TABLE chunk_fts USING fts5(
            chunk_id UNINDEXED, text, reviewed_note,
            tokenize='{FTS5_TOKENIZER}'
        );
    """)

    for document in batch["documents"]:
        summary = {
            key: value for key, value in document.items()
            if key not in {"pages", "chunks"}
        }
        connection.execute(
            "INSERT INTO documents VALUES (?, ?, ?, ?)",
            (document["source_id"], document["document_sha256"],
             document["page_count"], _canonical_json(summary)),
        )
        pages = {page["pdf_page"]: page for page in document["pages"]}
        for page in pages.values():
            if (
                page["source_id"] != document["source_id"]
                or page["document_sha256"] != document["document_sha256"]
                or hashlib.sha256(page["text"].encode("utf-8")).hexdigest() != page["text_sha256"]
            ):
                raise ValueError("Page evidence is inconsistent; index not replaced.")
            connection.execute(
                "INSERT INTO pages VALUES (?, ?, ?, ?, ?)",
                (page["source_id"], page["pdf_page"], page["text"],
                 page["text_sha256"], _canonical_json(page)),
            )

        for chunk in document["chunks"]:
            parent = pages[chunk["pdf_page"]]
            start, end = chunk["start_char"], chunk["end_char"]
            identity = {key: value for key, value in chunk.items() if key != "chunk_id"}
            if (
                chunk["source_id"] != document["source_id"]
                or chunk["document_sha256"] != document["document_sha256"]
                or not 0 <= start < end <= len(parent["text"])
                or chunk["text"] != parent["text"][start:end]
                or chunk["page_text_sha256"] != parent["text_sha256"]
                or _json_sha256(identity) != chunk["chunk_id"]
            ):
                raise ValueError("Chunk evidence is inconsistent; index not replaced.")
            connection.execute(
                "INSERT INTO chunks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (chunk["chunk_id"], chunk["source_id"], chunk["pdf_page"],
                 chunk["reporting_scope"], start, end, chunk["text"],
                 chunk["reviewed_note"], _canonical_json(chunk)),
            )
            # Both fields are searchable, but review notes stay separate from text.
            connection.execute(
                "INSERT INTO chunk_fts (chunk_id, text, reviewed_note) VALUES (?, ?, ?)",
                (chunk["chunk_id"], chunk["text"], chunk["reviewed_note"] or ""),
            )
    connection.execute(
        "INSERT INTO manifest VALUES (1, ?)", (_canonical_json(manifest),)
    )


def _inspect_index_database(path: Path, expected_inputs: dict) -> dict:
    """Open an existing index read-only and verify freshness/basic consistency.

    Parameters:
        path: Existing index or completed temporary database.
        expected_inputs: Current approved configuration/runtime snapshot.
    Returns:
        A compact ready-status dictionary.
    Raises:
        FileNotFoundError, ValueError or sqlite3.Error for missing/stale/bad data.
    """
    if not path.is_file():
        raise FileNotFoundError("Retrieval index is missing; build it first.")

    # mode=ro refuses to create a missing database; closing releases OS handles.
    uri = path.resolve().as_uri() + "?mode=ro"
    with closing(sqlite3.connect(uri, uri=True)) as connection:
        connection.execute("PRAGMA query_only = ON")
        if connection.execute("PRAGMA quick_check").fetchall() != [("ok",)]:
            raise ValueError("Index integrity check failed; rebuild it.")
        row = connection.execute(
            "SELECT manifest_json FROM manifest WHERE singleton = 1"
        ).fetchone()
        if row is None:
            raise ValueError("Index manifest is missing; rebuild it.")
        manifest = json.loads(row[0])
        if (
            not isinstance(manifest, dict)
            or type(manifest.get("index_schema_version")) is not int
            or manifest["index_schema_version"] != INDEX_SCHEMA_VERSION
        ):
            raise ValueError("Unsupported index schema; rebuild it.")
        required_fields = ("inputs", "inputs_sha256", "counts", "built_at_utc",
                           "physical_pages", "skipped_page_count")
        if any(field not in manifest for field in required_fields):
            raise ValueError("Index manifest is incomplete; rebuild it.")
        stored_hash = manifest.get("inputs_sha256")
        if stored_hash != _json_sha256(manifest.get("inputs")):
            raise ValueError("Index manifest fingerprint mismatch; rebuild it.")
        if stored_hash != _json_sha256(expected_inputs):
            raise ValueError("Retrieval index is stale; rebuild it.")

        counts = {
            "documents": connection.execute("SELECT COUNT(*) FROM documents").fetchone()[0],
            "pages": connection.execute("SELECT COUNT(*) FROM pages").fetchone()[0],
            "chunks": connection.execute("SELECT COUNT(*) FROM chunks").fetchone()[0],
            "fts_rows": connection.execute("SELECT COUNT(*) FROM chunk_fts").fetchone()[0],
        }
        physical_pages = connection.execute(
            "SELECT COALESCE(SUM(page_count), 0) FROM documents"
        ).fetchone()[0]
        if (
            counts != manifest.get("counts")
            or physical_pages != manifest["physical_pages"]
            or physical_pages - counts["pages"] != manifest["skipped_page_count"]
        ):
            raise ValueError("Index counts do not match its manifest; rebuild it.")
        if connection.execute("PRAGMA foreign_key_check").fetchall():
            raise ValueError("Index page/source relationships are invalid; rebuild it.")

        distinct_ids = connection.execute(
            "SELECT COUNT(DISTINCT chunk_id) FROM chunk_fts"
        ).fetchone()[0]
        mismatches = connection.execute("""
            SELECT COUNT(*) FROM chunk_fts AS f
            LEFT JOIN chunks AS c ON c.chunk_id = f.chunk_id
            WHERE c.chunk_id IS NULL OR f.text IS NOT c.text
               OR f.reviewed_note IS NOT COALESCE(c.reviewed_note, '')
        """).fetchone()[0]
        if distinct_ids != counts["chunks"] or mismatches:
            raise ValueError("Full-text rows do not match chunk records; rebuild it.")

    return {
        "status": "ready",
        "index_path": str(path),
        "index_schema_version": INDEX_SCHEMA_VERSION,
        "built_at_utc": manifest["built_at_utc"],
        "inputs_sha256": stored_hash,
        "source_count": counts["documents"],
        "physical_pages": manifest["physical_pages"],
        "usable_pages": counts["pages"],
        "skipped_page_count": manifest["skipped_page_count"],
        "chunk_count": counts["chunks"],
        "fts_row_count": counts["fts_rows"],
    }


def build_index(root: Path) -> dict:
    """Build a complete replacement index, preserving the old file on failure.

    Parameters:
        root: Repository directory; target is fixed under data/retrieval/.
    Returns:
        Verified ready-status information after successful replacement.
    """
    project_root, sources, settings = _read_inputs(root)
    inputs = _index_inputs(sources, settings)
    batch = _collect_chunks(project_root, sources, settings)
    manifest = {
        "index_schema_version": INDEX_SCHEMA_VERSION,
        "built_at_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": inputs,
        "inputs_sha256": _json_sha256(inputs),
        "physical_pages": batch["physical_pages"],
        "skipped_page_count": batch["skipped_page_count"],
        "counts": {
            "documents": batch["source_count"],
            "pages": batch["usable_pages"],
            "chunks": batch["chunk_count"],
            "fts_rows": batch["chunk_count"],
        },
    }

    target = project_root / INDEX_RELATIVE_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, name = tempfile.mkstemp(
        prefix=".index-", suffix=".sqlite", dir=target.parent
    )
    os.close(descriptor)  # SQLite opens it separately; important on Windows.
    temporary = Path(name)
    replaced = False
    try:
        with closing(sqlite3.connect(temporary)) as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.execute("PRAGMA journal_mode = DELETE").fetchone()
            _write_index_database(connection, batch, manifest)
            connection.commit()
        # All writer handles are closed before validation and replacement.
        report = _inspect_index_database(temporary, inputs)
        report["index_path"] = str(target)

        # Use one captured configuration for the build; reject later changes.
        _, current_sources, current_settings = _read_inputs(project_root)
        if _index_inputs(current_sources, current_settings) != inputs:
            raise ValueError("Configuration changed during index build; old index preserved.")
        os.replace(temporary, target)
        replaced = True
        return report  # No further file operations after the replacement.
    finally:
        if not replaced:
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass  # Preserve the original build error if cleanup is refused.


def get_index_status(root: Path) -> dict:
    """Read and validate the saved index without creating or rebuilding a file.

    Parameters:
        root: Repository directory with current approved configuration.
    Returns:
        A compact ready-status dictionary; missing/stale indexes raise errors.
    """
    project_root, sources, settings = _read_inputs(root)
    return _inspect_index_database(
        project_root / INDEX_RELATIVE_PATH, _index_inputs(sources, settings)
    )
```

### Understand the tables

| Table | Stored evidence / purpose |
|---|---|
| documents | One current approved document version per source, physical count, skip/count summary |
| pages | Complete canonical page JSON and exact extracted text/hash, keyed by source/page |
| chunks | Complete chunk JSON, offsets, source/scope and separate review metadata |
| chunk_fts | Searchable raw-text and reviewed-note columns; chunk ID connects back to chunks |
| manifest | One build receipt with versions, input fingerprint, counts and timestamp |

The SQL columns provide keys/joins/filtering. The JSON preserves the complete
existing evidence-record layout without rebuilding every field in each reader.
There is deliberate duplication; the builder writes both representations from
the same verified record. This is not a general schema for arbitrary documents.

The full-text table indexes raw text and reviewed_note as separate columns.
This lets later retrieval find reviewed labels that embedded extraction missed.
A note remains labelled metadata, not verbatim PDF text. It describes a parent
page and may not support every small chunk on that page. Step 7 must return
evidence clearly; an FTS match is not itself a supported answer.

Parameter placeholders bind document values safely. The schema names and
tokenizer are fixed code, not SQL accepted from a question or a document.
Foreign-key checks connect chunks to existing pages and pages to documents.

### Understand the functions

| Function | Inputs | Responsibility |
|---|---|---|
| _canonical_json | JSON-compatible value | Fixed key/spacing representation |
| _json_sha256 | JSON-compatible value | Fingerprint the representation |
| _index_inputs | Approved sources and settings | Include source/configuration and runtime/method versions |
| _write_index_database | Temporary connection, batch, manifest | Create/populate tables using verified evidence |
| _inspect_index_database | Existing path, expected input snapshot | Open read-only; check schema, freshness, counts, relationships and FTS correspondence |
| build_index | Repository root | Build, validate, close and replace the complete index |
| get_index_status | Repository root | Inspect freshness/readiness without building or writing |

The index always covers the full approved source register. A source filter still
works for page/chunk inspection; index construction is intentionally complete,
so a partial run cannot silently replace a full catalogue.

The manifest fingerprints the full source register, retrieval settings including
notes, schema/method/tokenizer versions, PyMuPDF, Python and SQLite versions.
A formatting-only JSON edit does not change canonical values. A relevant value
or runtime-version change invalidates the old index and requires an explicit
rebuild. Conservative runtime checks are intentional.

The UTC build time is a receipt, not part of chunk identity. Rebuilding may change
database bytes/timestamps while keeping the same logical chunk IDs.
A matching hash detects a mismatch; it does not authenticate an editable cache
as a signed document or certify the truth of its contents.

### How replacement works

1. Read/validate a configuration snapshot and extract all selected PDF bytes
   against their approved hashes.
2. Create a temporary SQLite file in the destination directory.
3. Write and commit its complete records, close the writer, then inspect it.
4. Reject any input-configuration change detected before publication.
5. Use os.replace only after every check succeeds.

The temporary file shares the destination filesystem, supporting an atomic
replacement. Every SQLite connection is closed before the swap, including on
Windows. If writing, validation or replacement fails, preserve the old index
and attempt to remove the unpublished temporary file.

closing(connection) is deliberate: SQLite's own with connection block controls
transactions but does not itself close the connection. PRAGMA foreign_keys
enables relationship checks during writing. DELETE journal mode keeps the
published database self-contained rather than relying on a WAL sidecar.

No potentially failing file read is performed after successful replacement.
If the OS refuses the swap, the old file remains available; a test simulates this.
Atomic replacement describes the publication step, not byte-identical rebuilds.

### What status verifies

Readiness checks include SQLite quick_check, stored schema/input fingerprints,
expected counts, foreign-key relationships, unique full-text IDs and matching
full-text content/review fields. These are useful consistency checks, not a
complete adversarial tamper-proof audit.

The reader uses mode=ro, refuses a missing file and never rebuilds automatically.
It compares the current approved configuration/runtime with the build receipt.
It does not rehash cached PDFs on every status call: the saved index represents
the pinned bytes verified at build time. Its evidence can remain available even
if the original cached PDF is later absent; source/version approval still comes
from current configuration. A later rebuild re-verifies the actual cached bytes.

An unsupported, missing, corrupt or stale index produces an explicit error.
Do not make the reader create a new empty database to hide missing evidence.

## 5. Replace only main()

Replace the existing main() definition through its final print with this block.
Keep the bottom if __name__ == "__main__": main() guard once.

```python
def main() -> None:
    """Run an existing inspection mode, a full-index build, or read-only status."""
    parser = argparse.ArgumentParser(description="Verified PDF evidence and local index.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository directory.")
    parser.add_argument("--source", help="Approved source ID for page/all-page/chunk modes.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--page", type=int, help="One-based physical PDF page.")
    mode.add_argument("--all-pages", action="store_true", help="Read all usable pages.")
    mode.add_argument("--chunks", action="store_true", help="Read and chunk usable pages.")
    mode.add_argument("--build-index", action="store_true", help="Replace the complete local index.")
    mode.add_argument("--index-status", action="store_true", help="Inspect a fresh index read-only.")
    parser.add_argument("--summary", action="store_true", help="Omit batch page/chunk bodies.")
    arguments = parser.parse_args()
    if arguments.page is not None and not arguments.source:
        parser.error("--page requires --source.")
    if arguments.source and (arguments.build_index or arguments.index_status):
        parser.error("Index commands always use the complete approved source register.")
    if arguments.summary and not (arguments.all_pages or arguments.chunks):
        parser.error("--summary requires --all-pages or --chunks.")

    try:
        if arguments.build_index:
            evidence = build_index(arguments.root)
        elif arguments.index_status:
            evidence = get_index_status(arguments.root)
        elif arguments.chunks:
            evidence = extract_chunks(arguments.root, arguments.source)
        elif arguments.all_pages:
            evidence = extract_documents(arguments.root, arguments.source)
        else:
            evidence = extract_page(arguments.root, arguments.source, arguments.page)

        if arguments.summary:
            evidence["documents"] = [
                {key: value for key, value in item.items() if key not in {"pages", "chunks"}}
                for item in evidence["documents"]
            ]
    except (OSError, ValueError, sqlite3.Error) as error:
        parser.exit(status=1, message=f"Error: {error}\n")
    print(json.dumps(evidence, indent=2, ensure_ascii=False))
```

Existing page/all-page/chunk commands remain. New commands are --build-index and
--index-status. Index commands already return compact JSON, so --summary applies
only to the earlier batch modes. Index commands reject --source to enforce a
complete catalogue. sqlite3.Error is caught alongside the earlier file/value
errors so database failures are reported as command failures.

These are verification entry points for storage. Step 7 adds actual query/ranking
behaviour; later CLI lessons integrate the growing interface. No search command
is claimed merely because an FTS table exists.

## 6. Extend test imports

Open tests/test_retrieval.py. Add import sqlite3 alongside the standard-library
imports. Replace from contextlib import redirect_stdout with:

```python
from contextlib import closing, redirect_stdout
```

Below import fitz, add:

```python
import gacl_pipeline.retrieval as retrieval_module
```

The module alias lets one test wrap the real temporary writer while injecting a
configuration change. Replace the existing multi-line function import with:

```python
from gacl_pipeline.retrieval import (
    build_index,
    chunk_page,
    chunk_text,
    extract_chunks,
    extract_documents,
    extract_page,
    get_index_status,
    main,
)
```

Keep the existing fixed self.settings, source/PDF fixture and all 28 retrieval
tests intact. Temporary fixture directories keep these tests independent of the
real PDFs, real warehouse and generated project index.

## 7. Add 12 tests inside PageEvidenceTests

Insert these methods after the existing test_invalid_chunk_settings_fail_before_pdf_read
method and immediately before class ChunkSpanTests begins. Keep the four-space
indentation: these methods belong to PageEvidenceTests, not the string-test class.

```python
    def test_index_round_trip_and_separate_fts_notes(self) -> None:
        """Persist complete fixture records; keep searchable reviews separate."""
        expected = extract_chunks(self.root)
        report = build_index(self.root)
        self.assertEqual(
            (report["source_count"], report["usable_pages"], report["chunk_count"], report["fts_row_count"]),
            (1, 2, 2, 2),
        )
        path = Path(report["index_path"])
        with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)) as connection:
            stored_pages = [
                json.loads(row[0])
                for row in connection.execute("SELECT page_json FROM pages ORDER BY pdf_page")
            ]
            stored_chunks = [
                json.loads(row[0])
                for row in connection.execute("SELECT chunk_json FROM chunks ORDER BY pdf_page, start_char")
            ]
            self.assertEqual(stored_pages, expected["documents"][0]["pages"])
            self.assertEqual(stored_chunks, expected["documents"][0]["chunks"])
            for chunk_id, text, note in connection.execute(
                "SELECT chunk_id, text, reviewed_note FROM chunk_fts"
            ):
                chunk = next(item for item in stored_chunks if item["chunk_id"] == chunk_id)
                self.assertEqual(text, chunk["text"])
                self.assertEqual(note, chunk["reviewed_note"] or "")
                self.assertNotIn("REVIEW_ONLY_SENTINEL", text)

    def test_index_rebuild_keeps_ids_without_duplicate_rows(self) -> None:
        """A rebuild replaces the catalogue instead of appending duplicate chunks."""
        first = build_index(self.root)
        path = Path(first["index_path"])
        with closing(sqlite3.connect(path)) as connection:
            first_ids = connection.execute(
                "SELECT chunk_id FROM chunks ORDER BY chunk_id"
            ).fetchall()
        second = build_index(self.root)
        with closing(sqlite3.connect(path)) as connection:
            second_ids = connection.execute(
                "SELECT chunk_id FROM chunks ORDER BY chunk_id"
            ).fetchall()
        self.assertEqual(first_ids, second_ids)
        self.assertEqual(second["chunk_count"], 2)
        self.assertEqual(second["fts_row_count"], 2)

    def test_failed_index_write_preserves_existing_file(self) -> None:
        """A write failure must leave the old index bytes unchanged."""
        path = Path(build_index(self.root)["index_path"])
        original_bytes = path.read_bytes()
        with patch(
            "gacl_pipeline.retrieval._write_index_database",
            side_effect=sqlite3.OperationalError("injected write failure"),
        ):
            with self.assertRaises(sqlite3.OperationalError):
                build_index(self.root)
        self.assertEqual(path.read_bytes(), original_bytes)
        self.assertEqual(get_index_status(self.root)["status"], "ready")
        self.assertEqual(list(path.parent.glob(".index-*.sqlite")), [])

    def test_failed_first_index_build_leaves_no_target(self) -> None:
        """An unsuccessful first build must not publish an empty index."""
        with patch(
            "gacl_pipeline.retrieval._write_index_database",
            side_effect=sqlite3.OperationalError("injected first-build failure"),
        ):
            with self.assertRaises(sqlite3.OperationalError):
                build_index(self.root)
        target = self.root / "data" / "retrieval" / "index.sqlite"
        self.assertFalse(target.exists())
        self.assertEqual(list(target.parent.glob(".index-*.sqlite")), [])
        with self.assertRaises(FileNotFoundError):
            get_index_status(self.root)
        self.assertFalse(target.exists())

    def test_failed_index_replace_preserves_existing_file(self) -> None:
        """An OS refusal to replace the destination must preserve the old file."""
        path = Path(build_index(self.root)["index_path"])
        original_bytes = path.read_bytes()
        with patch(
            "gacl_pipeline.retrieval.os.replace",
            side_effect=PermissionError("injected replacement refusal"),
        ):
            with self.assertRaises(PermissionError):
                build_index(self.root)
        self.assertEqual(path.read_bytes(), original_bytes)
        self.assertEqual(list(path.parent.glob(".index-*.sqlite")), [])

    def test_changed_inputs_during_build_preserve_existing_file(self) -> None:
        """Reject settings changed during the write, before publishing the result."""
        path = Path(build_index(self.root)["index_path"])
        original_bytes = path.read_bytes()
        original_writer = retrieval_module._write_index_database

        def change_settings_after_write(connection, batch, manifest) -> None:
            """Write the temporary DB, then simulate a concurrent config edit."""
            original_writer(connection, batch, manifest)
            self.settings["overlap_chars"] = 249
            self.write_config()

        with patch(
            "gacl_pipeline.retrieval._write_index_database",
            side_effect=change_settings_after_write,
        ):
            with self.assertRaisesRegex(ValueError, "Configuration changed"):
                build_index(self.root)
        self.assertEqual(path.read_bytes(), original_bytes)
        self.assertEqual(list(path.parent.glob(".index-*.sqlite")), [])

    def test_stale_index_settings_are_rejected_without_rebuild(self) -> None:
        """A changed settings value must invalidate status without writing a DB."""
        path = Path(build_index(self.root)["index_path"])
        original_bytes = path.read_bytes()
        self.settings["overlap_chars"] = 249
        self.write_config()
        with self.assertRaisesRegex(ValueError, "stale; rebuild"):
            get_index_status(self.root)
        self.assertEqual(path.read_bytes(), original_bytes)

    def test_missing_index_status_does_not_create_database(self) -> None:
        """Read-only status must not turn a missing path into an empty SQLite DB."""
        target = self.root / "data" / "retrieval" / "index.sqlite"
        with self.assertRaises(FileNotFoundError):
            get_index_status(self.root)
        self.assertFalse(target.exists())
        self.assertFalse(target.parent.exists())

    def test_index_manifest_problems_are_rejected(self) -> None:
        """Reject a missing manifest, wrong fingerprint or unsupported schema."""
        for issue in ("missing", "fingerprint", "schema"):
            with self.subTest(issue=issue):
                path = Path(build_index(self.root)["index_path"])
                with closing(sqlite3.connect(path)) as connection:
                    if issue == "missing":
                        connection.execute("DELETE FROM manifest")
                    else:
                        manifest = json.loads(connection.execute(
                            "SELECT manifest_json FROM manifest WHERE singleton = 1"
                        ).fetchone()[0])
                        if issue == "fingerprint":
                            manifest["inputs_sha256"] = "0" * 64
                        else:
                            manifest["index_schema_version"] = 999
                        connection.execute(
                            "UPDATE manifest SET manifest_json = ? WHERE singleton = 1",
                            (json.dumps(manifest),),
                        )
                    connection.commit()
                with self.assertRaises(ValueError):
                    get_index_status(self.root)

    def test_index_count_mismatch_is_rejected(self) -> None:
        """Detect a missing full-text row even when the SQLite file opens."""
        path = Path(build_index(self.root)["index_path"])
        with closing(sqlite3.connect(path)) as connection:
            connection.execute(
                "DELETE FROM chunk_fts WHERE chunk_id = (SELECT MIN(chunk_id) FROM chunks)"
            )
            connection.commit()
        with self.assertRaisesRegex(ValueError, "counts"):
            get_index_status(self.root)

    def test_index_build_leaves_observation_warehouse_untouched(self) -> None:
        """The separate catalogue must preserve an existing warehouse file."""
        warehouse = self.root / "data" / "warehouse" / "gacl.sqlite"
        warehouse.parent.mkdir(parents=True)
        with closing(sqlite3.connect(warehouse)) as connection:
            connection.execute("CREATE TABLE sentinel (value TEXT NOT NULL)")
            connection.execute("INSERT INTO sentinel VALUES (?)", ("existing warehouse",))
            connection.commit()
        original_bytes = warehouse.read_bytes()
        report = build_index(self.root)
        self.assertNotEqual(Path(report["index_path"]), warehouse)
        self.assertEqual(warehouse.read_bytes(), original_bytes)
        self.assertEqual(get_index_status(self.root)["status"], "ready")

    def test_index_build_and_status_cli_without_cached_pdf(self) -> None:
        """Status reads persisted evidence and settings, not the original PDF."""
        for selection in ("--build-index", "--index-status"):
            with self.subTest(selection=selection):
                output = io.StringIO()
                with patch(
                    "sys.argv", ["retrieval", "--root", str(self.root), selection]
                ), redirect_stdout(output):
                    main()
                report = json.loads(output.getvalue())
                self.assertEqual(report["status"], "ready")
                self.assertEqual(report["chunk_count"], 2)
                if selection == "--build-index":
                    self.pdf_path.unlink()  # The second command needs no cached PDF.
```

The tests cover persisted JSON round-trips, separate searchable review fields,
replacement without duplicate IDs, failed writes/first builds/swaps, changed
configuration during a build, stale reads, missing-file noncreation, manifest and
count errors, warehouse preservation and CLI status without a cached PDF.

patch temporarily injects failures instead of depending on a real disk failure.
The wrapped-writer test changes the temporary configuration after writing; it
proves that the builder checks again before replacing the old file.
The intentionally damaged SQLite files are test fixtures, not your real index.
All connections close before reading bytes, deleting files or replacing indexes.

Expected totals after implementation:

| Suite | Expected tests |
|---|---:|
| Retrieval file | 40 = 28 existing + 12 new |
| Full suite | 72 = 60 existing + 12 new |

These are learner acceptance targets. The isolated reference run is recorded
separately above; it does not establish your Windows or full-suite results.

## 8. Run focused and full tests

Save .gitignore and both Python files first:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_retrieval.py" -v

.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Expected: 40 focused / 72 full tests, all passing without skips.
Share any traceback before treating later actions as a completed gate.

## 9. Build the real index and inspect readiness

First confirm that the generated destination is ignored. Then, in this same
PowerShell session, capture the existing warehouse fingerprint before building:

```powershell
git check-ignore -v -- data/retrieval/index.sqlite

# A baseline for this build only; the core pipeline later records new run history.
$warehouseBefore = (Get-FileHash -LiteralPath .\data\warehouse\gacl.sqlite -Algorithm SHA256 -ErrorAction Stop).Hash
```

Now build and inspect the new catalogue:

```powershell
.\.venv\Scripts\python.exe -m gacl_pipeline.retrieval --build-index
if ($LASTEXITCODE -ne 0) { throw "Index build failed; stop and share the error." }

.\.venv\Scripts\python.exe -m gacl_pipeline.retrieval --index-status
if ($LASTEXITCODE -ne 0) { throw "Index status failed; stop and share the error." }

$warehouseAfter = (Get-FileHash -LiteralPath .\data\warehouse\gacl.sqlite -Algorithm SHA256 -ErrorAction Stop).Hash
if ($warehouseBefore -ne $warehouseAfter) { throw "Warehouse bytes changed during the index check." }
Write-Host "Warehouse unchanged during index build/status."
```

Expected ready output includes:

| Field | Expected with unchanged approved inputs |
|---|---|
| status | ready |
| source_count | 2 |
| physical_pages | 71 |
| usable_pages | 70 |
| skipped_page_count | 1 |
| chunk_count | 136 |
| fts_row_count | 136 |
| index_schema_version | 1 |
| index_path | Your repository's data/retrieval/index.sqlite |
| built_at_utc / inputs_sha256 | Actual build time and computed fingerprint; record your values |

These counts derive from the verified Step 5 corpus, but your stored result must
be checked. A successful status read does not create or refresh the index.

## 10. Verify saved records and rebuild repeatability

This read-only inspection plus one explicit rebuild checks the actual SQLite
records and confirms that IDs survive replacement. It prints summaries only.

```powershell
@'
"""Verify persisted real evidence and repeatable rebuilds without changing facts."""

import hashlib
import json
import sqlite3
from contextlib import closing
from pathlib import Path
from gacl_pipeline.retrieval import build_index, get_index_status

root = Path.cwd()
target = root / "data" / "retrieval" / "index.sqlite"
warehouse = root / "data" / "warehouse" / "gacl.sqlite"

# A status read should leave the existing index bytes unchanged.
before_status = hashlib.sha256(target.read_bytes()).hexdigest()
first_status = get_index_status(root)
assert hashlib.sha256(target.read_bytes()).hexdigest() == before_status

# Read saved records after the builder's connection has already closed.
with closing(sqlite3.connect(target.resolve().as_uri() + "?mode=ro", uri=True)) as connection:
    pages = {}
    for row in connection.execute("SELECT page_json FROM pages"):
        page = json.loads(row[0])
        pages[(page["source_id"], page["pdf_page"])] = page
    chunks = [
        json.loads(row[0])
        for row in connection.execute("SELECT chunk_json FROM chunks ORDER BY chunk_id")
    ]

covered = {key: 0 for key in pages}
for chunk in sorted(chunks, key=lambda item: (
    item["source_id"], item["pdf_page"], item["start_char"]
)):
    key = (chunk["source_id"], chunk["pdf_page"])
    parent = pages[key]
    start, end = chunk["start_char"], chunk["end_char"]
    assert start <= covered[key] < end <= len(parent["text"])
    assert chunk["text"] == parent["text"][start:end]
    assert chunk["page_text_sha256"] == parent["text_sha256"]
    assert chunk["reviewed_note"] == parent["reviewed_note"]
    covered[key] = end
for key, page in pages.items():
    assert covered[key] == len(page["text"])

# Rebuild once more and compare logical IDs, not whole-database file hashes.
warehouse_before = hashlib.sha256(warehouse.read_bytes()).hexdigest()
rebuilt = build_index(root)
with closing(sqlite3.connect(target.resolve().as_uri() + "?mode=ro", uri=True)) as connection:
    second_ids = [
        row[0] for row in connection.execute("SELECT chunk_id FROM chunks ORDER BY chunk_id")
    ]
assert [chunk["chunk_id"] for chunk in chunks] == second_ids
assert hashlib.sha256(warehouse.read_bytes()).hexdigest() == warehouse_before
assert rebuilt["chunk_count"] == len(chunks)

print(json.dumps({
    "source_count": rebuilt["source_count"],
    "usable_pages": len(pages),
    "chunk_count": len(chunks),
    "fts_row_count": rebuilt["fts_row_count"],
    "persisted_spans_and_coverage": "passed",
    "stable_ids_after_rebuild": True,
    "warehouse_unchanged_during_rebuild": True,
    "status_read_only_check": "passed",
}, indent=2))
'@ | .\.venv\Scripts\python.exe -
```

Expected: 2 sources, 70 usable pages, 136 chunks/FTS rows, passed persisted-span
coverage, stable IDs after rebuild, unchanged warehouse during rebuild and a
passed read-only status check. A changed whole-database file hash after rebuild
would be normal because its receipt timestamp can change.

The unit tests simulate failed rebuilds; the real check covers a successful
replacement on your Windows filesystem. Keep those evidence types separate.

## 11. Confirm the original numerical pipeline and Git scope

After the warehouse-preservation checks above, run the normal core regression:

```powershell
.\.venv\Scripts\python.exe -m gacl_pipeline --offline

git status --short --branch
git diff --stat
git diff --check
git check-ignore -v -- data/retrieval/index.sqlite
```

Expected: cached PDFs verified, 18 extracted/loaded/stored and four passing checks.
This core command legitimately records another run, so compare the earlier
warehouse fingerprints before running it.

Expected modified paths are .gitignore, src/gacl_pipeline/retrieval.py and
tests/test_retrieval.py. Generated index/temporary files remain ignored.
If generated files appear in Git status, repair the ignore rule before staging.
No real PDFs, warehouse databases or terminal dumps should be committed.

## Stop and share the evidence

Share focused/full test summaries, the real build/status JSON, both warehouse
preservation messages/results, persisted-record/rebuild verification, the offline
numerical summary and Git status/diff/ignore output. Share tracebacks for errors.
Keep the implementation uncommitted until results and file scope are reviewed.

For understanding, explain why a failed rebuild preserves the old index, why
same chunk IDs need not mean identical database-file bytes, and how a fingerprint
detects stale settings without becoming a security signature. Explain the roles
of the manifest and foreign keys, and why status uses a read-only connection.

After review, create the implementation checkpoint and batch documentation
synchronization. Step 7 then adds parameterized keyword retrieval, source/scope
filters, page deduplication and ranking. It is not part of this storage lesson.

References: [Python sqlite3](https://docs.python.org/3.11/library/sqlite3.html),
[SQLite FTS5](https://sqlite.org/fts5.html),
[Python tempfile](https://docs.python.org/3.11/library/tempfile.html),
[os.replace](https://docs.python.org/3.11/library/os.html#os.replace),
[contextlib.closing](https://docs.python.org/3.11/library/contextlib.html#contextlib.closing).
