# Project status

Updated: 20 November 2026. First-version target: 22 November 2026, 8:00 PM IST.

## Implemented and verified locally

- [x] Two official GACL PDFs downloaded and SHA-256 verified.
- [x] BRSR standalone boundary visually confirmed on printed page 43.
- [x] Automatic extraction of 6 monthly water and 12 annual energy/water observations.
- [x] All 18 selected values reconciled to source tables.
- [x] Exact decimal normalization with raw values preserved.
- [x] Contract validation, monthly/annual coverage and energy reconciliation.
- [x] Transactional local SQLite warehouse.
- [x] Repeated load retains 18 rows without duplicates.
- [x] Individual source reload: 6 extracted monthly rows, 18 total warehouse rows.
- [x] Online refresh verifies pinned documents and creates retrieval sidecars.
- [x] Run history, diagnostic logs and quarantine/check artifacts.
- [x] Explicit reviewed-extract input mode works without PDFs or network access; records that PDFs were not verified in that run.
- [x] 32 unit tests pass with the cloud extra (25 core plus 7 mocked cloud-boundary tests), including failure/retry and idempotency cases.
- [x] Core installed into a fresh isolated Python 3.12 environment.
- [x] Python modules compile; five YAML configuration files parse.
- [x] Essential setup, source, data, architecture, testing and operations documentation.

## Cloud checks and remaining milestones

- [x] User-reported live BigQuery counts: annual 12, monthly 6, duplicate-key query empty, total 18 after rerun check.
- [ ] Complete value-by-value cloud reconciliation and recorded load job IDs.
- [ ] dbt debug/build and warehouse tests.
- [x] User installed google-cloud-bigquery 3.47.0; pin recorded. Full transitive lock remains pending; stable dbt Core/adapter pins are recorded below.
- [ ] Power BI Desktop report and refresh validation.
- [ ] Recorded 3–5 minute walkthrough.
- [ ] Scheduled production-style execution.
- [x] GitHub Actions unit-test workflow passed for the initial project commit.
  Evidence: https://github.com/Saurabhzambare/gacl-public-disclosure-pipeline/actions/runs/44484974724

The repository is public and the Windows clone is installed. The user confirmed
the ordinary --refresh command on 20 November: run
a027f1fa-4961-4cce-b2cd-bb976f54a860, input_mode=verified_pdfs,
18 extracted/loaded/stored, four passing checks and 25 Windows tests passed.
The downloader uses an explicit native Windows SSLContext.

Cloud setup evidence from the user's terminal: ADC login succeeded for project
instacart-analytics-practice; billingEnabled=false; BigQuery client 3.47.0
installed. The user chose billing-free operation. Snapshot mode is implemented
and tested with a mocked BigQuery client, including incomplete-export rejection,
no DML, replacement on rerun, failure handling and cloud row-count verification.
The user has now queried the live BigQuery table: 12 annual and 6 monthly rows,
no duplicate observation/source/version keys, and 18 rows after the requested
repeat-load check. This evidence is user-reported query output; load job IDs and
a full value comparison have not been supplied.

The user installed dbt-bigquery 1.12.4; the unpinned Core resolved to beta
1.13.0b1. Pin Core 1.12.7 and adapter 1.12.4 for reproducible installation.
Development verification on Linux/Python 3.12: dbt parse succeeded with the
pinned Core 1.12.7 and BigQuery adapter 1.12.4 (three models and seven SQL tests).
All 32 Python tests still pass. Live dbt debug/build on the user's Windows
installation, Power BI and the walkthrough remain pending.

## Known limitations

- Only two pinned PDFs and six annual metrics are supported.
- Some BRSR labels are missing from PDF text extraction; only clear total rows are selected.
- FY 2024–25 comparison figures are recalculated disclosures in the latest BRSR, not necessarily equal to earlier publications.
- Source revision detection fails closed; no automated preferred-version selection exists.
- The aggregate tests demonstrate numerical consistency, not regulatory compliance.
- Raw BigQuery count/duplicate checks are verified; full reconciliation, dbt and Power BI remain pending.
- Snapshot mode replaces cloud-only rows absent from the local export; sandbox expiration applies.
- No raw SAP, OPC UA or SCADA access, streaming pipeline or deployed AI service.

