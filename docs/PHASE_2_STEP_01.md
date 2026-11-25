# Phase 2 — Step 1: Check the existing Windows environment

Build-order version: 1.0. Lesson prepared: 25 November 2026 (India).
Execution: **passed on the learner's Windows laptop, 25 November 2026**.
The author supplied Python 3.11.4, virtual environment True, PyMuPDF 1.26.6,
FTS5 available, two configured sources and both PDFs PRESENT. No source hash
verification or AI index/model run is established by this readiness result.
The understanding discussion is recorded separately in the learning log.
The reusable instructions below remain available for another environment.

## Purpose

Identify the real checkout, interpreter, installed PDF package, SQLite search
capability and source-file presence before creating application code. A missing
prerequisite should be repaired before the first PDF-reading exercise.

ELI5: check the toolbox and the two books before building the assistant.

## Required tools and files

Reuse the existing project at `D:\gacl-public-disclosure-pipeline`, PowerShell,
Python 3.11+ in its `.venv`, PyMuPDF 1.26.6 and Python's SQLite with FTS5.
The original project already declares its dependencies in `pyproject.toml`.
No new installation is assumed necessary. No source file, API key, GPU runtime,
model, vector database or cloud account is needed for this check.

The check reads `config/sources.json` and checks configured paths under
`data/raw`. It creates only a temporary in-memory SQLite table; it does not
write a database file, modify a PDF, build an index or verify source hashes yet.

## A. Inspect the checkout and locate its interpreter

Open PowerShell and run:

```powershell
# Move into the existing repository. Adjust only if your actual location differs.
Set-Location "D:\gacl-public-disclosure-pipeline"

# Identify the current branch and pre-existing changes without changing them.
git status --short --branch
git log -1 --oneline

# Confirm that this clone's Python executable exists.
Test-Path ".\.venv\Scripts\python.exe"
```

The last command should print `True`. If it prints `False`, stop and share the
output; first locate or restore the environment rather than running dependent
commands. Do not discard changes, recreate the environment, pull or switch
branches merely to match the assistant's reference workspace.

## B. Run the commented readiness check

Paste this complete block in the same PowerShell window. No file needs to be
created. The PowerShell here-string holds Python source; the final pipe sends
it to the explicitly selected interpreter. The final `-` means read source from
standard input.

```powershell
@'
"""Inspect prerequisites without modifying project files or databases."""

import json
import sqlite3
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path


def main() -> None:
    """Print environment and file-presence information.

    Parameters:
        None. The function inspects the interpreter and current directory.

    Returns:
        None. Results are printed; a failed prerequisite stops this function.
    """

    # version_info lets us check the minimum without comparing version strings.
    print("Python version:", sys.version.split()[0])
    if sys.version_info < (3, 11):
        print("FAIL: This project requires Python 3.11 or newer.")
        return

    # Different prefixes normally identify a virtual-environment interpreter.
    using_virtual_environment = sys.prefix != sys.base_prefix
    print("Using a virtual environment:", using_virtual_environment)
    if not using_virtual_environment:
        print("FAIL: Use the project's .venv interpreter.")
        return

    try:
        # PyMuPDF is the installed package; fitz is its existing import name here.
        import fitz

        # Check installed metadata as well as whether the library can load.
        print("PyMuPDF version:", version("PyMuPDF"))
    except (ImportError, PackageNotFoundError) as error:
        print("FAIL: PyMuPDF is unavailable or cannot load:", error)
        return

    # :memory: creates a temporary database without a filesystem artifact.
    connection = sqlite3.connect(":memory:")
    try:
        # Creating a virtual table tests the interpreter's FTS5 capability.
        connection.execute(
            "CREATE VIRTUAL TABLE readiness_check USING fts5(content)"
        )
        print("SQLite FTS5: available")
    except sqlite3.OperationalError as error:
        print("FAIL: SQLite FTS5 check failed:", error)
        return
    finally:
        # Always release the connection, including on a failed capability check.
        connection.close()

    # Resolve paths from the current repository folder, not a hard-coded username.
    project_root = Path.cwd()
    source_register_path = project_root / "config" / "sources.json"
    if not source_register_path.is_file():
        print("FAIL: config/sources.json was not found in this project folder.")
        return

    try:
        # JSON configuration becomes Python dictionaries and lists.
        source_register = json.loads(
            source_register_path.read_text(encoding="utf-8")
        )
        configured_sources = source_register["sources"]
    except (OSError, json.JSONDecodeError, KeyError) as error:
        print("FAIL: Could not read the existing source register:", error)
        return

    print("Configured sources:", len(configured_sources))
    for source in configured_sources:
        # The existing approved source ID determines its cached filename.
        pdf_path = project_root / "data" / "raw" / f"{source['source_id']}.pdf"

        # Presence is not integrity: hash verification belongs to Step 3.
        file_status = "PRESENT" if pdf_path.is_file() else "MISSING"
        print(f"Cached PDF: {source['source_id']} -> {file_status}")


# Direct execution invokes our entry point; importing a file would not.
if __name__ == "__main__":
    main()
'@ | .\.venv\Scripts\python.exe -
```

The code has no classes because a simple diagnostic function is sufficient. It
does not declare the whole environment valid just because it printed something;
review the complete output, dependency version and both PDF-presence lines.

## C. Expected evidence and meaning

```text
Python version: 3.11.4
Using a virtual environment: True
PyMuPDF version: 1.26.6
SQLite FTS5: available
Configured sources: 2
Cached PDF: gacl_dahej_plot3_ec_2025_h1 -> PRESENT
Cached PDF: gacl_brsr_2025_26 -> PRESENT
```

The Python patch/minor version can differ if it meets the project's minimum.
An unexpected package version requires review against `pyproject.toml`, not an
automatic upgrade of everything. Missing PDFs require locating/recovering the
approved bytes before text extraction. A traceback or `FAIL` is useful evidence;
do not suppress it or mark the step complete.

## D. Understanding check and stopping point

Explain why we invoke `.venv\Scripts\python.exe`, why an in-memory table leaves
no index file, and why `PRESENT` does not prove a PDF matches its approved hash.
Share terminal output from A and B. Stop here; do not create the inspection script
yet. After review, record results in [the learning log](AI_LEARNING_LOG.md) and
continue to [Step 2](PHASE_2_BUILD_ORDER.md#step-2--record-a-baseline-and-isolate-personal-implementation).

Concept help: [AI_CONCEPTS.md](AI_CONCEPTS.md). This lesson's commands do not
publish a branch, enable billing or perform an AI/model inference call.
