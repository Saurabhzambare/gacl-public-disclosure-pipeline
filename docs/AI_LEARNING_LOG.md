# AI extension — guided implementation log

Started: 25 November 2026 (India).

Build-order reference: [Master Build Order](PHASE_2_BUILD_ORDER.md), version 1.0,
30 stable steps in eight stages. Step 1 readiness execution: **passed**.
Step 2 baseline execution: **passed**.
Step 3 inspector execution checks: **passed**.
Step 3 local commit checkpoint: **complete, 39ceacb, clean branch**.
Documentation merge: **verified, local merge a5001c0; clean branch**.
Step 4A execution checks: **passed, 27 November 2026**.
Current checkpoint: **Step 4B real-source batch and offline numerical regression passed; software-test and page-review evidence pending**. Existing
prototype milestones are product evidence, not learner-completed lessons.

## Working agreement

The author will implement the AI extension personally, one small step at a
time. For each step the assistant supplies the purpose, an ELI5 explanation,
prerequisites, exact file locations, commented code, execution instructions,
expected evidence and a stopping point. Actual results are reviewed before
dependent implementation begins.

The assistant independently maintains documentation. It does not independently
edit application code, configuration, dependency declarations or tests under
this learning agreement. Documentation maintenance does not imply publishing,
pushing, merging, deploying, installing dependencies or calling paid services.

Code examples should explain functions, parameters, return values and important
variables where applicable. Introduce classes only when they serve a concrete
purpose. Installation instructions should distinguish packages already installed
from genuinely new requirements and use the existing Windows virtual environment
where appropriate.

## Starting evidence

- The original data pipeline, BigQuery/dbt verification and Power BI refresh
  remain documented in [the first-version verification](VERIFICATION_2026-11-24.md).
- An assistant-prepared retrieval prototype exists on the local
  `feature/document-retrieval` branch. Its local test/evaluation evidence is in
  [the retrieval evaluation](RETRIEVAL_EVALUATION.md).
- That prototype is reference material. It is not evidence that the author has
  personally implemented or run the new retrieval feature on Windows.
- Publication of that local branch and its Windows verification remain pending.
- Embeddings, generated RAG answers, numerical assistant tools and agentic tool
  selection remain planned, not implemented.

## Step 1 — readiness execution verified on 25 November

Status: author-supplied Windows terminal output confirms the readiness checks.
Understanding discussion: still to be answered in the learner's own words.

Exact instructions, commented readiness code and expected output:
[Step 1 lesson](PHASE_2_STEP_01.md). Later code lessons will be documented when
their prerequisites and actual file contents have been inspected.

Purpose: establish which checkout, interpreter, PDF package, SQLite full-text
search capability and source files exist on the author's laptop before making
code changes. A missing prerequisite should be repaired before the first PDF
reading exercise.

ELI5: check that the toolbox and the two books are present before building the
assistant.

Run from `D:\gacl-public-disclosure-pipeline` in PowerShell. Check:

1. `git status --short --branch` and `git log -1 --oneline` to identify the
   checkout and any pre-existing changes. Do not discard files or switch branches
   merely to match the assistant's workspace.
2. The presence of `.venv\Scripts\python.exe` and its Python version. The
   project's declared minimum is Python 3.11.
3. The active interpreter's installed PyMuPDF version. The project currently
   declares `PyMuPDF==1.26.6`.
4. SQLite FTS5 support using an in-memory database only. This is a capability
   check, not creation of the project's retrieval index.
5. The source register and the two configured cached PDF paths under `data/raw`.
   File presence alone does not verify PDF integrity; checksum verification is a
   subsequent lesson.

No new source file, API key, model, vector database, GPU setup or cloud query is
required for this lesson. No dependency installation is assumed necessary until
the actual environment output is reviewed.

Stop after collecting these results. Report missing prerequisites and errors
honestly; do not mark this lesson passed without the author's output.

## Verified Step 1 output

| Check | Author-supplied result |
|---|---|
| Local checkout after pull | main/origin/main at 23634b2 |
| Project interpreter exists | True |
| Python | 3.11.4 |
| Virtual environment | True |
| PyMuPDF | 1.26.6 |
| SQLite FTS5 | Available; temporary in-memory table |
| Configured sources | 2 |
| Monthly cached PDF | PRESENT |
| Annual cached PDF | PRESENT |

