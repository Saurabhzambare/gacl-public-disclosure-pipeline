# Phase 2 — Step 4: Define page evidence and extract usable pages

Build-order version: 1.0. Prepared: 25 November 2026 (India).
Step 4A execution: **passed on the author's Windows laptop, 27 November 2026**.
Evidence: approved monthly PDF hash, page 5/printed 4 with six freshwater rows,
page 6/printed null, page zero exit 1, and 32 tests passing in 1.233 seconds.
The module is untracked. Review its actual contents before precise 4B edits;
existing regression tests do not constitute focused coverage of the new module.
Then: **4B — all usable pages, metadata configuration and focused tests; pending**.
These are two exercises inside existing Step 4, not new numbered roadmap steps.
Step 5 cannot begin until the complete Step 4 gate passes.

## Verified starting point

The author supplied successful local merge a5001c0 on feature/phase2-guided,
preserving inspector commit 39ceacb and documentation through origin/main
3df36db. Git status was clean. This is a personal-branch merge, not evidence
that the inspector was uploaded or merged into public main.

Read the lesson online or use the code supplied in the conversation. No additional
documentation merge is required just to start 4A. Batch newer documentation
synchronization at the Step 4 checkpoint, inspecting actual branch state first.

## Purpose and ELI5

The Step 3 inspector prints text for a person. A reusable extractor should
return a Python dictionary containing text together with its source, approved
document version, page and reporting boundary. Later functions can inspect,
chunk, index or cite that evidence without parsing terminal output.

ELI5: put the page's words and its address label into one envelope. Hand that
envelope to the next part of the application.

A contract is an agreement about field names, types and meanings. It does not
make a statement true merely because it fits the expected shape. This lesson
introduces a minimal page contract; full reviewed metadata and all-page rules
are completed in 4B.

## Installations and files

No new installation. Reuse the existing Python 3.11.4 / PyMuPDF 1.26.6 environment.
Create exactly one application file in 4A:

`D:\gacl-public-disclosure-pipeline\src\gacl_pipeline\retrieval.py`

The folder already exists. Keep scripts/inspect_source_page.py unchanged.
Do not create .github/scripts, a model, index, cloud service or retrieval
configuration yet. config/retrieval.json and focused tests come in 4B.

From the repository root:

```powershell
# Confirm the implementation branch and inspect any changes first.
git status --short --branch

# This was absent at the earlier baseline. Inspect rather than overwrite if True.
Test-Path .\src\gacl_pipeline\retrieval.py
```

If the file is absent and the starting branch is clean, open the exact file:

```powershell
notepad .\src\gacl_pipeline\retrieval.py
```

Save the complete code below as retrieval.py, UTF-8, not retrieval.py.txt.
This is file content, not a PowerShell command.

## Complete commented 4A code

