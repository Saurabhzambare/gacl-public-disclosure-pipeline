"""Optional cloud loader. Prepared for the next milestone; requires ADC."""
import argparse
import json
import os
import re
from pathlib import Path
from uuid import uuid4

from .store import COLUMNS
from .validate import reconcile, validate_rows


def main(argv=None):
    parser = argparse.ArgumentParser(description="Load validated local outputs into BigQuery")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--project", default=os.environ.get("GCP_PROJECT_ID"))
    parser.add_argument("--dataset", default=os.environ.get("BQ_DATASET", "gacl_public_disclosures"))
    parser.add_argument("--location", default=os.environ.get("BQ_LOCATION", "asia-south1"))
    args = parser.parse_args(argv)
    if not args.project or not re.fullmatch(r"[a-z][a-z0-9-]{4,61}[a-z0-9]", args.project) or args.project == "your-project-id":
        parser.error("Set a real GCP_PROJECT_ID or --project")
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]{0,1023}", args.dataset):
        parser.error("Invalid dataset identifier")
    root = args.root.resolve()
    rows = json.loads((root / "data/processed/observations.json").read_text())
    metrics = json.loads((root / "config/metrics.json").read_text())
    sources = json.loads((root / "config/sources.json").read_text())["sources"]
    valid, rejected = validate_rows(rows, metrics, sources)
    checks = reconcile(valid, {r["source_id"] for r in valid})
    if not valid or rejected or any(not c["passed"] for c in checks):
        raise ValueError("Refusing cloud load: local outputs failed validation")
    try:
        from google.cloud import bigquery
    except ImportError as exc:
        raise SystemExit('Install cloud dependencies: python -m pip install -e ".[cloud]"') from exc
    client = bigquery.Client(project=args.project, location=args.location)
    dataset_id = f"{args.project}.{args.dataset}"
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = args.location
    client.create_dataset(dataset, exists_ok=True)
    actual = client.get_dataset(dataset_id)
    if actual.location.casefold() != args.location.casefold():
        raise ValueError("Existing dataset location differs from --location")
    schema = [bigquery.SchemaField(k, "INT64" if k in ("pdf_page", "printed_page") else "STRING", mode="REQUIRED") for k in COLUMNS]
    target = dataset_id + ".observations"
    staging = dataset_id + "._load_" + uuid4().hex
    client.create_table(bigquery.Table(target, schema=schema), exists_ok=True)
    try:
        job = client.load_table_from_json(valid, staging, job_config=bigquery.LoadJobConfig(
            schema=schema, write_disposition="WRITE_TRUNCATE"))
        job.result()
        fields = ",".join(f"`{k}`" for k in COLUMNS)
        update = ",".join(f"T.`{k}`=S.`{k}`" for k in COLUMNS if k not in ("observation_id", "source_id", "document_sha256"))
        values = ",".join(f"S.`{k}`" for k in COLUMNS)
        query = f"""MERGE `{target}` T USING `{staging}` S
          ON T.observation_id=S.observation_id AND T.source_id=S.source_id
          AND T.document_sha256=S.document_sha256
          WHEN MATCHED THEN UPDATE SET {update}
          WHEN NOT MATCHED THEN INSERT ({fields}) VALUES ({values})"""
        client.query(query, job_config=bigquery.QueryJobConfig(maximum_bytes_billed=1_000_000_000)).result()
    finally:
        client.delete_table(staging, not_found_ok=True)
    print(json.dumps({"target": target, "merged_rows": len(valid), "location": args.location}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