The author initially pasted only the closing here-string line and cancelled it
with Ctrl+C, then pasted the full block and obtained the successful results
above. Explain the opening/closing delimiters as one complete block. No file
presence check proves checksum integrity, and no model or retrieval feature was
executed by this lesson. No installation or code-file change was required.

## Step 2 — baseline execution verified on 25 November

| Check | Author-supplied evidence |
|---|---|
| Starting main commit | eb7e18b |
| Personal implementation branch | feature/phase2-guided |
| Retrieval module / configuration / tests | All three Test-Path probes False |
| Existing unit tests | 32 passed in 1.278 seconds; no skips |
| Offline run ID | 0516c23e-efac-4775-9f42-1fdc4464d1ab |
| Input / source verification | cached_pdfs; pdfs_verified_this_run=true |
| Extracted / loaded / stored | 18 / 18 / 18 |
| Dataset checks | Four passed: monthly coverage, annual coverage, two energy reconciliations |
| Energy differences | 0.002 GJ and 0.00 GJ, each within 0.01 GJ |
| Final working tree | Clean on feature/phase2-guided |

This is author-supplied local Windows execution evidence, not an independently
executed audit or a new cloud/dbt/Power BI verification. Cloud-boundary unit tests
use a mocked client. The offline run verifies actual cached PDF hashes and
re-extracts facts; it establishes more than Step 1 file presence alone.
Understanding discussion remains open; do not invent the author's explanation.

## Step 3 — inspector execution checks verified on 25 November

Evidence: author-uploaded terminal output, Pasted text(20261125-072102).txt.
This is author execution evidence, not an assistant-run test or a source-code review.

| Check | Observed result |
|---|---|
| Branch | feature/phase2-guided |
| Monthly source hash | 4882f4e453a78fe956850944d9df2b636c74d225eab2331e7d8873fe4050c9c1 — MATCH |
| Scope / physical pages | dahej_plot3_report / 21 |
| Requested PDF / printed page | 5 / 4 |
| Monthly values, April–September | 12540.8, 12621.3, 12452.7, 11818.3, 11865.5, 11738.1; KL/day |
| Invalid page zero | Error: PDF page must be 1 or greater; exit code 1 |
| Existing software suite | 32 passed in 0.987 seconds, no skips |
| Untracked paths | scripts/ and .github/scripts/ |
| Commit / publication | No source-code commit or push evidenced |

The first bare path command failed before the inspector file existed. The author
then created the folder/file and successfully invoked it with the project's
Python executable. Teach the distinction between a file location and an execution
command; no package reinstall is needed for that initial shell error.

The extracted page is visibly imperfect in whitespace/column order, but contains
the six reported rates and unit context. This is embedded-text inspection, not
general table reconstruction, OCR or AI generation. Existing unit tests protect
the original system; direct page/error runs check this new inspector's behavior.

Understanding: the assistant explained zero-based library indexing when asked.
Do not mark an independent learner explanation as supplied. Physical page 5,
library index 4 and the report's printed page 4 are distinct concepts.

## Step 3 — file review, cleanup and local commit verified

The author listed two 4,179-byte files: scripts/inspect_source_page.py and
.github/scripts/inspect_source_page.py. Displayed hash prefixes were truncated,
so the full hashes were compared in variables before deletion. The guard passed;
only the extra copy was removed. The submitted script matches the intended
103-line lesson implementation. No assistant application-code edit was made.

Only scripts/inspect_source_page.py was staged. The author supplied the resulting
local commit 39ceacb, message "feat: add verified PDF page inspection script",
one new file/103 inserted lines. Final git status shows a clean
feature/phase2-guided branch. This closes the local commit checkpoint; there
is no evidence of a source-code push or merge into public main.

Git's CRLF-to-LF message describes normalizing this Python script's line endings.
It does not change the report PDFs or invalidate their source hashes. No new
test execution is invented after cleanup; the last supplied suite remains
32 passing tests in 0.987 seconds.

## Documentation synchronization — verified local merge a5001c0

The author supplied fetch/merge output using the ort strategy, clean status on
feature/phase2-guided and a graph with a5001c0 combining local inspector commit
39ceacb and origin/main documentation through 3df36db. No conflict, code push or
merge into public main is evidenced. Both lines of work were preserved.
The source branch remains personal and the latest verified software suite is
still 32 tests in 0.987 seconds; this docs merge is not a new runtime test.

## Step 4A — execution checks verified on 27 November

Evidence: author-uploaded Pasted text(20261127-042953).txt. The author created
src/gacl_pipeline/retrieval.py locally and ran the module on the personal branch.