```python
"""Extract verified PDF-page evidence for later document retrieval."""

import argparse
import hashlib
import json
from pathlib import Path

import fitz  # Existing PyMuPDF dependency; no new installation is needed.


# Identify the extraction method so later artifacts can record how text was read.
EXTRACTION_VERSION = "pymupdf-page-text-sort-v1"


def extract_page(root: Path, source_id: str, pdf_page: int) -> dict:
    """Return one verified page as a structured evidence record.

    Parameters:
        root: Repository directory containing config/ and data/raw/.
        source_id: Approved report identifier in config/sources.json.
        pdf_page: One-based physical PDF page, not its printed label.

    Returns:
        A dictionary containing exact extracted text and source/page metadata.

    Raises:
        ValueError: Invalid selection, changed PDF or unusable page.
        OSError: Configuration or source file cannot be read.
    """
    # Reject bool as well as zero/negative/non-integer page selections.
    if type(pdf_page) is not int or pdf_page < 1:
        raise ValueError("PDF page must be a positive integer.")

    # An explicit root also lets future tests use temporary project folders.
    project_root = Path(root).resolve()
    manifest_path = project_root / "config" / "sources.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    # Source selection is limited to the existing approved register.
    source = None
    for candidate in manifest["sources"]:
        if candidate["source_id"] == source_id:
            source = candidate
            break
    if source is None:
        raise ValueError(f"Unknown source ID: {source_id}")

    # Hash and parse the same in-memory bytes, preserving document identity.
    pdf_path = project_root / "data" / "raw" / f"{source_id}.pdf"
    pdf_bytes = pdf_path.read_bytes()
    document_hash = hashlib.sha256(pdf_bytes).hexdigest()
    if document_hash != source["sha256"]:
        raise ValueError("PDF checksum mismatch. Stop and review the source.")

    # Unknown printed-page mappings stay None rather than being guessed.
    printed_page = None
    for mapping in source.get("pages", []):
        if mapping["pdf_page"] == pdf_page:
            printed_page = mapping["printed_page"]
            break

    # Close the PDF automatically; extracted strings survive after closing.
    with fitz.open(stream=pdf_bytes, filetype="pdf") as document:
        if document.needs_pass:
            raise ValueError("Encrypted PDFs are not supported.")

        page_count = len(document)
        if pdf_page > page_count:
            raise ValueError(f"This PDF has only {page_count} pages.")

        page = document.load_page(pdf_page - 1)
        text = page.get_text("text", sort=True)
        if not text.strip():
            raise ValueError("No embedded text found; OCR is not implemented.")

    # Do not strip/rewrite text: later chunk offsets must refer to exact content.
    text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()

    # Return values for other functions instead of printing inside the extractor.
    return {
        "source_id": source_id,
        "document_sha256": document_hash,
        "source_url": source["url"],
        "reporting_scope": source["reporting_scope"],
        "pdf_page": pdf_page,
        "printed_page": printed_page,
        "page_count": page_count,
        "text": text,
        "text_sha256": text_hash,
        "extraction_version": EXTRACTION_VERSION,
        "pymupdf_version": fitz.VersionBind,
        "citation_url": source["url"] + f"#page={pdf_page}",
    }


def main() -> None:
    """Read terminal inputs and display the returned evidence as JSON."""
    parser = argparse.ArgumentParser(description="Extract one verified PDF page.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository directory; defaults to the current working directory.",
    )
    parser.add_argument("--source", required=True, help="Approved source ID.")
    parser.add_argument("--page", required=True, type=int, help="Physical PDF page.")
    arguments = parser.parse_args()

    try:
        evidence = extract_page(
            arguments.root, arguments.source, arguments.page
        )
    except (OSError, ValueError) as error:
        parser.exit(status=1, message=f"Error: {error}\n")

    # JSON is a display/serialization format; the function returns a Python dict.
    print(json.dumps(evidence, indent=2, ensure_ascii=False))


# Importing extract_page elsewhere must not execute the command-line interface.
if __name__ == "__main__":
    main()
```

## What changed from the inspector?

| Responsibility | Step 3 inspector | Step 4A module |
|---|---|---|
| Purpose | Human inspection utility | Reusable extraction/evidence function |
| Core function | Prints directly and returns None | Returns a dictionary |
| Repository location | Derived from the script path | Explicit root parameter; CLI defaults to current directory |
| Text provenance | Printed source identity/page | Stored with the returned text |
| Text fingerprint | Not a separate returned field | UTF-8 text SHA-256 stored separately from PDF hash |
| Terminal presentation | Plain text and metadata | main serializes the returned dictionary as JSON |
| Existing utility | Already committed locally | Remains unchanged |

Do not copy terminal output back into the data warehouse. The source configuration
and validated numerical facts remain authoritative and unchanged.

## Functions and parameters

extract_page(root, source_id, pdf_page) reads an approved source and returns its
page evidence. root makes future temporary-fixture tests possible; source_id
selects only a registered report; pdf_page is a positive one-based integer.
Type hints describe intended usage. The explicit check rejects bool because bool
is a subclass of int in Python.

main() parses command-line arguments, calls extract_page and displays JSON.
Importing extract_page from another module does not run main because of the
__name__ guard. The CLI here is a small inspection entry point; search/index
commands are introduced later, not available merely because this module exists.

The extractor performs file reads, but does not print, write a database, create
an index, download documents or invoke a model. The caller chooses what to do
with the returned record. No custom class is needed for this focused lesson.

## Evidence contract and variables

