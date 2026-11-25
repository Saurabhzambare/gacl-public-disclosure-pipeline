# Phase 2 — Step 3: Verify and inspect one known PDF page

Build-order version: 1.0. Prepared: 25 November 2026 (India).
Execution checks: **passed on the author's Windows laptop, 25 November 2026**.
The supplied terminal output shows the approved monthly hash, PDF page 5 /
printed page 4, six freshwater rows, rejection of page zero with exit code 1,
and 32 existing tests passing in 0.987 seconds. Subsequent file review found the
intended script matched this lesson. The author verified complete duplicate hashes,
removed only the extra .github/scripts/ copy and committed the single intended
103-line file locally as 39ceacb. Final branch feature/phase2-guided is clean.
The Step 3 local commit checkpoint is complete; no code upload/public merge is
claimed. The CRLF-to-LF warning is ordinary script line-ending normalization,
not a Python failure or a change to the verified source PDF. The reusable lesson and
sample below remain for reference.
Step 2 baseline execution passed on the author's Windows laptop. Understanding
discussion remains recorded separately in the learning log.

## Purpose and ELI5

Read one approved PDF page yourself and preserve its identity. This is the first
new application file you implement in the guided sequence. It is a learning
inspector, not the existing observation parser or a completed search/AI system.

ELI5: compare the book's fingerprint with the approved fingerprint, then open the
correct page and read its words. Finding a file is weaker evidence than checking
its contents.

## Requirements and exact file location

No installation is needed: reuse Python 3.11.4, PyMuPDF 1.26.6 and standard-library
modules. Create only `scripts/inspect_source_page.py` in the repository root,
normally `D:\gacl-public-disclosure-pipeline\scripts\inspect_source_page.py`.
Do not create retrieval/model/configuration files yet.

Stay on `feature/phase2-guided`. Before editing, check status and receive this
documentation while your branch is still clean at the main-based baseline:

```powershell
git status --short --branch
git pull --ff-only origin main
```

If Git reports changes, divergent history or any error, stop and share it.
Do not discard work. At this documented checkpoint the author has created the
branch but has not made a code commit, so receiving the new docs can fast-forward.
Future documentation synchronization after code commits may need a different
reviewed Git operation; do not assume this command always applies.

Then prepare the file:

```powershell
# Create the scripts folder if needed; existing contents are retained.
New-Item -ItemType Directory -Path .\scripts -Force

# Inspect before editing. If True, share the existing file first.
Test-Path .\scripts\inspect_source_page.py
```

If the file does not exist, open it:

```powershell
notepad .\scripts\inspect_source_page.py
```

Paste the complete Python block below into that file and save it as
`inspect_source_page.py`, UTF-8, not `inspect_source_page.py.txt`.
These are file contents, not commands to paste directly into PowerShell.

## Complete commented code

```python
"""Inspect one approved PDF page without changing project data."""

import argparse
import hashlib
import json
from pathlib import Path

import fitz  # PyMuPDF: already installed in the project's virtual environment.


def inspect_source_page(source_id: str, pdf_page: int) -> None:
    """Verify an approved PDF and print one page's text and provenance.

    Parameters:
        source_id: Identifier from config/sources.json.
        pdf_page: Physical PDF page number, starting at 1.

    Returns:
        None. Evidence and extracted text are printed to the terminal.
    """
    # Reject invalid human page numbers before opening any source.
    if pdf_page < 1:
        raise ValueError("PDF page must be 1 or greater.")

    # This script lives in scripts/, so its parent's parent is the repository.
    project_root = Path(__file__).resolve().parents[1]
    manifest_path = project_root / "config" / "sources.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    # Select only a source explicitly listed in the approved manifest.
    source = None
    for candidate in manifest["sources"]:
        if candidate["source_id"] == source_id:
            source = candidate
            break
    if source is None:
        raise ValueError(f"Unknown source ID: {source_id}")

    # Read the source once, then hash and parse those same bytes.
    pdf_path = project_root / "data" / "raw" / f"{source_id}.pdf"
    pdf_bytes = pdf_path.read_bytes()
    actual_hash = hashlib.sha256(pdf_bytes).hexdigest()

    # Stop if the bytes differ from the approved document version.
    if actual_hash != source["sha256"]:
        raise ValueError("PDF checksum mismatch. Stop and review the source.")

    # Printed page numbers come from explicit mappings, never a guessed offset.
    printed_page = None
    for mapping in source.get("pages", []):
        if mapping["pdf_page"] == pdf_page:
            printed_page = mapping["printed_page"]
            break

    # A context manager closes the PDF even if reading fails.
    with fitz.open(stream=pdf_bytes, filetype="pdf") as document:
        if document.needs_pass:
            raise ValueError("This inspector does not support encrypted PDFs.")

        page_count = len(document)
        if pdf_page > page_count:
            raise ValueError(f"This PDF has only {page_count} pages.")

        # PyMuPDF indexes pages from zero: human page 5 uses index 4.
        page_index = pdf_page - 1
        page = document.load_page(page_index)

        # Read embedded text; sorting helps reading order but does not perform OCR.
        text = page.get_text("text", sort=True)
        if not text.strip():
            raise ValueError("No embedded text found. OCR is outside this lesson.")

    # Strings and numbers remain usable after the PDF has been closed.
    print("Source ID:", source_id)
    print("Reporting scope:", source["reporting_scope"])
    print("SHA-256 verification: MATCH")
    print("Document hash:", actual_hash)
    print("PDF page:", pdf_page)
    print("Printed page:", printed_page if printed_page is not None else "not mapped")
    print("PDF page count:", page_count)
    print("Source URL:", source["url"])
    print("\nExtracted page text:\n")
    print(text)


def main() -> None:
    """Read command-line arguments, run the inspector and report expected errors."""
    # ArgumentParser defines the inputs accepted by this command.
    parser = argparse.ArgumentParser(description="Inspect a verified source page.")
    parser.add_argument("--source", required=True, help="Approved source ID.")
    parser.add_argument("--page", required=True, type=int, help="One-based PDF page.")
    arguments = parser.parse_args()

    try:
        inspect_source_page(arguments.source, arguments.page)
    except (OSError, ValueError) as error:
        # A nonzero exit makes missing files and invalid input visible.
        parser.exit(status=1, message=f"Error: {error}\n")


# Execute main when run as a script; importing the file does not run it.
if __name__ == "__main__":
    main()
```