| Check | Author-supplied result |
|---|---|
| Source / scope | gacl_dahej_plot3_ec_2025_h1 / dahej_plot3_report |
| Document version | Approved monthly SHA-256 4882f4e453a78fe956850944d9df2b636c74d225eab2331e7d8873fe4050c9c1 |
| Physical page 5 | printed_page 4, page_count 21, six monthly freshwater rows |
| Physical page 6 | printed_page null; extracted footer says Page 5 of 20 |
| Page 5 text SHA-256 | 1975b4bd411905133835f961efe30c7ffbfb600bfe37390e783306943ba6abd8 |
| Page 6 text SHA-256 | 81b517eab4bda8fc718702da5c368dc9ca0ff10100a0af19a1cc66f4050be95a |
| Extraction / library | pymupdf-page-text-sort-v1 / PyMuPDF 1.26.6 |
| Citation targets | Official monthly PDF with physical page fragments 5 and 6 |
| Invalid physical page 0 | Error: PDF page must be a positive integer; exit code 1 |
| Existing regression suite | 32 tests, 1.233 seconds, OK |
| Git status | feature/phase2-guided; only src/gacl_pipeline/retrieval.py untracked |

The supplied paste repeats some commands/test lines and the same final summary.
Count the reported 32-test suite once; do not add duplicated display lines or
infer several independently verified runs. Text hashes are recorded as reported;
do not recompute them from console-wrapped copied text and claim an independent
integrity check. The raw canonical text must be checked from the actual module
result when needed.

Page 6 is the intended unknown-mapping behavior. Extracting a footer does not
automatically populate reviewed configuration. No guessed page offset or new
numerical observation is introduced. The original source configuration remains
unchanged according to the supplied Git status.

The assistant explained physical/index/printed numbering and where the saved
mapping lives when asked. Do not mark a learner's independent explanation as
supplied. No new focused retrieval tests, all-page extraction or model run is
claimed. Current software counts remain separate from observations and page counts.

## Current checkpoint — module reviewed; Step 4B supplied

The author supplied the full 122-line src/gacl_pipeline/retrieval.py through
Get-Content. It matches the Step 4A implementation, including exact-text hashing,
unknown-label handling and the existing page CLI. This closes the source-file
inspection prerequisite; it is not another runtime test or a local commit.

The [Step 4B lesson](PHASE_2_STEP_04B.md) supplies exact commented JSON/Python,
file locations, concepts/ELI5, no-new-installation guidance, verification commands
and a stopping point. It creates config/retrieval.json and tests/test_retrieval.py,
and explains replacing the inspected module with shared verification/extraction
helpers while retaining extract_page and the single-page command. All-page
extraction opens each PDF once per batch. Reviews stay version-pinned and separate
from text; required unreadable/missing evidence fails, optional insufficient pages
are listed as skipped, unknown labels stay null, conflicting labels fail.

Documentation checks: the 20-line JSON and 266-/180-line Python blocks parse;
13 focused test methods were counted. No supplied application/test code was
executed by that check. Expected results are 13 focused / 45 full software tests,
71 physical / 70 usable pages and one skipped monthly cover; actual learner
results, visual comparison of the two recorded review notes, offline 18-fact
regression and Git scope remain pending. These counts describe different units.

The notes preserve the assistant's earlier 24 November visual review, not a new
learner attestation. The author must compare physical annual pages 1 and 37
before accepting their labels/notes. The annual production explanation must not
be transferred to monthly site rates. Source configuration and the inspector stay
unchanged; the raw text hash must exclude reviewer prose.

Do not commit partial Step 4 or start Step 5 yet. Batch newer documentation
synchronization at the Step 4 checkpoint after inspecting actual history.
The assistant changes documentation only; learner application code stays on the
personal branch until explicitly published.

## Step 4B — real-source batch and numerical regression verified, 27 November

The author pasted Windows terminal output directly after the uploaded text file
could not be read in the unavailable execution workspace. Only the pasted
results below are verified here; no uninspected attachment content is treated
as evidence.