| Key / variable | Meaning |
|---|---|
| root / project_root | Explicit repository path; resolved before reading files |
| source / candidate | Approved source selected from the existing register |
| pdf_bytes | Same bytes used for verification and parsing |
| source_id | Stable registered report identifier |
| document_sha256 | SHA-256 of the original binary PDF |
| source_url | Approved official report URL |
| reporting_scope | Established document boundary, not inferred sentence/year classification |
| pdf_page | One-based physical PDF page; converted to zero-based index when reading |
| printed_page | Explicit configured mapping; None when unknown |
| page_count | Physical page count of the verified PDF |
| text | Exact output of embedded-text extraction, including its whitespace |
| text_sha256 | SHA-256 of that text encoded as UTF-8; not the same thing as PDF SHA-256 |
| extraction_version | Named extraction-method version |
| pymupdf_version | Actual installed extraction-library version |
| citation_url | Official URL plus physical PDF page fragment; does not check ongoing website availability |

We check text.strip() for emptiness but return the original text. Trimming or
rewriting it would change character positions used by later chunks. A text hash
can change if extraction/library behavior changes even when the PDF bytes match;
record both identities and versions.

A page can contain several measurements and units. Do not attach a guessed
single numerical value/unit/year to the whole page. Exact numerical answers
later use validated observations. JSON uses null for Python None. Escaped
newline sequences in JSON represent characters in a string; they are not lost
page content.

sort=True helps reading order but is not general table reconstruction. OCR,
reviewed annotations, multi-page extraction, chunking, database/index storage,
semantic retrieval and generation are outside 4A.

## Run from the repository root

The editable project installation exposes new modules inside src/gacl_pipeline;
no reinstall is normally needed.

```powershell
.\.venv\Scripts\python.exe -m gacl_pipeline.retrieval --source gacl_dahej_plot3_ec_2025_h1 --page 5
```

Here -m runs a package module. The required --source and --page arguments are
parsed by main. --root is optional when running from the repository root.

Expected: JSON containing the monthly source ID, approved PDF hash, source URL,
dahej_plot3_report, pdf_page 5, printed_page 4, page_count 21, extracted text,
a text hash and extraction/library versions. The text should retain the six
monthly rows and KL/day context. Source hash:
4882f4e453a78fe956850944d9df2b636c74d225eab2331e7d8873fe4050c9c1.

These are expected outcomes, not an executed-result claim. Review the actual
output before marking 4A passed. The record is a Python dictionary inside the
function; JSON is its terminal representation.

## Check unknown mappings and invalid input

```powershell
# Physical page 6 has no printed-page entry in the existing source configuration.
.\.venv\Scripts\python.exe -m gacl_pipeline.retrieval --source gacl_dahej_plot3_ec_2025_h1 --page 6
```

Expected printed_page: null. Even if a printed label is visible on the actual
page, do not guess its mapping in code or silently add an offset. This check
does not add a new measurement.

```powershell
# Page zero should fail explicitly.
.\.venv\Scripts\python.exe -m gacl_pipeline.retrieval --source gacl_dahej_plot3_ec_2025_h1 --page 0
$LASTEXITCODE
```

Expected: Error: PDF page must be a positive integer. Exit code 1 is expected
for this deliberate negative case. An unexpected error on the valid page is
a failure to inspect, not a successful negative test.

After implementing the new module, run the existing regression suite and status:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
git status --short --branch
```

The existing baseline is 32 passing tests. They protect original behavior;
focused tests for this new extractor are introduced in 4B. The direct page,
mapping and invalid-input runs check 4A behavior. Expect the new retrieval.py
to be untracked and the original inspector/source files unchanged.

## Understanding and stopping point

Explain the difference between print and return, why PDF and extracted-text
hashes describe different content, and why unknown printed_page should be None.
Share page-5 metadata and relevant table context, page-6 printed_page,
page-zero exit code, test summary and Git status. Do not commit Step 4 yet.

## 4B plan — not implementation instructions yet

After reviewing 4A output, extend the page contract/configuration to separate
reviewed notes from raw text, verify all required mappings, extract usable pages
from each approved document efficiently, record skipped image-only pages and
add meaningful isolated tests. Do not infer missing labels. The expected
reference coverage is 70 usable pages across two PDFs, but the learner's actual
counts and failures must be checked, not assumed.

Only after both exercises and actual evidence pass is Step 4 complete. Chunking
remains Step 5. Exact 4B code and file edits will be supplied after the current
module/output are reviewed. No application file is created or executed by the
assistant through this documentation publication.

References: [Python dictionaries](https://docs.python.org/3.11/tutorial/datastructures.html#dictionaries),
[hashlib](https://docs.python.org/3.11/library/hashlib.html),
[PyMuPDF page text](https://pymupdf.readthedocs.io/en/latest/page.html).
