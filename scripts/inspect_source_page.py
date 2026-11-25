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