| Check | Author-supplied result |
|---|---|
| Batch command | python -m gacl_pipeline.retrieval --all-pages --summary |
| Approved sources | 2; both reported PDF hashes match the pinned register |
| Monthly source | 21 physical pages, 20 usable pages |
| Monthly skip | Physical page 1; insufficient_embedded_text_no_ocr; alnum_chars 0 |
| Annual source | 50 physical pages, 50 usable pages; no skips |
| Total | 71 physical pages, 70 usable pages, one skipped page |
| Offline run ID | a8998693-ba1f-4044-b3b5-169b84456ca8 |
| Offline status/input | success / cached_pdfs; pdfs_verified_this_run=true |
| Numerical observations | 18 extracted, 18 loaded, 18 stored |
| Dataset checks | All four passed: monthly coverage, annual coverage, two energy reconciliations |
| Energy differences | 0.002 GJ and 0.00 GJ; tolerance 0.01 GJ |
| Git branch | feature/phase2-guided |
| Untracked paths | config/retrieval.json; src/gacl_pipeline/retrieval.py; tests/test_retrieval.py |
| Tracked diff summary | Empty; untracked files do not appear in git diff --stat |

This confirms real-source batch coverage and an unchanged accepted numerical
dataset in the supplied local run. A batch summary omits page bodies; it does not
independently establish exact page-text preservation, mapping/review field values
or agreement of review notes with the visible PDF. File presence does not prove
test execution. No cloud/dbt/Power BI rerun, local commit or source upload is
claimed.

Still needed: focused/full software-test summaries (expected 13/45 with the
unchanged baseline), Step 4B page-5 text hash and page-6 unknown mapping, the annual
page-1/page-37 review fields and learner visual comparison, plus the understanding
discussion. Existing results may be pasted; no repeat run is required merely to
share output. Keep Step 4 open and code uncommitted until the remaining evidence
is reviewed. Documentation synchronization stays batched at that checkpoint.

## Evidence to record after each lesson

Use the existing stable step ID. Record purpose, exact files changed, new
dependencies only if actually installed, commands/output, checks that passed or
failed, the learner's explanation, errors and their causes/fixes, local commit
if created, and next step. Do not store credentials or unreviewed raw responses
in documentation. A concise handoff includes build-order version, completed/current
step, relevant file content and latest output.

Record an understanding check such as: what went in, what came out, why this
method was chosen, and what failure the check catches. A documentation or plan
change does not advance the learner automatically.

## Progress record

| Date (India) | Step | Evidence | State |
|---|---|---|---|
| 25 November 2026 | Guided implementation agreement | Author requests personal implementation and independent documentation maintenance | Recorded |
| 25 November 2026 | Windows readiness check | Python 3.11.4; venv True; PyMuPDF 1.26.6; FTS5 available; two configured sources; both PDFs PRESENT | Execution passed; understanding discussion open |
| 25 November 2026 | Phase 2 documentation | Master Build Order v1.0, concept/contracts/evaluation guides and cross-guide scope updates prepared; no source implementation | Documentation prepared; learner still at Step 1 |
| 25 November 2026 | Documentation validation | 31 Markdown files / 184 local links checked; 30 sequential step IDs and eight stages verified; Step 1 sample syntax parsed without execution; whitespace checks passed | Passed; no new runtime or learner completion claimed |
| 25 November 2026 | Step 2 | Clean personal branch; 32 tests passed; run 0516c23e-efac-4775-9f42-1fdc4464d1ab verified PDFs, 18 records and four checks | Execution passed; understanding discussion open |
| 25 November 2026 | Step 3 | Inspector reviewed; full duplicate hashes matched; extra copy removed; only intended 103-line script committed as 39ceacb; clean personal branch | Local commit checkpoint complete; code not evidenced as uploaded |
| 25 November 2026 | Before Step 4 | Local merge a5001c0 combines 39ceacb and documentation through 3df36db; clean feature branch | Verified |
| 25 November 2026 | Step 4A | Single-page dictionary lesson prepared; 4B required before Step 4 completion | Pending learner implementation |
| 27 November 2026 | Step 4A | Page-5 evidence, null unknown mapping, expected page-zero error, 32 tests OK in 1.233 seconds; module untracked | Execution checks passed; source-file review before 4B pending |
| 27 November 2026 | Step 4A source review / Step 4B | Actual module matches 4A; complete 4B lesson supplied; JSON/Python syntax and 13 test-method count checked without execution | Review complete; learner 4B implementation/execution pending |
| 27 November 2026 | Step 4B partial execution | Both pinned PDFs: 71 physical / 70 usable pages, one monthly cover skipped; offline run a8998693-ba1f-4044-b3b5-169b84456ca8 preserves 18 facts and four passing checks; exactly three intended untracked paths | Batch/core checks passed; tests and page-review evidence pending |
