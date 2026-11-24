# GACL Operations and Sustainability Data Pipeline — Build Plan

Prepared for Saurabh Zambare on 19 November 2026.
Target completion: Sunday, 22 November 2026, by 8:00 PM IST.
Application deadline discussed: Sunday, 29 November 2026.
Status: implementation in progress. See STATUS.md for verified evidence.

Checkpoint — 20 November: local PDF-to-SQLite execution is verified on the user's
Windows laptop, with 18 observations and 25 passing core tests. The user has
chosen billing-free BigQuery; replace the planned cloud MERGE step with an
explicit full-snapshot batch load. Snapshot code and mocked SDK tests are
prepared. The user has since verified live BigQuery counts (12 annual,
6 monthly), no duplicate keys, and 18 rows after the rerun check. Full value
reconciliation, dbt, Power BI and the walkthrough remain pending. The original daily checklists below are planning gates, not a live
completion tracker.

Checkpoint — 22 November: live dbt debug succeeded and build created three
reporting views with seven passing SQL tests (10 total successful resources,
no warnings/errors/skips). All eight checks in sql/bigquery_verification.sql subsequently passed in
BigQuery (user screenshot): expected counts and zero differing facts. Power BI and the recorded
walkthrough remain outstanding; the entire project is not yet complete.

Checkpoint — 24 November: both Power BI pages are built, and the user confirmed
Desktop refresh success. The actual two-page PDF was reviewed for chart values,
counts, units, source pages and all four exported source-link destinations.
PDF/previews and report documentation are now packaged in dashboard/. The actual
second page is Sources & Coverage; live run-status/check/rejection visuals from
the original specification were not implemented. A walkthrough script is ready,
but the video, shared editable PBIX and captured end-to-end rerun remain pending.
The original dated checklists below are preserved as the plan; docs/STATUS.md is
the current evidence tracker.

## 1. Project objective

Build a reproducible batch data pipeline that converts GACL's public environmental and sustainability disclosures into validated BigQuery tables and Power BI reports. Demonstrate source traceability, careful interpretation, repeatable loading, failure handling and clear technical communication.

Business questions:
- How did average daily freshwater consumption change across the reported months at Dahej Plot 3?
- How did GACL's disclosed annual renewable and non-renewable energy use change?
- Which periods, units and reporting boundaries are covered, and which observations fail checks?
- Can a reviewer trace each dashboard number back to a report page?

This is an independent portfolio project using public GACL disclosures. It is not commissioned by GACL and does not use internal SAP transactions or live plant telemetry.

## 2. Delivery scope and time budget

Assume about 20–24 focused hours across 19–22 November. This is an estimate, not a completion guarantee. Each day's exit gate takes priority over extra features.

Must ship:
- Two verified public PDFs and a source register.
- Monthly freshwater observations for April–September 2025 from the Dahej Plot 3 report.
- Annual energy and water observations for FY 2024–25 and FY 2025–26 from the latest BRSR.
- Python download/extraction/validation workflow, BigQuery load and SQL/dbt transformations.
- Idempotent loading: reruns do not multiply records.
- Run logs, quarantined invalid rows, bounded retries for transient failures and a historical reload option.
- Power BI dashboard with two pages.
- Documentation, reproducible commands, dependency versions and a short recorded demonstration.

Add only after the core works:
- A second compliance period from the same site and reporting boundary.
- Scheduled execution using an already available runner.
- Additional annual reports and production history.

After the 22 November release:
- RAG with embeddings, a vector store, document versioning and page citations.
- Industrial connectivity in a separate, explicitly simulated environment.
- Additional cloud platforms, NoSQL systems or deployment services only if they address an actual need.

Do not add synthetic measurements to the GACL dataset, invent timestamps, or describe historical report ingestion as live streaming.

## 3. Source register

| Source | URL | Extract | Scope and limitations |
|---|---|---|---|
| Dahej Plot 3 EC compliance, April–September 2025 | https://gacl.com/wp-content/uploads/2026/04/EC_Compliance_Plot-3_April-to-Sept-25.pdf | Printed page 4, PDF page 5: monthly average freshwater consumption | Six monthly observations in KL/day; retain the report's site/plot boundary. These are not individual daily meter readings. |
| GACL BRSR FY 2025–26 | https://gacl.com/wp-content/uploads/2026/08/53RD-AR-BRSR.pdf | Printed pages 78–80: annual energy and water tables; page 81 emissions is optional | FY 2025–26 and FY 2024–25 comparative disclosures. Confirm the reporting boundary and footnotes before labeling values as standalone or consolidated. |
| Optional production history | https://gacl.com/wp-content/uploads/2025/09/Report-2024-25-.pdf | Quantitative Data for Ten Years | Annual product production and captive power generation; a later extension, not needed for the first release. |

