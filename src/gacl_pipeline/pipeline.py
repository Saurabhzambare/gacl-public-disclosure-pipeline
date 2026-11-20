"""Offline-first execution; no cloud account is needed for the local pipeline."""
import csv
import hashlib
import json
import logging
import ssl
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from .extract import extract_pdf
from .examples import load_examples
from .store import COLUMNS, connect, finish_run, load, start_run
from .validate import reconcile, validate_rows


def utcnow():
    return datetime.now(timezone.utc).isoformat()


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def create_https_context():
    """Use Windows chain validation without changing process-wide SSL behavior."""
    if sys.platform == "win32":
        import truststore
        return truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    return ssl.create_default_context()


def download(source, raw_dir, refresh=False):
    path = Path(raw_dir) / (source["source_id"] + ".pdf")
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not refresh:
        if sha256(path) != source["sha256"]:
            raise ValueError(f"Checksum mismatch for cached {source['source_id']}")
        return path
    context = create_https_context()
    # Bounded retry only for transient network failures. A changed document is not retried.
    for attempt in range(3):
        try:
            request = urllib.request.Request(source["url"], headers={"User-Agent": "GACL-Public-Disclosure-Portfolio/0.1"})
            with urllib.request.urlopen(request, timeout=45, context=context) as response:
                data = response.read(25 * 1024 * 1024 + 1)
            if len(data) > 25 * 1024 * 1024 or not data.startswith(b"%PDF"):
                raise ValueError("Response is not an allowed PDF")
            if hashlib.sha256(data).hexdigest() != source["sha256"]:
                raise ValueError("Source changed: checksum mismatch; review before updating manifest")
            temp = path.with_suffix(".pdf.tmp")
            temp.write_bytes(data)
            temp.replace(path)
            write_json(path.with_suffix(".retrieval.json"),
                       {"source_id": source["source_id"], "url": source["url"], "retrieved_at": utcnow(), "sha256": source["sha256"]})
            return path
        except urllib.error.HTTPError as exc:
            if exc.code not in (408, 429, 500, 502, 503, 504) or attempt == 2:
                raise
        except ssl.SSLCertVerificationError as exc:
            raise ValueError("HTTPS certificate verification failed for " + source["url"] +
                             ". Check the computer clock and certificate chain. "
                             "To use reviewed extracts without downloading PDFs, run: "
                             "python -m gacl_pipeline --from-examples") from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            if isinstance(getattr(exc, "reason", None), ssl.SSLCertVerificationError):
                raise ValueError("HTTPS certificate verification failed for " + source["url"] +
                                 ". Check the computer clock and certificate chain. "
                                 "To use reviewed extracts without downloading PDFs, run: "
                                 "python -m gacl_pipeline --from-examples") from exc
            if attempt == 2:
                raise
        time.sleep(2 ** attempt)
    raise RuntimeError("Download retry budget exhausted")


def run(root, source_id=None, offline=False, refresh=False, from_examples=False):
    root = Path(root).resolve()
    if sum(bool(x) for x in (offline, refresh, from_examples)) > 1:
        raise ValueError("--offline, --refresh and --from-examples cannot be combined")
    sources = json.loads((root / "config/sources.json").read_text(encoding="utf-8"))["sources"]
    metrics = json.loads((root / "config/metrics.json").read_text(encoding="utf-8"))
    selected = [s for s in sources if source_id is None or s["source_id"] == source_id]
    if not selected:
        raise ValueError(f"Unknown source: {source_id}")
    run_id = str(uuid4())
    log_dir = root / "logs"
    log_dir.mkdir(exist_ok=True)
    handler = logging.FileHandler(log_dir / f"{run_id}.log", encoding="utf-8")
    logger = logging.getLogger("gacl_pipeline")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    db = connect(root / "data/warehouse/gacl.sqlite")
    input_mode = "reviewed_extracts" if from_examples else ("cached_pdfs" if offline else "verified_pdfs")
    start_run(db, run_id, utcnow(), [s["source_id"] for s in selected], input_mode)
    count = 0
    try:
        rows = []
        if from_examples:
            rows = load_examples(root, {s["source_id"] for s in selected})
            logger.info("reviewed_extracts_loaded rows=%d; no PDFs verified this run", len(rows))
        for source in selected:
            if from_examples:
                continue
            logger.info("source_start source_id=%s", source["source_id"])
            path = root / "data/raw" / (source["source_id"] + ".pdf")
            if offline:
                if not path.exists() or sha256(path) != source["sha256"]:
                    raise ValueError(f"Offline source missing or checksum mismatch: {source['source_id']}")
            else:
                path = download(source, root / "data/raw", refresh=refresh)
            extracted = extract_pdf(path, source)
            rows.extend(extracted)
            logger.info("source_extracted source_id=%s rows=%d", source["source_id"], len(extracted))
        valid, rejected = validate_rows(rows, metrics, sources)
        checks = reconcile(valid, {s["source_id"] for s in selected})
        write_json(log_dir / f"{run_id}.quarantine.json", rejected)
        write_json(log_dir / f"{run_id}.checks.json", checks)
        if rejected or any(not c["passed"] for c in checks):
            raise ValueError(f"Validation failed: {len(rejected)} rejected rows; inspect run artifacts")
        load(db, valid)
        count = len(valid)
        # Export all accepted history. Distinct source versions are preserved, not silently preferred.
        exported = [dict(row) for row in db.execute("SELECT * FROM observations ORDER BY frequency,metric_id,period_start")]
        out = root / "data/processed"
        out.mkdir(parents=True, exist_ok=True)
        for name, subset in (
            ("observations", exported),
            ("monthly_site_observations", [r for r in exported if r["frequency"] == "monthly"]),
            ("annual_company_observations", [r for r in exported if r["frequency"] == "annual"]),
        ):
            with (out / f"{name}.csv").open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=COLUMNS)
                writer.writeheader()
                writer.writerows(subset)
        write_json(out / "observations.json", exported)
        write_json(out / "source_register.json", sources)
        finish_run(db, run_id, utcnow(), "success", count)
        summary = {"run_id": run_id, "status": "success",
                   "input_mode": input_mode, "pdfs_verified_this_run": not from_examples,
                   "extracted_rows": 0 if from_examples else count, "loaded_rows": count,
                   "warehouse_rows": len(exported), "checks": checks}
        write_json(out / "run_manifest.json", summary)
        write_json(log_dir / "latest_run.json", summary)
        logger.info("run_success rows=%d warehouse_rows=%d", count, len(exported))
        return summary
    except Exception as exc:
        logger.exception("run_failed")
        finish_run(db, run_id, utcnow(), "failed", count, f"{type(exc).__name__}: {exc}")
        write_json(log_dir / "latest_run.json",
                   {"run_id": run_id, "status": "failed", "input_mode": input_mode,
                    "error": f"{type(exc).__name__}: {exc}"})
        raise
    finally:
        db.close()
        logger.removeHandler(handler)
        handler.close()

