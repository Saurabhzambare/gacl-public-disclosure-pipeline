# Changelog

## Billing-free cloud mode — 20 November 2026

Add mandatory --mode snapshot or --mode merge selection. Snapshot validates both
configured sources before cloud calls, uses one WRITE_TRUNCATE batch load with
no DML, checks the resulting row count and records job/expiration evidence.
Seven mocked SDK-boundary tests bring the cloud-enabled suite to 32 tests.
Pin google-cloud-bigquery 3.47.0, matching the user's installed version. Update
CI to exercise cloud tests on Windows/Linux; live upload remains unverified.
Document replacement/history limits, sandbox expiration and Python 3.11 dbt setup.

## Update — 20 November 2026

Use pinned truststore 0.10.5 and an explicit native Windows TLS context for PDF
downloads, preserving certificate/hostname and source checksum checks. Other
platforms retain the default verified SSL context. Add three tests (25 total)
and Windows/Python 3.11 CI coverage. Record the user's successful full PDF run
with the temporary launcher; normal-command laptop confirmation remains pending.

## Update — 19 November 2026

Added an explicit --from-examples mode using checksum-pinned, reviewed repository CSVs. Run provenance distinguishes reviewed extracts from fresh PDF verification. Certificate errors fail immediately with actionable instructions. Added seven tests (22 total), a network-free CLI check in CI, HTTPS troubleshooting and Python 3.11 Windows instructions. Recorded the repository's public visibility.


## 0.1.0 — 19 November 2026

Initial local foundation: verified GACL report collection, targeted PDF extraction, 18 traceable observations, validation, SQLite storage, exports, failure logs, historical source reloads, 15 unit tests, example outputs and essential documentation.

Optional BigQuery/dbt files and a Power BI specification are included as the next milestones. They have not been verified against cloud services or Power BI Desktop.

