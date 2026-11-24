# End-to-end verification — 24 November 2026

Outcome: the author completed a manual sequence from cached source PDFs through
local extraction/loading, BigQuery snapshot loading, dbt, reference comparison
and Power BI Desktop refresh.

Evidence consists of terminal output supplied by the author, a BigQuery results
screenshot, a Power BI Sources & Coverage screenshot, and explicit confirmation
that Home > Refresh completed without errors. This is a curated evidence record;
it is not an independently executed cloud audit or an automated orchestration
log. Only the local stage has the pipeline run_id below. No common cross-stage
run identifier or recorded video is claimed.

## 1. Local extraction and validation

Command, from the Windows repository root:

```powershell
.\.venv\Scripts\python.exe -m gacl_pipeline --offline
```

| Field | Observed result |
|---|---|
| run_id | 686d38a0-30d6-4551-b6a9-25c7d89307e1 |
| status | success |
| input_mode | cached_pdfs |
| pdfs_verified_this_run | true |
| extracted_rows | 18 |
| loaded_rows | 18 |
| warehouse_rows | 18 |

| Dataset check | Result | Details |
|---|---|---|
| monthly_coverage | passed | Six unique months, April–September 2025 |
| annual_coverage | passed | Six annual totals for each of two financial years |
| energy_reconciliation_2024-04-01 | passed | Absolute difference 0.002 GJ; tolerance 0.01 GJ |
| energy_reconciliation_2025-04-01 | passed | Absolute difference 0.00 GJ; tolerance 0.01 GJ |

This run verified cached PDF checksums and extracted their data. It did not
redownload the reports. The 0.002 GJ difference is within the rounding tolerance;
reported source values remain unchanged.

## 2. BigQuery snapshot load

The author set GCP_PROJECT_ID=instacart-analytics-practice,
BQ_DATASET=gacl_public_disclosures and BQ_LOCATION=asia-south1, then ran:

```powershell
.\.venv\Scripts\python.exe -m gacl_pipeline.bigquery_load --mode snapshot
```

| Field | Observed result |
|---|---|
| target | instacart-analytics-practice.gacl_public_disclosures.observations |
| load_mode | snapshot |
| loaded_rows | 18 |
| warehouse_rows | 18 |
| location | asia-south1 |
| job_id | 2bfa8593-f4e7-4bd4-bd1b-6426ff209e18 |
| table_expires_at | 2027-01-19T06:05:47.607000+00:00 |

All four dataset checks above also passed in the loader summary. The expiration
is the actual value returned by this run; do not assume the load extended it.
The cloud copy is a full snapshot replacement, not an incremental MERGE or an
independent history store.

## 3. dbt models and SQL tests

```powershell
$env:DBT_SEND_ANONYMOUS_USAGE_STATS = "false"
.\.venv-dbt\Scripts\dbt.exe build --project-dir dbt --profiles-dir dbt
```

Observed versions: dbt Core 1.12.7 and BigQuery adapter 1.12.4. The terminal
reported three models and seven data tests, completing successfully:

```text
PASS=10 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=10
```

The individual model line for stg_observations reported NO-OP, reusing the
existing staging definition. annual_company_observations and
monthly_site_observations reported CREATE VIEW. All seven tests passed:

- no_duplicate_versions
- nonnegative_values
- not_null_stg_observations_observation_id
- not_null_stg_observations_reporting_scope
- not_null_stg_observations_source_url
- not_null_stg_observations_value
- energy_reconciliation

The terminal also reported dbt State adapter v2.65.0 enabled. The evidence
records that actual invocation; it does not claim a newly verified local
configuration without the State adapter.

## 4. Read-only reference comparison

The author ran the complete [reference script](../sql/bigquery_verification.sql)
in BigQuery after the load and dbt build. The screenshot shows Query completed
and eight results, every one with passed=true:

| Relation | Observed rows | Expected rows | Differing facts | Expected differences |
|---|---:|---:|---:|---:|
| observations | 18 | 18 | 0 | 0 |
| stg_observations | 18 | 18 | 0 | 0 |
| monthly_site_observations | 6 | 6 | 0 | 0 |
| annual_company_observations | 12 | 12 | 0 | 0 |

Each relation contributes a count check and a bidirectional fact-comparison
check. The comparison covers selected values, periods, units and scopes; it
does not independently compare every provenance column or establish regulatory
compliance. The eight checks are separate from the seven dbt tests and 32 Python
unit tests previously verified in CI.

## 5. Power BI Desktop refresh

After the cloud checks, the author refreshed the existing report. The supplied
Sources & Coverage screenshot shows 6 monthly, 12 annual and 18 total
observations, with the annual and monthly source-page references intact. The
author explicitly confirmed that Home > Refresh completed without errors.

The earlier exported two-page PDF and previews remain in [dashboard](../dashboard/).
They were reviewed before this rerun and were not replaced with a newly exported
PDF during this verification. Exact PBIX connection options and connectivity
mode have not been independently inspected. The PBIX remains on the author's
laptop; no hosted Power BI Service report is claimed.

## Remaining delivery work

- Record the prepared 3–5 minute [walkthrough](WALKTHROUGH.md).
- Share editable report source if desired; PBIX is currently excluded from Git.
- Scheduling and a hosted interactive report remain future work.

This verifies a manual execution sequence for the selected 18 historical public
disclosures. It does not imply live plant access, larger-scale throughput,
automated scheduling, or new operational impact.
