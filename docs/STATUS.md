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
- [x] 25 unit tests pass, including failure/retry and idempotency cases.
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

The repository is public and the Windows clone is installed. On 20 November,
the user confirmed a full verified-PDF refresh using a one-process truststore
0.10.5 launcher: run 4a949773-e15d-4b6a-a7fb-6cb83d55ee6f, 18 extracted,
18 loaded, 18 stored, four passing aggregate checks. The integrated downloader
now uses an explicit native Windows SSLContext and has 25 passing development
tests. Confirmation of the ordinary command on the user's laptop is pending.
BigQuery/dbt, Power BI and the walkthrough remain the next delivery milestones.

## Known limitations

- Only two pinned PDFs and six annual metrics are supported.
- Some BRSR labels are missing from PDF text extraction; only clear total rows are selected.
- FY 2024–25 comparison figures are recalculated disclosures in the latest BRSR, not necessarily equal to earlier publications.
- Source revision detection fails closed; no automated preferred-version selection exists.
- The aggregate tests demonstrate numerical consistency, not regulatory compliance.
- Cloud/dbt/Power BI are not claimed as completed.
- No raw SAP, OPC UA or SCADA access, streaming pipeline or deployed AI service.