Archive pages:
- https://gacl.com/brsr-reports/
- https://gacl.com/safety-compliance/
- https://gacl.com/financials/

For every source retain: source_id, title, URL, reporting period, published date if explicitly available, retrieved_at, checksum, local filename, PDF page and printed page. Keep publication date separate from reporting period and download date.

## 4. Architecture and stack

Use Python for collection and parsing, BigQuery for storage, SQL/dbt for transformations and checks, Power BI for reporting, and Git for version control. Keep scheduling lightweight; a local run must work first.

Processing layers:
1. Raw: unmodified PDFs and retrieval manifests.
2. Staging: extracted strings, normalized values, provenance and extraction method.
3. Curated: validated tables at explicitly documented grains.
4. Reporting: separate monthly site and annual company views.
5. Operations: run summaries, validation outcomes and quarantine records.

Prefer deterministic text/table extraction for these selected documents. If a layout cannot be parsed reliably within the time budget, use a manually reviewed seed for that table and label it as manual extraction. The downstream validation and loading remain reproducible; do not claim fully automated extraction.

## 5. Minimal data model

| Table | Grain / purpose | Important fields |
|---|---|---|
| source_documents | One version of one source document | source_id, URL, checksum, reporting period, retrieved_at |
| metric_definitions | One defined measurement | metric_id, label, unit, statistic_type, reporting_scope |
| monthly_site_observations | One month, site/plot, metric and source version | period_start, period_end, site_id, plot_id, metric_id, numeric_value, unit, source_id, page |
| annual_company_observations | One financial year, reporting boundary, metric and source version | fiscal_year, scope_id, metric_id, numeric_value, unit, source_id, page |
| pipeline_runs | One attempted execution | run_id, started_at, ended_at, status, stage, row counts, error category |
| validation_results | One check outcome for a run | run_id, check_id, passed, failed_count, details |
| quarantined_observations | One rejected candidate observation | raw_value, source_id, page, reason, run_id |

Retain source wording and raw values. Define a canonical identity from period + reporting scope + metric + unit/statistic. Preserve document versions separately and use a documented rule for choosing the current reporting value.

Do not split company totals into assumed plant values. Do not join annual company metrics to monthly site records as if they had the same grain.

## 6. Day-by-day tasks

### Thursday, 19 November — Sources, interpretation and extraction (about 5 hours)

- [ ] Create project folders and a README stating scope and provenance.
- [ ] Download the two core PDFs and record checksums.
- [ ] Confirm the exact pages and table headers visually.
- [ ] Define the two observation schemas and data dictionary.
- [ ] Extract six monthly water observations and the selected annual energy/water rows.
- [ ] Preserve Indian-number formatting in raw fields and convert numerical fields carefully.
- [ ] Reconcile all selected values against the source tables.
- [ ] Verify existing BigQuery access and the intended project/dataset before cloud work.

Exit gate: reviewed local datasets, source register and explicit metric definitions exist. If cloud setup is blocked, continue with local staging rather than losing the day.

### Friday, 20 November — Repeatable pipeline and warehouse (about 6 hours)

- [ ] Separate download, extraction, normalization, validation and load stages.
- [ ] Add source/version tracking and run identifiers.
- [ ] Create BigQuery staging and curated tables.
- [ ] Implement duplicate-safe load/merge logic.
- [ ] Build dbt staging models and curated reporting views.
- [ ] Implement the core checks in section 7.
- [ ] Run twice and compare keys, counts and values.

Exit gate: one command runs the selected pipeline; a rerun produces the same curated records. Cloud stages must actually succeed before calling the project a deployed BigQuery pipeline.

### Saturday, 21 November — Reliability and dashboard (about 6 hours)

- [ ] Log each pipeline stage and its result.
- [ ] Add bounded retries only for transient download/load errors.
- [ ] Quarantine invalid data with useful reasons.
- [ ] Add a source/period option for historical reloads.
- [ ] Exercise controlled failures in isolated fixtures.
- [ ] Build Power BI page 1: monthly water and annual energy/water trends in separate visuals.
- [ ] Build Power BI page 2: coverage, source links, run status and validation results.
- [ ] Add clear units, scope labels and reporting dates.
- [ ] Attempt scheduling only if the manual pipeline and dashboard already work.

Exit gate: valid observations reach reporting, invalid input is visibly rejected, and reruns recover without duplicates.

### Sunday, 22 November — Verification, explanation and release (about 4–6 hours)

- [ ] Freeze feature additions by midday.
- [ ] Run from a clean environment using the README.
- [ ] Reconcile every first-version observation with the original PDFs.
- [ ] Check every dashboard measure against SQL results.
- [ ] Confirm credentials, local paths and secrets are excluded from the repository.
- [ ] Write architecture, limitations, extraction decisions and troubleshooting notes.
- [ ] Record a 3–5 minute walkthrough.
- [ ] Record actual row counts, checks and observed run results for the project summary.
- [ ] Package the repository, dashboard and documentation for review by 8:00 PM IST.
- [ ] Review any public publication or outreach separately; this plan does not send messages.

