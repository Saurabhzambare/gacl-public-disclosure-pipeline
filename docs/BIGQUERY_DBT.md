# BigQuery and dbt

Status: local PDF processing works. The user has verified the live BigQuery
table contains 12 annual and 6 monthly rows, no duplicate version keys, and
18 total rows after the requested rerun check. On 22 November, dbt debug passed
and the live build created 3 views with 7 passing SQL tests, no warnings/errors
or skipped resources. All eight live reference checks passed, as shown in the user's screenshot.
The 24 November rerun supplied actual load job ID and expiration evidence:
see [verification record](VERIFICATION_2026-11-24.md).

## Chosen route: billing-free sandbox

On 20 November 2026 the user confirmed Application Default Credentials (ADC),
project instacart-analytics-practice, billingEnabled=false, and installation of
google-cloud-bigquery 3.47.0. The user explicitly chose to keep billing disabled.
No command in this guide links a billing account or enables billing.

The sandbox does not support DML, so use --mode snapshot rather than MERGE.
The loader validates the complete local data/processed/observations.json export,
including coverage of both configured reports, before contacting Google Cloud.
It then sends one batch load with WRITE_TRUNCATE to the observations table.
A successful refresh replaces that table's contents with the validated export;
it does not append a second copy. A rejected load does not first delete the old
table. BigQuery applies batch load results atomically.

This is a full refresh, not incremental upsert. Cloud-only rows absent from the
local export are replaced. Source versions remain in local SQLite; uploading
multiple conflicting document versions requires a reviewed selection policy and
is currently rejected by validation. Keep local source and warehouse artifacts.

Sandbox tables/views/partitions expire after 60 days and sandbox quotas apply.
Reloading data is not a backup strategy. Inspect the reported table_expires_at.
No paid capacity reservation, Cloud Storage bucket or streaming API is needed.

Official references:
- https://docs.cloud.google.com/bigquery/docs/authentication
- https://docs.cloud.google.com/bigquery/docs/sandbox
- https://docs.cloud.google.com/bigquery/docs/batch-loading-data
- https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client
- https://docs.getdbt.com/docs/local/connect-data-platform/bigquery-setup

## Windows setup and first load

Authentication and the cloud package are already installed on the user's laptop.
For another machine, use gcloud auth application-default login and install the
cloud extra. Never commit credential files.

Run from the repository root, stopping if any command fails:

```powershell
git pull --ff-only
.\.venv\Scripts\python.exe -m pip install -e ".[cloud]"
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
$env:GCP_PROJECT_ID = "instacart-analytics-practice"
$env:BQ_DATASET = "gacl_public_disclosures"
$env:BQ_LOCATION = "asia-south1"
.\.venv\Scripts\python.exe -m gacl_pipeline.bigquery_load --mode snapshot
```

The chosen location is Mumbai for this portfolio dataset, not an assertion about
GACL's hosting. An existing dataset must have the same location; a mismatch stops
before upload. The loader creates only the named dataset if missing and loads its
observations table. Other datasets, including Instacart tables, are not modified.
It does not enable APIs automatically; if a missing-API error occurs, inspect that
error and enable only the BigQuery API for the intended project as needed.

Expected loader summary: load_mode=snapshot, loaded_rows=18,
warehouse_rows=18, four passing checks and a real job_id. The user has verified
the live table counts; retain the actual job ID from the terminal. A success summary is
written to logs/bigquery_latest_run.json, which is ignored by Git. This file
records the latest successful snapshot load, not later failed attempts.

Run the same load command again and confirm 18 rows remain. These shell variables
must be set again if a new PowerShell session is opened. .env.example is only a
template and is not automatically loaded.

## Inspect the data in BigQuery

Open https://console.cloud.google.com/bigquery?project=instacart-analytics-practice
and inspect gacl_public_disclosures.observations. The raw schema preserves dates
and decimal values as strings; page fields are INT64. dbt will provide typed views.

