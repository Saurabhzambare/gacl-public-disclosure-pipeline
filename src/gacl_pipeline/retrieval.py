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