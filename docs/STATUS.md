# Project status

Updated: 19 November 2026. First-version target: 22 November 2026, 8:00 PM IST.

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
- [x] 22 unit tests pass, including failure/retry and idempotency cases.
- [x] Core installed into a fresh isolated Python 3.12 environment.
- [x] Python modules compile; five YAML configuration files parse.
- [x] Essential setup, source, data, architecture, testing and operations documentation.

## Prepared, not yet cloud-verified

- [ ] BigQuery dataset and validated MERGE loader execution.
- [ ] dbt debug/build and warehouse tests.
- [ ] Cloud dependency versions resolved and recorded.
- [ ] Power BI Desktop report and refresh validation.
- [ ] Recorded 3–5 minute walkthrough.
- [ ] Scheduled production-style execution.
- [x] GitHub Actions unit-test workflow passed for the initial project commit.
  Evidence: https://github.com/Saurabhzambare/gacl-public-disclosure-pipeline/actions/runs/44484974724

The repository is public. Local files are prepared in the agent workspace; clone and run docs/SETUP.md on the intended Windows laptop to create that separate local installation.

## Known limitations

- Only two pinned PDFs and six annual metrics are supported.
- Some BRSR labels are missing from PDF text extraction; only clear total rows are selected.
- FY 2024–25 comparison figures are recalculated disclosures in the latest BRSR, not necessarily equal to earlier publications.
- Source revision detection fails closed; no automated preferred-version selection exists.
- The aggregate tests demonstrate numerical consistency, not regulatory compliance.
- Cloud/dbt/Power BI are not claimed as completed.
- No raw SAP, OPC UA or SCADA access, streaming pipeline or deployed AI service.

