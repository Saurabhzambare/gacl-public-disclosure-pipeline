# GACL Public-Disclosure Data Pipeline

A data engineering portfolio project by **Saurabh Zambare** that turns GACL's public water and energy disclosures into traceable, validated observations.

**Current status:** the local Python → SQLite → CSV pipeline works with **18 real observations** from two official reports. BigQuery/dbt deployment and the Power BI report are next milestones, not completed claims.

This is independent work using public disclosures; it is not affiliated with or commissioned by GACL.

## What the project demonstrates

- Downloaded PDFs verified against pinned SHA-256 checksums.
- Deterministic, document-specific text extraction with source/page lineage.
- Exact decimal parsing, including Indian number formatting.
- Separate monthly site rates and annual company totals.
- Validation, quarantine files, bounded download retries and run history.
- Duplicate-safe local loads and reloads of individual historical sources.
- A credential-free local path, with optional BigQuery/dbt setup files.

## Billing-free BigQuery route

The optional loader now requires an explicit mode. `--mode snapshot` uploads the
complete validated local export with one batch replacement job and executes no
DML, so it is intended for the user's billing-free sandbox. The cloud table is a
copy of the local export, not an independent history store. Live cloud execution
is still pending. Follow [BigQuery setup](docs/BIGQUERY_DBT.md).

## The data

| Dataset | Grain | Initial coverage |
|---|---|---|
| Dahej Plot 3 freshwater consumption | Monthly average daily rate, KL/day | Six months, April–September 2025 |
| GACL standalone energy and water disclosures | Annual totals, GJ or KL | Six metrics × two financial years |

Source links, PDF pages, checksums and definitions: [source register](docs/SOURCES.md) and [data dictionary](docs/DATA_DICTIONARY.md).

These are historical public disclosures, not SAP transactions, a sensor feed or live SCADA data.

## Quick start

Python **3.11 or newer** is required. Development was verified on Python 3.12.14.

### Windows PowerShell

Clone this public repository with GitHub Desktop, or run:

```powershell
git clone https://github.com/Saurabhzambare/gacl-public-disclosure-pipeline.git
cd gacl-public-disclosure-pipeline
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m gacl_pipeline
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

### macOS / Linux

```bash
git clone https://github.com/Saurabhzambare/gacl-public-disclosure-pipeline.git
cd gacl-public-disclosure-pipeline
python3 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/python -m gacl_pipeline
.venv/bin/python -m unittest discover -s tests -v
```

The first run downloads approximately 14 MB of public PDFs. Later runs reuse checksum-verified cached files. No cloud credentials are needed.

On Windows, the downloader uses native certificate validation through pinned
`truststore`. After pulling this update into an existing clone, rerun
`python -m pip install -e .` using that clone's virtual-environment interpreter.
Certificate and document checksum verification remain enabled.

If HTTPS certificate verification blocks the report download, explicitly use the
reviewed extracts already included in the repository:

```powershell
.\.venv\Scripts\python.exe -m gacl_pipeline --from-examples
```

This mode makes no network requests. It checks the CSV snapshots against pinned
normalized-text checksums, validates their records, and runs the same warehouse
load and reporting exports. Expected: `input_mode: reviewed_extracts`,
`loaded_rows: 18`, `warehouse_rows: 18`, `extracted_rows: 0` and
`pdfs_verified_this_run: false`. The original PDF lineage is preserved, but this
does not claim a fresh PDF download or verification. See [HTTPS troubleshooting](docs/HTTPS_TROUBLESHOOTING.md).

Expected first-run output: `status: success`, `extracted_rows: 18`, `warehouse_rows: 18` and four passing dataset-level checks. Run identifiers and times vary.

After a successful first run, use `--offline` to avoid downloads. For a historical source reload:

```powershell
.\.venv\Scripts\python.exe -m gacl_pipeline --offline --source gacl_dahej_plot3_ec_2025_h1
```

Use `--refresh` to re-download against the pinned checksum. A changed source stops the run for review.

## Outputs

- `data/warehouse/gacl.sqlite`: local observations and execution history.
- `data/processed/monthly_site_observations.csv`: six monthly site rates.
- `data/processed/annual_company_observations.csv`: twelve annual totals.
- `data/processed/observations.json`: all accepted observations.
- `data/processed/run_manifest.json`: input mode and whether PDFs were verified in this run.
- `logs/latest_run.json`: latest outcome.
- `logs/<run_id>.checks.json`, `.quarantine.json` and `.log`: quality and diagnostic evidence.

Generated PDFs, databases, exports, environments and logs are ignored by Git. A reviewed, generated snapshot in [data/examples](data/examples/) provides an inspectable example; it is not a replacement for the extraction pipeline.

## Documentation

| Guide | Purpose |
|---|---|
| [Setup](docs/SETUP.md) | Windows/GitHub Desktop and Linux setup |
| [Architecture](docs/ARCHITECTURE.md) | Pipeline stages and storage decisions |
| [Data dictionary](docs/DATA_DICTIONARY.md) | Field definitions, grains and units |
| [Sources](docs/SOURCES.md) | Official reports, checksums and extraction pages |
| [Quality and testing](docs/TESTING.md) | Checks, failure cases and commands |
| [Operations runbook](docs/RUNBOOK.md) | Reruns, failures and source changes |
| [Cloud setup](docs/BIGQUERY_DBT.md) | Optional BigQuery loader and dbt configuration |
| [Power BI specification](dashboard/README.md) | Two-page dashboard plan |
| [Build plan](docs/PROJECT_PLAN.md) | Target: 22 November 2026 |
| [Status](docs/STATUS.md) | Verified work and remaining tasks |
| [Decisions](docs/DECISIONS.md) | Scope, precision and provenance choices |
| [Security](SECURITY.md) | Credentials and data handling |
| [Contributing](CONTRIBUTING.md) | Development and review checklist |

## Boundaries

The parsers support the two pinned documents, not arbitrary PDFs. Missing months are not synthesized. Annual totals are not distributed across plants or months. Source changes require manual review before a manifest update. A changed document is detected but not automatically accepted.

The dataset is deliberately small; the case study is about engineering correctness, not throughput or forecasting. See [status](docs/STATUS.md) before making resume claims.

Original project code is MIT licensed. GACL reports, branding and source material retain their owners' rights; they are not covered by that license.