```sql
SELECT frequency, COUNT(*) AS observation_count
FROM `instacart-analytics-practice.gacl_public_disclosures.observations`
GROUP BY frequency;
-- Expected: annual 12, monthly 6.

SELECT observation_id, source_id, document_sha256, COUNT(*) AS copies
FROM `instacart-analytics-practice.gacl_public_disclosures.observations`
GROUP BY observation_id, source_id, document_sha256
HAVING COUNT(*) > 1;
-- Expected: no rows, including after a second snapshot load.
```

The SELECT queries use sandbox query quota. The snapshot upload itself executes
no SQL queries. Reconcile selected values, units, dates and source pages against
SQLite, not only the row count. Record load job IDs, expiration and actual results.

## Optional MERGE mode

--mode merge retains the original staged SQL upsert, and requires DML support.
It is outside the user's chosen billing-free route. There is no automatic
fallback from snapshot to MERGE or from an error to a different write mode.
Mode selection is mandatory to make replacement versus upsert explicit.

## dbt setup — after the cloud load is verified

Prefer a separate virtual environment; Python 3.11 is installed on the user's
laptop. Core 1.12.7 and adapter 1.12.4 are pinned. The previous broad adapter
range selected beta Core 1.13.0b1 on the user's laptop. Pull the updated metadata
and reinstall the dbt extra to use the stable pair. Keep the environment variables
and dataset location in the same PowerShell session.

```powershell
py -3.11 -m venv .venv-dbt
.\.venv-dbt\Scripts\python.exe -m pip install -e ".[dbt]"
$env:GCP_PROJECT_ID = "instacart-analytics-practice"
$env:BQ_DATASET = "gacl_public_disclosures"
$env:BQ_LOCATION = "asia-south1"
if (!(Test-Path dbt/profiles.yml)) { Copy-Item dbt/profiles.yml.example dbt/profiles.yml }
.\.venv-dbt\Scripts\dbt.exe --version
.\.venv-dbt\Scripts\dbt.exe debug --project-dir dbt --profiles-dir dbt
.\.venv-dbt\Scripts\dbt.exe build --project-dir dbt --profiles-dir dbt
```

Models are configured as views; do not switch to incremental/DML models in the
sandbox. The source table is observations, and dbt creates stg_observations plus
separate monthly/annual reporting views. On 22 November the user verified
Connection test OK and a completed build: 3 views, 7 passing data tests,
PASS=10 WARN=0 ERROR=0 SKIP=0. This is actual user terminal evidence with
Core 1.12.7, adapter 1.12.4 and Windows/Python 3.11.4.
Development parse succeeded on Linux/Python 3.12 with the pinned pair, finding
three models and seven SQL tests. A successful parse checks project structure and references without querying
BigQuery; it is not a successful database connection or build.

## Final read-only reference comparison

Open sql/bigquery_verification.sql and run its entire SELECT query in BigQuery.
It embeds the 18 reviewed facts from the checksum-pinned repository extracts
and compares each relation in both directions using EXCEPT DISTINCT. It checks
values, periods, units and reporting scopes, not just record counts.

Expected eight result rows, all passed=true:
- observations: 18 rows, 0 differing facts.
- stg_observations: 18 rows, 0 differing facts.
- monthly_site_observations: 6 rows, 0 differing facts.
- annual_company_observations: 12 rows, 0 differing facts.

The query does not change tables or settings and consumes only normal SELECT
query quota. It is tied to the current project and approved 18 facts; review it
when adding reports or changing the source manifest. It does not compare every
provenance column, certify regulatory compliance or prove operational causes.
On 22 November the user supplied a screenshot of all eight results with
passed=true, the expected counts and zero differing facts.

## Acceptance checks

- Confirm the correct project, ADC account and dataset location.
- Load all 18 observations and inspect the reported job and table count.
- Rerun the snapshot; counts and observation/source/version keys remain unchanged.
- Reconcile source, SQLite, BigQuery and dbt values; run dbt checks.
- Record dependency versions, job results, expiration and query usage.
- Update STATUS.md with actual results before claiming cloud deployment.

There is no distributed transaction across SQLite and BigQuery. Concurrent
snapshot writers are unsupported; the last successful replacement wins.
