# Phase 2 — Step 2: Record a baseline and isolate personal implementation

Build-order version: 1.0. Prepared: 25 November 2026 (India).
Status: **instructions prepared; learner execution pending**.
Prerequisite: Step 1 readiness execution passed on Windows. Review its short
understanding questions alongside this lesson's output.

## Purpose and ELI5

Record what already works before changing application code, and create a branch
for your own implementation. ELI5: photograph the working machine, then set up a
separate workbench for its new parts.

A baseline is a recorded reference result. Later, regression tests let us check
that an AI change did not break the original pipeline. A Git branch records a
separate line of development; it does not make another physical copy of the
PDFs, environment or database. Ignored local artifacts remain in this clone.

## Installations, files and scope

No new package or application file is required. Reuse `.venv`, the existing
tests and the original pipeline. Optional BigQuery tests may skip if the cloud
SDK is absent; report that honestly rather than installing a cloud stack merely
to reach a particular test count.

The tests create controlled temporary fixtures. The offline pipeline verifies
cached PDFs, extracts facts, and updates the local SQLite warehouse, exports
and logs. It makes no report download or cloud load. A rerun of the same approved
sources should retain 18 observations without duplicates. This is a local run,
not a new BigQuery/dbt/Power BI refresh or an AI run.

## A. Inspect and receive the documentation update

Run in PowerShell from `D:\gacl-public-disclosure-pipeline`:

```powershell
# Check the actual branch and any tracked/untracked changes first.
git status --short --branch
```

If changed/untracked files appear, stop and share the output before switching or
pulling. The previous successful readiness check should not create such files.
If the checkout is still clean and on main, run the following one command at a
time, stopping on an error:

```powershell
# Receive the documentation recording Step 1 and this Step 2 lesson.
# --ff-only refuses to create an unexpected merge commit.
git pull --ff-only origin main

# Record which commit your baseline begins from.
git log -1 --oneline
```

## B. Create your implementation branch

```powershell
# Create and switch to a branch for your personally implemented AI work.
git switch -c feature/phase2-guided

# Confirm the branch name and that the working tree remains clean.
git status --short --branch
```

Expected branch: `feature/phase2-guided`. If Git reports that the name already
exists, share the output; do not delete the branch or overwrite changes. Creating
this local branch does not push, publish, merge or deploy anything.

## C. Inspect which reference implementation files actually exist

```powershell
# Public main currently contains the guides, not the local prototype's code.
Test-Path ".\src\gacl_pipeline\retrieval.py"
Test-Path ".\config\retrieval.json"
Test-Path ".\tests\test_retrieval.py"
```

For the documented main-based starting point, expect three `False` results.
That is not a failed installation: those files will be introduced in later
lessons. If any result is `True`, report it so we inspect existing content before
giving insertion instructions. Do not copy or overwrite the entire prototype.

## D. Run the existing software tests

```powershell
# -m runs Python's standard-library unittest module in this environment.
# discover finds tests; -s sets the folder; -v prints each test's result.
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The main-based suite has 32 tests: 25 core tests and seven cloud-boundary tests.
With its cloud dependency available, the expected summary is 32 passing tests.
Without it, report the actual skips; do not claim all 32 executed successfully.
These cloud-boundary tests use a mocked client, not live credentials/cloud jobs.
The prototype's 28 additional retrieval tests are not in this starting checkout.

If the suite has failures or unexpected errors, stop and share them before
continuing. Test methods are executable checks; they are not GACL measurements.

## E. Rerun the original pipeline offline

After reviewing a successful test result, run:

```powershell
# Use actual cached PDFs, verify their configured hashes and re-extract facts.
# --offline avoids report downloads; it does not mean reuse reviewed CSVs.
.\.venv\Scripts\python.exe -m gacl_pipeline --offline
```

Expected for the original selected sources:

```text
status: success
input_mode: cached_pdfs
pdfs_verified_this_run: true
extracted_rows: 18
loaded_rows: 18
warehouse_rows: 18
```

The JSON also reports four dataset checks: monthly coverage, annual coverage and
two energy reconciliations. Their results should be true. The FY 2024–25 energy
difference of 0.002 GJ is within the documented 0.01 GJ tolerance. Run ID/timestamps
will differ. This command provides actual hash/extraction verification; Step 1's
file-presence check did not.

If a hash/source/layout check fails, keep the error and stop. Do not update a
hash or modify reviewed examples to make the run pass.

## F. Confirm tracked files remain unchanged

```powershell
# Local databases/exports/logs should remain ignored rather than source changes.
git status --short --branch
```

Expected: branch `feature/phase2-guided` without changed/untracked file entries.
Do not commit an environment, PDF, database or raw log. There is no source-code
commit to make merely because tests and a rerun succeeded.

## Output and understanding checkpoint

Share branch/inventory output, the test summary (and any skips), the complete
pipeline JSON and final Git status. We record exact versions/results in the
learning log; running commands alone does not invent a completion record.

Explain briefly: why is a test count different from an observation count, and why
does a repeated load retaining 18 warehouse rows matter? Also revisit Step 1:
why does PRESENT not prove approved content, and why use the `.venv` interpreter?

Stop after this lesson. Step 3 will create `scripts/inspect_source_page.py`
personally, after the baseline output is reviewed. No PDF-inspection source file
or future AI dependency should be created during Step 2.
