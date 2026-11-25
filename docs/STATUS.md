# Project status

Updated: 25 November 2026. Original first-version target: 22 November 2026, 8:00 PM IST; this was a target, not a completed release date.

## Guided AI implementation — 25 November 2026

The author will personally implement each new AI step, with explanations,
commented code, exact file instructions and execution checks supplied in the
conversation. The assistant independently maintains documentation. The earlier
local retrieval prototype remains reference material; it is not evidence of
author implementation or Windows execution. The first lesson checks the existing
Windows environment and cached source files; its results are pending. See the
[guided implementation log](AI_LEARNING_LOG.md). No code, configuration,
dependency or test changes are part of this documentation checkpoint.

The [Phase 2 Master Build Order](PHASE_2_BUILD_ORDER.md) version 1.0 records
30 stable steps in eight stages. Current learner position: Step 1, pending
Windows readiness output; all learner steps remain pending. Supporting
[concept](AI_CONCEPTS.md), [contract](AI_CONTRACTS.md) and
[evaluation](AI_EVALUATION_PLAN.md) guides define scope without claiming
implementation. The first-version dated evidence below remains unchanged.

Documentation checkpoint in the reference checkout: 31 Markdown files and
184 local links checked; build
order has 30 sequential steps/eight stages; the standalone Step 1 sample parses
without execution. Markdown-only changes and whitespace checks verified. These
are documentation checks, not a new software/model/cloud/Windows run.

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
- [x] User screenshot verifies all eight reference checks passed: 18 raw, 18 staged, 6 monthly, 12 annual, zero differing facts.
- [x] Record actual cloud load job ID and table expiration: see [24 November verification](VERIFICATION_2026-11-24.md).
- [x] User-verified dbt debug and build: 3 views created, 7 SQL tests passed; PASS=10 WARN=0 ERROR=0 SKIP=0.
- [x] User installed google-cloud-bigquery 3.47.0; pin recorded. Full transitive lock remains pending; stable dbt Core/adapter pins are recorded below.
- [x] Power BI Desktop: two report pages built; user confirmed a successful refresh.
- [x] Actual two-page PDF reviewed on 24 November; displayed values, units, counts, page references and all four source-link annotations checked. PDF and previews are included under dashboard/.
- [x] Dashboard documentation and a 3–5 minute walkthrough script prepared.
- [ ] Editable PBIX shared or reproducible PBIP source supplied; PBIX remains on the author's laptop.
- [x] Manually executed extraction → BigQuery snapshot → dbt build → eight reference checks → Desktop refresh verified in sequence on 24 November; terminal output, screenshots and explicit refresh confirmation recorded in [verification evidence](VERIFICATION_2026-11-24.md). This was not a single orchestrated job or video recording.
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
repeat-load check. The initial evidence was user-reported query output. The
24 November rerun supplied job_id 2bfa8593-f4e7-4bd4-bd1b-6426ff209e18 and
table_expires_at 2027-01-19T06:05:47.607000+00:00. Reference-comparison
screenshots verify the selected core facts.

The user installed dbt-bigquery 1.12.4; the unpinned Core resolved to beta
1.13.0b1. Pin Core 1.12.7 and adapter 1.12.4 for reproducible installation.
Development verification on Linux/Python 3.12: dbt parse succeeded with the
pinned Core 1.12.7 and BigQuery adapter 1.12.4 (three models and seven SQL tests).
All 32 Python tests still pass. On 22 November the user confirmed live dbt debug
(Connection test OK; All checks passed) and build on Windows/Python 3.11.4,
Core 1.12.7, adapter 1.12.4. Three views were created and seven SQL tests passed;
PASS=10 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=10. The reported build
included an interactive dbt State sign-in; this is separate from the Google ADC
setup. Anonymous usage-event flushing failed after debug succeeded; the user
then disabled usage stats for the build.