## How the functions, inputs and variables work

`inspect_source_page(source_id, pdf_page)` accepts an approved manifest identifier
and a one-based physical PDF page. It prints evidence and text and returns None.
It raises an error for invalid input, missing/changed files, unknown sources or
unusable pages. `main()` accepts no Python parameters; it parses command-line
arguments, calls the inspector and reports expected errors with a nonzero exit.

| Item | Purpose / why |
|---|---|
| argparse | Convert explicit --source / --page arguments into named inputs; page must parse as an integer |
| hashlib.sha256(...).hexdigest() | Fingerprint the source bytes in hexadecimal for comparison with the approved manifest |
| json.loads(...) | Read the existing configuration into Python dictionaries/lists |
| Path(__file__).resolve().parents[1] | Locate the repository relative to this file in scripts/, even when the working directory differs |
| source / candidate | Select a configured source rather than construct a path from an arbitrary supplied identifier |
| pdf_bytes | Read once, then hash and parse the same bytes instead of reopening a potentially different file |
| actual_hash | Actual fingerprint; must match the configured source version before parsing |
| printed_page | Explicit known mapping; unknown stays None, displayed as not mapped |
| document / page_count | Open approved PDF and validate its physical page range |
| page_index | Convert human page 5 to library index 4 |
| text | Extracted embedded text copied into a string; no OCR or model inference |
| with | Close the PDF automatically, including when an operation fails |
| try / except | Surface expected input/file errors without pretending the command succeeded |
| __name__ guard | Run the entry point only when executed directly |
| -> None | The inspector prints results rather than returning a reusable evidence object; that contract comes in Step 4 |

We do not define a custom class because two focused functions are sufficient.
Sorting helps reading order, but does not guarantee that table columns, year
headers or visual labels are completely recovered. A hash proves the file matches
the approved version; it does not independently establish that its claims are true.

## Run the known monthly page

After saving, run:

```powershell
.\.venv\Scripts\python.exe .\scripts\inspect_source_page.py --source gacl_dahej_plot3_ec_2025_h1 --page 5
```

Expected metadata: the configured monthly source, scope dahej_plot3_report,
SHA-256 MATCH, PDF page 5, printed page 4 and 21 physical pages. The text should
contain the monthly freshwater table, KL/day context and April–September rows.
Look for April's 12540.8 value, allowing the report's actual printed formatting.
This lesson does not change the PDF, warehouse, exports or logs and does not
generate artificial values or interpretations.

## Verify input handling and existing behavior

A safe invalid-input check does not require editing a PDF:

```powershell
# Page zero is invalid for the human-facing page parameter.
.\.venv\Scripts\python.exe .\scripts\inspect_source_page.py --source gacl_dahej_plot3_ec_2025_h1 --page 0

# Inspect this immediately after the invalid-input command.
$LASTEXITCODE
```

Expected: Error: PDF page must be 1 or greater. Exit code 1 is expected for this
specific negative check. An unexpected error on the valid page-5 command remains
a failure to inspect before proceeding.

After adding the script, run the required existing regression suite:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
git status --short --branch
```

The baseline had 32 passing tests. These existing tests protect original behavior;
they do not specifically test the new inspector. The real page run and invalid
input run above verify this lesson's new behavior. Expect Git to list the new
scripts file/folder as untracked, while PDFs/databases remain ignored. Do not
commit raw PDFs, copied report text, databases or execution logs.

## Stop, explain and share

Send metadata plus the relevant extracted water-table lines, invalid-input
result/exit code, test summary and Git status. Explain why page 5 becomes index 4
and why the same bytes are hashed and parsed. We review these before the Step 3
checkpoint or Step 4. No code file is published by the assistant; it belongs to
the learner's implementation. This sample has been reviewed against the
referenced interfaces, but is not claimed to have been executed in this lesson.

References: [PyMuPDF document](https://pymupdf.readthedocs.io/en/latest/document.html),
[page text extraction](https://pymupdf.readthedocs.io/en/latest/page.html),
[Python 3.11 hashlib](https://docs.python.org/3.11/library/hashlib.html).