Exit gate: all mandatory acceptance checks below pass. If a feature is unfinished, document it as unfinished and exclude it from completed-feature claims.

## 7. Meaningful validation and failure demonstrations

| Check | Expected behavior |
|---|---|
| Required fields and numeric parsing | Reject observations without period/scope/metric/source or with unparseable values. |
| Uniqueness and idempotency | Reprocessing the same document leaves curated record counts and values unchanged. |
| Unit and statistic consistency | KL/day averages cannot silently enter annual KL totals; GJ and kWh remain distinct unless explicitly converted. |
| Reporting period and boundary | Annual and monthly facts retain their own grains; company and site scopes remain separate. |
| Monthly coverage | The selected April–September report contains six distinct expected months; missing months are flagged. |
| Energy arithmetic | Renewable and non-renewable components reconcile with the corresponding source totals, using a documented rounding tolerance. |
| Null semantics | NA, blank, dash and zero remain distinguishable; ambiguous entries are reviewed. |
| Source reconciliation | Selected values match their cited PDF pages, including signs, decimal places and units. |
| Controlled failure and recovery | A test download failure logs an error; a test invalid row is quarantined; recovery does not duplicate valid rows. |
| Source revision | Changed bytes are recognized as a new version; conflicting historical values are preserved and flagged. |

Use isolated test fixtures for deliberately broken records. Do not present those fixtures as GACL observations. Do not treat a statistical outlier as proof of operational failure or regulatory non-compliance.

## 8. Dashboard specification

Page 1 — Reported trends:
- Monthly average freshwater consumption at the disclosed Dahej site/plot.
- Year-over-year renewable/non-renewable energy and annual water measures.
- Separate visuals for monthly site measurements and annual company data.
- Clearly labeled units, periods, definitions and source links.

Page 2 — Pipeline and data quality:
- Loaded observations and reporting coverage.
- Last successful run, failed checks and rejected rows.
- Source-document register and extraction-method disclosure.
- Missing periods and source revisions.

Avoid capacity-utilization, emissions-per-product or water-per-tonne calculations unless numerator and denominator have compatible periods, scopes and definitions. Do not interpolate monthly data to create an appearance of daily granularity.

## 9. Repository deliverables

- README with problem, setup, commands, data limitations and reproducibility steps.
- Source manifest and data dictionary.
- Python pipeline and pinned dependencies.
- dbt project with models and meaningful tests.
- SQL for warehouse setup and reconciliation.
- Example configuration without credentials.
- Reviewed extracted data or reproducible instructions, with source references.
- Power BI file, exported screenshots and refresh instructions.
- Run/test evidence and short demonstration recording.

Suggested folders: config/, data/raw/, data/staging/, src/, dbt/, tests/fixtures/, dashboard/, docs/. Keep large source PDFs out of Git by default; download them through the manifest. Include source URLs and checksums.

## 10. Completion checklist

- [ ] Only genuine public GACL observations appear in the main dataset.
- [ ] Every reported observation has a source, page, period, unit and scope.
- [ ] The selected pipeline runs from documented commands.
- [ ] A repeated run does not duplicate observations.
- [ ] A historical reload works for a selected source or period.
- [ ] Invalid records are flagged and logged.
- [ ] Calculated totals reconcile within documented tolerance.
- [ ] BigQuery, dbt and Power BI results agree for the included measures.
- [ ] Another person can understand the setup without a private explanation.
- [ ] All claims match demonstrated features; planned work is marked separately.

## 11. Contingencies

- PDF parsing difficulty: use a disclosed, reviewed seed for the difficult table; preserve the raw source and extraction notes.
- BigQuery access difficulty: finish local extraction, validation and SQL first. If cloud loading remains untested, say so and do not claim cloud deployment.
- Power BI connectivity difficulty: export the verified curated tables to CSV and document manual refresh.
- Time pressure: cut scheduling first, then extra periods/metrics. Preserve provenance, validation, duplicate-safe loads and documentation.
- Small sample: emphasize pipeline correctness. Six monthly readings and a few annual periods do not support credible predictive maintenance or a sophisticated forecasting model.

## 12. Interview evidence

Prepare to demonstrate:
1. A reported observation traveling from PDF to curated table to dashboard.
2. How a misleading unit, duplicate or scope mismatch is caught.
3. What happens when a pipeline stage fails.
4. Why monthly averages and annual totals are kept separate.
5. What would change for authorized historian or OPC UA data in a future implementation.

Use the project title “GACL Public-Disclosure Data Pipeline” in outreach if it helps make the independent scope clear. Write resume bullets after completion using actual measurements and features; do not invent throughput, time savings, production impact or employment at GACL.

