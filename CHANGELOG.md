# Changelog

## Power BI report and portfolio evidence — 24 November 2026

Add the author-supplied two-page Power BI PDF and page previews rendered from it.
Record successful Desktop refresh reported by the user and review of displayed
values, counts, units, source pages and four link annotations. Replace the
planned-dashboard description with the actual pages, DAX measures, formatting
and refresh guidance; update README/status/build-plan checkpoints and add a
walkthrough script. The PDF is unchanged, including the retained cosmetic
heading marks. Editable PBIX, a recorded video and a captured end-to-end rerun
remain pending. No pipeline code or test-count claims changed.

## Reference verification — 22 November 2026

Record the user's screenshot showing all eight BigQuery reference checks passed:
18 raw, 18 staged, 6 monthly and 12 annual rows, with zero differing facts in
each relation. Ignore generated dbt/.user.yml local metadata. Document Power BI
Import connection to the validated views with UseStorageApi=false and the exact
project, plus a manual cloud-view CSV fallback. Power BI remains unverified.

## Live dbt milestone — 22 November 2026

Record user-verified connection/build: 3 views created and 7 SQL data tests
passed, with no warnings, errors or skips. Add a read-only BigQuery reference
script with eight checks covering all 18 reviewed values, dates, units and
scopes across raw/staged/monthly/annual relations. Expected reference facts
passed snapshot checksum/contract checks; GoogleSQL syntax parsed locally.
Live execution of the reference script, Power BI and the walkthrough remain
pending. No additional Python or dbt test count is claimed for the manual SQL.

## Stable dbt setup — 20 November 2026

Pin dbt-core 1.12.7 and dbt-bigquery 1.12.4 after the broad adapter range
selected beta Core 1.13.0b1 on the user's Windows laptop. Record the user's
successful BigQuery count/duplicate/rerun queries, and distinguish them from
pending job-ID evidence, full value reconciliation and live dbt execution.
Document all profile environment variables and preserve an existing local profile.
Verified development parse with the stable pair: three models/seven SQL tests;
32 Python tests pass. Live dbt connection/build is still pending.

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