A read-only reference comparison is prepared in sql/bigquery_verification.sql:
eight checks compare all 18 reviewed fact values, units, dates and scopes across
the raw table and dbt views. The expected facts were loaded through the pinned
CSV checksum reader, validated, and the generated GoogleSQL was syntax-parsed.
The user supplied a BigQuery screenshot on 22 November with all eight checks
passed=true: annual 12 and zero differences, monthly 6 and zero differences,
raw 18 and zero differences, staging 18 and zero differences. This verifies the
selected values, periods, units and scopes against the reviewed reference;
it does not independently verify every provenance column. The subsequent Power BI milestone is recorded below; the walkthrough recording remains pending.

## Power BI evidence — 24 November 2026

- Direct Google BigQuery navigation and the two reporting tables were shown in the user's Desktop workflow; the exact connection options and Import/DirectQuery mode have not been independently inspected from PBIX source.
- The user confirmed a successful Desktop refresh after the 24 November local/cloud/dbt/reference-check sequence; see [verification evidence](VERIFICATION_2026-11-24.md). Evidence is terminal output, screenshots and explicit confirmation, not a video or automated cross-stage log.
- Water & Energy Overview: six monthly daily-average rates (April–September 2025), two annual energy stacks and annual water comparison by financial year.
- Sources & Coverage: 6 monthly, 12 annual and 18 total observations; three annual reference rows and one monthly reference row; coverage, units and interpretation notes.
- Monthly values and rounded annual chart labels agree with the reviewed reference facts. Source references show annual PDF pages 36/37/38 (printed 78/79/80) and monthly PDF page 5 (printed 4).
- The original exported PDF has two pages; each contains annual and monthly link annotations pointing to the approved official source URLs. These annotation checks establish stored destinations, not ongoing URL availability.
- The PDF is preserved as supplied. A small grey mark beside each page heading remains; the author chose to retain it. No chart, table or source note is obscured.
- Page previews are rendered from the actual PDF, not design mockups. PBIX is not included; repository ignore rules still exclude it.
- Page 2 implements coverage and provenance. Latest-run status, check results, rejected-row counts and extraction-method fields are available elsewhere in the pipeline and documentation; they are not displayed as live dashboard visuals.

## AI extension — local feature branch, 24 November 2026

- [x] Separate checksum-verified page/chunk index and read-only lexical search implemented on feature/document-retrieval.
- [x] Real-source index: 2 PDFs, 71 physical pages, 70 indexed text pages, 136 chunks; monthly cover skipped without OCR.
- [x] Explicit PDF/known printed-page citations and two separately labelled visual-review annotations.
- [x] 40 assistant-authored/source-checked evaluation cases (24 development, 16 holdout partition). Independent human annotation review is pending.
- [x] Baseline top-five reference-page hits: 15/16 development, 11/12 holdout; 26/28 combined answerable questions. Twelve unsupported/adversarial cases are diagnostic only; no answer/refusal accuracy claim.
- [x] 60 local Linux/Python 3.12 tests passed: 32 existing plus 28 retrieval tests. Real extraction still matches all 18 reviewed records, including provenance.
- [ ] Feature execution on the user's Windows laptop / Windows CI.
- [ ] Publish the local feature branch to GitHub; no publication is implied by this development checkpoint.
- [ ] Embeddings, RAG generation, validated numerical answer tools, agentic tool selection and an interactive interface.

Details and commands: [retrieval guide](RETRIEVAL.md), [evaluation results](RETRIEVAL_EVALUATION.md), and [AI scope plan](AI_EXTENSION_PLAN.md).

## Known limitations

- Only two pinned PDFs and six annual metrics are supported.
- Some BRSR labels are missing from PDF text extraction; only clear total rows are selected.
- FY 2024–25 comparison figures are recalculated disclosures in the latest BRSR, not necessarily equal to earlier publications.
- Source revision detection fails closed; no automated preferred-version selection exists.
- The aggregate tests demonstrate numerical consistency, not regulatory compliance.
- Raw BigQuery count/duplicate checks are verified; dbt views/tests are verified; core reference reconciliation is verified; Power BI report/refresh is verified as described above; the manual end-to-end verification sequence is recorded; the walkthrough video and scheduled execution remain pending.
- Snapshot mode replaces cloud-only rows absent from the local export; sandbox expiration applies.
- No raw SAP, OPC UA or SCADA access, streaming pipeline or deployed AI service.

