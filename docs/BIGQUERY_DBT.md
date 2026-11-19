# BigQuery and dbt — next milestone

Status: optional loader and model files are prepared. They have not been executed against a live BigQuery project. Local verification is separate.

## Prerequisites

Choose your own Google Cloud project and confirm billing/sandbox constraints, dataset location and intended permissions before running. The loader creates the named dataset if absent, creates an observations table, uses a temporary staging table, and merges validated output. It does not delete the target dataset or its records.

Use Application Default Credentials. Do not add a service-account key to Git.

Official references:
- https://docs.cloud.google.com/bigquery/docs/authentication
- https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client
- https://docs.getdbt.com/docs/local/connect-data-platform/bigquery-setup

## Windows setup

After installing the official Google Cloud CLI and selecting the intended account/project:

```powershell
gcloud auth application-default login
$env:GCP_PROJECT_ID = "replace-with-your-project"
$env:BQ_DATASET = "gacl_public_disclosures"
$env:BQ_LOCATION = "asia-south1"
.\.venv\Scripts\python.exe -m pip install -e ".[cloud]"
.\.venv\Scripts\python.exe -m gacl_pipeline
.\.venv\Scripts\python.exe -m gacl_pipeline.bigquery_load
```

Location is an example, not an assertion about GACL's hosting. It must match the actual dataset location.

## dbt setup

Prefer a separate virtual environment for dbt to isolate optional dependencies:

```powershell
py -3.12 -m venv .venv-dbt
.\.venv-dbt\Scripts\python.exe -m pip install -e ".[dbt]"
Copy-Item dbt/profiles.yml.example dbt/profiles.yml
.\.venv-dbt\Scripts\dbt.exe debug --project-dir dbt --profiles-dir dbt
.\.venv-dbt\Scripts\dbt.exe build --project-dir dbt --profiles-dir dbt
```

Export the environment variables in the same PowerShell session. The profile uses OAuth/ADC. The raw source and model views use the chosen dataset; the loader writes observations, and dbt writes stg_observations plus monthly/annual views.

Core dependency is pinned; optional dependency ranges still need a resolved cloud environment and verification before being called reproducible cloud deployment.

## Cloud acceptance checks

- Confirm correct account, project and dataset location.
- Load all 18 observations and run dbt checks.
- Rerun the cloud load; observation/source/version keys remain unique.
- Reconcile source, SQLite, BigQuery and dbt results.
- Record adapter versions, job results and query costs.
- Update STATUS.md only after successful execution.

The staging table is cleaned up in a finally block. This loader does not implement a distributed transaction with local execution or an automatic preferred-revision policy.

