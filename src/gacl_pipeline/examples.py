"""Load reviewed extracts explicitly; never claim a fresh PDF verification."""
import csv
import hashlib
import io
import json
from pathlib import Path


def load_examples(root, selected_source_ids):
    root = Path(root)
    manifest = json.loads((root / "config/examples.json").read_text(encoding="utf-8"))
    rows = []
    for item in manifest["files"]:
        if item["source_id"] not in selected_source_ids:
            continue
        path = root / item["path"]
        # Universal newline conversion keeps checksums stable on Windows and Linux.
        text = path.read_text(encoding="utf-8")
        if hashlib.sha256(text.encode("utf-8")).hexdigest() != item["normalized_text_sha256"]:
            raise ValueError(f"Reviewed extract checksum mismatch: {item['path']}")
        for row in csv.DictReader(io.StringIO(text)):
            if row["source_id"] != item["source_id"]:
                raise ValueError("Reviewed extract source does not match its manifest")
            for field in ("pdf_page", "printed_page"):
                row[field] = int(row[field])
            rows.append(row)
    if not rows:
        raise ValueError("No reviewed extracts found for selected source")
    return rows
