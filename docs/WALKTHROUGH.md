# Project walkthrough script

Status: script prepared on 24 November 2026; video not yet recorded.
Target length: about 3–5 minutes. Demonstrate the actual project and distinguish
previously verified evidence from commands you successfully run during recording.

## 0:00–0:30 — Problem and scope

Show the README and report overview.

> I built this independent data engineering project to turn selected GACL public
> water and energy disclosures into traceable reporting. It processes two pinned
> official PDFs and 18 observations. It does not use GACL's internal systems or
> live plant data. The focus is reliable extraction, validation and provenance.

## 0:30–1:15 — One observation through the pipeline

Show the source register, then the reviewed monthly CSV in data/examples.
Trace April 2025 freshwater use: 12,540.8 KL/day, Dahej Plot 3 scope,
PDF page 5, printed page 4. Open the official PDF page if it is available.

> Python verifies the document checksum, extracts the selected table, preserves
> the original number string and normalizes the value. Each observation carries
> its period, unit, reporting boundary, source version and page references.

Show the architecture and validation modules. Explain one concrete check:
monthly coverage must contain the six expected months, and annual energy
components must reconcile within the documented 0.01 GJ tolerance.

## 1:15–2:00 — Repeatability and cloud reporting

Show a successful local run summary only after actually running it, or label
existing output as a previous run. The runbook documents --offline and --refresh;
--from-examples is a separate reviewed-extract mode and does not verify PDFs.

> SQLite loads are duplicate-safe. Repeating a load retains the same selected
> observations. The billing-free cloud route uploads a validated full snapshot;
> it replaces the cloud copy and does not perform incremental MERGE operations.
> dbt provides separate monthly and annual reporting views.

Show the actual BigQuery reference-check results if available: 18 raw, 18 staged,
6 monthly and 12 annual, with zero differing facts. Explain that three views and
seven dbt tests are distinct from 32 Python unit tests and eight manual SQL checks.
Do not describe a parse-only result as a live build. Do not show credentials.

## 2:00–3:00 — Read the report

Show Water & Energy Overview.

> Monthly average daily freshwater use decreases from 12,540.8 in April to
> 11,738.1 KL/day in September, with some variation in between. These are monthly
> daily-average rates, not monthly volumes. I cannot infer the operational cause
> or claim efficiency savings from these disclosures alone.

Point to the annual energy stacks and annual water groups. Explain that energy
is GJ and water is KL. The earlier financial year contains recalculated
comparatives from the FY 2025–2026 report. Annual company totals and monthly
site rates remain separate because their scopes and statistics differ.

## 3:00–3:40 — Traceability and limitations

Show Sources & Coverage. Trace an annual energy reference to PDF page 36,
printed page 78, and the monthly reference to PDF page 5, printed page 4.
Open a source footer link if it is available.

> This page documents the 6 monthly and 12 annual observations, their coverage,
> units and source pages. Eighteen is an observation count, not a test count.
> Dashboard labels are rounded where shown in millions; source precision is
> preserved upstream. Run logs and check artifacts are separate from these
> coverage cards.

## 3:40–4:15 — Engineering choices and next work

> The parsers deliberately support two known documents. A changed checksum stops
> processing for review. Scheduling, broader document coverage and a hosted
> interactive report are future work. A complete captured run through extraction,
> cloud loading, dbt and dashboard refresh is still an outstanding evidence task.

Close with the repository URL. Keep the recording understandable without private
setup explanations; the README, source register and dashboard guide provide them.

## Before recording

Open only the report, repository and relevant query results. Prepare the source
pages and recent successful outputs. Close login prompts and unrelated tabs.
Save the recording outside the repository initially; add its link only after
reviewing the actual video. Do not claim the recording is published until a
working link exists.
