# AI extension — guided implementation log

Started: 25 November 2026 (India).

Build-order reference: [Master Build Order](PHASE_2_BUILD_ORDER.md), version 1.0,
30 stable steps in eight stages. Step 1 readiness execution: **passed**.
Step 2 baseline execution: **passed**.
Step 3 inspector execution checks: **passed**.
Step 3 local commit checkpoint: **complete, 39ceacb, clean branch**.
Documentation merge: **verified, local merge a5001c0; clean branch**.
Step 4A execution checks: **passed, 27 November 2026**.
Step 4: **execution, source-review confirmation and Git checkpoint complete, 27 November**.
Step 5: **complete; implementation 42c9ceb and documentation merge 98c14ec published, reviewed and clean**.
Current lesson: **Step 6 separate SQLite index; instructions prepared, learner implementation/execution pending**. Existing
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

At this checkpoint the software-test summaries and page-review evidence were
still pending. The subsequent software-test results are recorded below.
Page-field results already available locally may be pasted without repeating
their extraction. Documentation synchronization stays batched at the Step 4
checkpoint.

## Step 4B — focused and full Windows tests verified, 27 November

The author supplied both verbose terminal test runs directly in the conversation.

| Run | Author-supplied result |
|---|---|
| Focused test_retrieval.py suite | 13 tests, 0.634 seconds, OK |
| Complete tests suite | 45 tests, 1.620 seconds, OK |
| Composition | 32 existing tests plus the same 13 new retrieval tests |
| Failures/errors/skips | None shown in either run |

The 13 retrieval tests cover exact fixture text/hash and separate notes, explicit
skips/counts, changed source bytes, stale/duplicate reviews, conflicting labels,
invalid source/page/threshold inputs, unreadable/out-of-range required pages,
unknown printed labels and preservation of the page CLI alongside batch summary.
These use synthetic temporary PDFs, not new GACL documents or observations.
The full suite includes mocked BigQuery boundaries; it is not a fresh cloud job.
The focused suite is included in the full suite, so there are 45 distinct tests.

Together with the earlier pasted batch/offline output this verifies the software
tests, 70 usable real-source pages and the preserved 18-fact numerical pipeline.
At this test checkpoint the real-page fields, learner visual comparison and
understanding discussion remained pending. The subsequent metadata results are
recorded below. Do not repeat successful tests without a relevant code change.
No local code commit, source upload or final Step 4 completion was evidenced.

## Step 4B — real-page metadata verified; local checkpoint ready, 27 November

The author ran the compact read-only Python block and pasted all four records.
The accompanying GitHub Desktop screenshot shows the personal
feature/phase2-guided branch, exactly three selected new files and an empty
commit-summary field. The commit button is disabled until a summary is entered;
no new commit is evidenced by that screenshot.

| Source / physical page | Printed page | Review field | Text SHA-256, as reported |
|---|---|---|---|
| Monthly / 5 | 4 | null | 1975b4bd411905133835f961efe30c7ffbfb600bfe37390e783306943ba6abd8 |
| Monthly / 6 | null | null | 81b517eab4bda8fc718702da5c368dc9ca0ff10100a0af19a1cc66f4050be95a |
| Annual / 1 | 43 | Separate labelled review, standalone boundary and financial year | 9e551faa06772481d38415a3a85717245022bad46df8c02f93f3766d69c75765 |
| Annual / 37 | 79 | Separate labelled review, recalculated comparatives and annual production explanation | 6a2124705e9b65a9aef0f1dbec650086dfcec6e602e4c4e0a6ac793109e6cd76 |

Both monthly hashes match the earlier reported Step 4A hashes. Annual hashes
are newly recorded extraction output, not an independently recomputed audit.
The records show the intended explicit/unknown labels and separate notes.
Printing configured notes does not independently verify their source support or
prove the learner visually inspected the PDF. No new learner visual-comparison
confirmation is inferred from the GitHub Desktop screenshot.

With software tests, real batch coverage, core regression and detailed metadata
reviewed, a local version-control checkpoint is now appropriate. This advances
the earlier temporary instruction to hold uncommitted work: save these verified
implementation changes locally while keeping the two-note source-review
confirmation and understanding discussion explicit. A local commit is reversible
and does not publish code or close the entire Step 4 learning gate.

Suggested Desktop summary: feat: add verified PDF page evidence extraction.
Commit only config/retrieval.json, src/gacl_pipeline/retrieval.py and
tests/test_retrieval.py to feature/phase2-guided. Then share git status and the
latest commit line so the checkpoint can be recorded. CRLF/LF normalization in
the displayed JSON is ordinary Git text handling; it is not a change to PDF bytes.
The local commit, current clean status, documentation merge and learner visual
comparison of annual physical pages 1 and 37 remain unverified until supplied.
Step 5 still follows the remaining review and Step 4 checkpoint.

## Step 4B — commit, publication and source review verified, 27 November

The author supplied git status showing a clean feature/phase2-guided tracking
origin/feature/phase2-guided, and git log naming 29795de on both HEAD and the
remote-tracking ref. GitHub Desktop shows zero changed files. GitHub connector
readback independently confirms the published branch head as
29795de7be220373bd0a3ffbe779a44841b4a66a.

Commit: feat: add verified PDF page evidence extraction.
The new commit contains config/retrieval.json (20 lines),
src/gacl_pipeline/retrieval.py (266 lines), and tests/test_retrieval.py (180 lines).
The previously committed 103-line scripts/inspect_source_page.py is also present
on the published branch. No merge into public main is claimed.

The assistant read all four published application files and the branch AGENTS.md.
The extractor and tests match the Step 4B lesson after ignoring final newline
differences; the parsed JSON matches semantically despite indentation. The
review found no additional correction needed for the current lesson's scope.
The source register remains the existing approved structure; arbitrary external
manifest validation is outside this lesson. This is source review, not a newly
executed software/PDF/model/cloud run. Windows software/real-source results
remain the previously supplied evidence.

Before this documentation update, GitHub compared main at 4e051477 with feature
at 29795de as diverged: three feature-side commits and six main-side documentation
commits since merge base 3df36db. Feature-side changed files are exactly the
three Step 4B files plus the earlier inspector. Main-side changed files are
Markdown documentation only. A normal merge of refreshed origin/main into the
clean feature branch is appropriate; a fast-forward-only pull cannot combine
these two histories. This documentation update advances main again, so fetch
the latest ref rather than copying the recorded comparison SHA.

At this checkpoint the next commands were fetch origin, merge origin/main with
--no-edit, then push the feature branch and inspect status/log. The author has
subsequently performed that synchronization as recorded below. The assistant
did not merge or push the implementation branch.

## Step 4B — documentation merge and push verified, 27 November

The author supplied successful git fetch, merge and push output. Git used the
ort strategy to merge origin/main at 9a954b7 into feature/phase2-guided.
The merge changed nine Markdown files, with 1,527 insertions and 30 deletions,
including the two Step 4 lesson documents. It reported no conflicts.

The resulting merge commit is 53b9be45534a144ab5b2effbe99f3918173919bb.
The push advanced origin/feature/phase2-guided from 29795de to 53b9be4.
Supplied status is clean and tracking the remote. The graph preserves the
implementation history and newer main documentation.

GitHub connector readback independently confirms the feature head at 53b9be4.
Comparing 29795de to 53b9be4 shows only the nine intended Markdown paths changed;
application/configuration/test code is unchanged by the merge. This is Git/source
evidence, not a fresh runtime test. Previous 13/45 passing tests and real-source
coverage/core outputs remain the applicable execution evidence.

The Step 4 version-control checkpoint and batched documentation synchronization
are complete. Do not trigger another learner merge solely to receive this
evidence-recording update: collect subsequent documentation updates at the next
implementation checkpoint. A new main documentation commit after this record
does not undo the verified synchronization or invalidate the user's clean state
at the supplied checkpoint.

Remaining before Step 5: learner visual comparison of the annual notes with
physical PDF pages 1/37 (printed 43/79), and the separate understanding discussion.
Those confirmations have not been supplied and are not inferred from metadata
or Git output. No pull request, merge of feature code into main, chunker, model
or newly executed test/cloud run is claimed.

## Step 4 closed; Step 5 lesson supplied — 27 November

The author answered yes to the final question asking whether both annual review
notes agree with the visible report at physical pages 1 and 37 (printed 43/79),
and explicitly requested Step 5. Record this as the author's source-review
confirmation, not a new assistant PDF inspection or a new extraction/test run.
Together with the existing 13/45 Windows tests, real-source batch/core results,
detailed metadata and published clean merge 53b9be4, the Step 4 gate is closed.

The assistant's explanations and the learner's independent concept reflection
are separate. No independent explanation was supplied by the confirmation.
Reflection can continue during the next lesson; it is not a reason to repeat
verified checks or delay the expressly requested Step 5.

[Step 5](PHASE_2_STEP_05.md) is prepared from the actual published retrieval.py,
retrieval.json and test_retrieval.py at feature/phase2-guided 53b9be4.
It supplies exact insertions, a bounded main replacement, comments, concepts/ELI5
and verification commands. Only three existing implementation files are to be
edited by the learner; no new package is required. The assistant publishes
Markdown only, not application/configuration/test changes.

Planned current exercise: exact page-string spans, maximum 1,800 characters,
target overlap 250 with newline preference, preserved page offsets/provenance,
separate notes, deterministic chunk IDs and an in-memory --chunks command.
Existing page/all-page interfaces remain. A separate persisted index is Step 6.
Expected software totals are 28 retrieval tests and 60 full tests after 15 added
methods; these are not executed results. Real chunk counts must be measured.

Documentation review assembled the proposed insertions in memory, checked one
main/guard per file, counted the expected 28 retrieval test methods, parsed the
proposed JSON and checked Markdown fences/whitespace. Python source/test
execution and real chunk verification were not performed by those checks.
The user will run the implementation and supply actual evidence.

No immediate documentation merge is required. Read the new lesson online and
batch synchronization at the next reviewed implementation checkpoint.
The last actual local clean Git checkpoint remains 53b9be4 until new output
is supplied. Step 5 is open; no search, storage, model or generation run is claimed.

## Step 5 — initial Windows test errors diagnosed, 27 November

Evidence: uploaded Pasted text(20261127-070226).txt, read from the supplied scratch
attachment copy after the execution environment became ready. The attachment is
terminal output, not the full current source files. No implementation file was
changed by the assistant.

| Run | Author-supplied result |
|---|---|
| Retrieval tests | 28 run in 0.738 seconds; FAILED (errors=3), 25 completed successfully |
| Full suite | 60 run in 1.715 seconds; FAILED (errors=3), 57 completed successfully |
| String-level ChunkSpanTests | All 12 shown as passing |
| Existing Phase 1 / page tests | All shown as passing |
| Errors | The three new PageEvidenceTests integration cases |

The paste repeats several traceback fragments, particularly near the full-suite
summary. Record the final three-error count per run; do not count repeated text
as additional failed tests or independent runs.

Root evidence is KeyError: 'max_chunk_chars' at the direct self.settings lookup
inside test_invalid_chunk_settings_fail_before_pdf_read. The PageEvidenceTests
fixture lacks that exact key. The two other cases invoke extract_chunks with
the fixture's temporary root. settings.get yields None for the absent key;
the positive-integer validator raises ValueError. The CLI case catches that
error and exits with SystemExit: 1. These are related symptoms of the missing
fixture setting, not evidence of three separate chunk-boundary defects.

The real config/retrieval.json and self.settings in PageEvidenceTests.setUp are
independent configurations. write_config serializes the latter into a temporary
repository. Updating the real configuration does not update test fixtures.
The current real configuration contents are not established by this log.

Prescribed learner edit: inside tests/test_retrieval.py, PageEvidenceTests.setUp,
add/correct max_chunk_chars: 1800 and overlap_chars: 250 in the self.settings
dictionary, immediately after min_alnum_chars. Keep the existing fixture entries.
The missing maximum is confirmed; overlap must also be supplied as required by
the Step 5 interface. Do not weaken validation, add silent defaults or make the
isolated tests read production configuration.

Rerun the 28-test retrieval suite; after it passes, rerun the full 60-test suite.
Corrected output is pending. Step 5 real-PDF chunk counts, span/coverage/repeated-ID
checks, offline core rerun and Git checkpoint remain unverified for this lesson.
No success, code correction or new commit is claimed from the diagnosis alone.

## Step 5 — corrected tests and real-source chunk verification passed, 27 November

The author supplied the corrected Windows terminal runs directly. The three
previous fixture-related integration errors are absent and all named tests pass.
This confirms the rerun's behaviour; the exact uncommitted source edits have not
yet been read back from a published Step 5 commit.

| Check | Author-supplied result |
|---|---|
| Retrieval suite | 28 tests, 0.913 seconds, OK |
| Complete suite | 60 tests, 1.931 seconds, OK |
| Test composition | 32 core/cloud-boundary tests plus the same 28 retrieval tests; no failures/skips shown |
| Existing all-page CLI | 2 sources, 71 physical / 70 usable pages, one skipped monthly cover |
| Monthly chunks | 60 from 20 usable pages; approved monthly PDF hash matches |
| Annual chunks | 76 from 50 usable pages; approved annual PDF hash matches |
| Total chunks | 136 |
| Method/settings | line-window-v1; maximum 1,800 characters, target overlap 250 |
| Real span/coverage checks | 70 pages, 136 chunks; exact_spans_and_coverage=passed |
| Repeatability | stable_ids_across_two_runs=true |
| Offline run ID | f2d60348-903b-4438-a74f-ca4a01545c8a |
| Offline mode/status | cached_pdfs / success; pdfs_verified_this_run=true |
| Numerical observations | 18 extracted, 18 loaded, 18 stored |
| Dataset checks | All four passed; energy differences 0.002/0.00 GJ within 0.01 GJ |
| Git branch | feature/phase2-guided tracking its remote |
| Modified tracked files | config/retrieval.json; src/gacl_pipeline/retrieval.py; tests/test_retrieval.py |
| Tracked diff | Three files, 385 insertions, 14 deletions |
| Whitespace output | No whitespace errors reported; CRLF/LF normalization notices only |

The focused 28 tests are included in the complete 60, not additional tests.
The full suite's BigQuery tests use mocks; no fresh cloud/dbt/Power BI run is
implied. The 136 chunks are text passages, not new numerical observations.

The real verifier checks exact slices, valid/bounded offsets, progress and full
coverage to each page's end, parent text hashes, inherited source/scope/citation/
review metadata, unique IDs and identical ordered IDs across two actual batches.
The actual script uses normal interpreter execution. This is author-supplied
local evidence, not independent assistant rerunning of the Windows checkout.

The earlier reference prototype also happened to have 136 chunks; record this
as a new learner-executed result, not an inference from that prototype or a fixed
target. The observed maximum is the configured bound; overlap remains a target
and is not claimed to be exactly 250 in every pair.

Execution checks are passed. Next save the exact three modified files in a local
commit, message feat: add exact-span chunking with page provenance, then push the
already published feature branch. Share the resulting status/log for review.
The implementation remains on the author's laptop until that new commit is
published; connector readback currently still shows feature head 53b9be4.
No Step 5 commit, public source review, final checkpoint or Step 6 implementation
is claimed yet. Successful tests need not be repeated without a relevant change.
Documentation synchronization is batched after the reviewed implementation
checkpoint; this evidence update does not require an immediate documentation pull.

## Step 5 — published commit and source review verified, 27 November

The author supplied staging/check output for exactly the three intended paths,
then committed feat: add exact-span chunking with page provenance as 42c9ceb.
The push advanced origin/feature/phase2-guided from 53b9be4 to 42c9ceb.
Status is clean and tracks the remote; the log shows the same commit on HEAD
and origin/feature/phase2-guided. The wrapped word in the pasted log is display
formatting; the supplied commit command/message is recorded exactly above.

GitHub connector readback confirms
42c9cebf9ee61d14e1c05b1d86f59904390b5151. Comparing it with 53b9be4
shows one commit changing only config/retrieval.json,
src/gacl_pipeline/retrieval.py and tests/test_retrieval.py:
385 insertions / 14 deletions. No unrelated file or observation-parser change
is present in that comparison.

The assistant read the published module, configuration, tests, AGENTS.md,
.gitignore and dependency declaration. Reconstructing the supplied Step 5
insertions against 53b9be4 matches the published module after ignoring blank
lines, and matches the tests after ignoring blank lines and the two explanatory
fixture comments. Parsed retrieval JSON matches exactly. All 28 retrieval
test methods remain, and the repaired self.settings includes both required
chunk parameters. No source correction is needed for the current lesson.

This is read-only source comparison, not an assistant runtime rerun or a new
Windows/cloud/model execution. The prior 28/60 tests, real 136-chunk/70-page
coverage/ID checks and offline 18-fact run remain the applicable evidence.
The implementation source publication/review checkpoint is now complete.

Before this documentation update, main at dbf4bc9 and the feature at 42c9ceb
were diverged. The newer main changes are Markdown only; the feature preserves
the implementation. Refresh origin and normally merge origin/main into the
clean feature branch, then push and inspect status/history. The learner performs
these Git commands, as documented in Step 5. The assistant has not merged or
pushed the implementation branch in this update.

The remaining housekeeping is that single batched documentation synchronization.
Do not repeat successful tests just for a Markdown-only merge. Inspect and
share any actual merge error/conflict before pushing. Main still has no merged
learner application code; no PR or main merge is claimed. Step 6 is next after
the checkpoint: its index must be separate from the observations warehouse and
ignored by Git. The inspected .gitignore does not yet include data/retrieval/;
adding that rule belongs to the learner's Step 6 implementation. No index was
created by this review or documentation update.

## Step 5 synchronization complete; Step 6 supplied — 27 November

The author supplied a successful fetch/ort merge of origin/main 996ca93 into
feature/phase2-guided, then a successful push from 42c9ceb to 98c14ec.
Status is clean and tracking its remote; the graph preserves both histories.
The merge reports nine Markdown files, 1,285 insertions and 60 deletions,
including the new Step 5 lesson document.

GitHub connector readback confirms feature head
98c14ecdfa8bc55ad134772c1a3ba44bb3fbc907. Comparing 42c9ceb to 98c14ec
shows only those nine documentation paths changed. The already reviewed
application code and earlier 28/60 test and real-source evidence remain unchanged.
The Step 5 implementation/source/Git gate is complete. No runtime retest is
claimed for the documentation merge.

The assistant inspected the actual retrieval module, tests, retrieval settings,
.gitignore and package declaration at 98c14ec before preparing
[Step 6](PHASE_2_STEP_06.md). The learner will edit only .gitignore and the existing
module/test file. No new package or source is introduced. The new ignored target
is data/retrieval/index.sqlite, separate from data/warehouse/gacl.sqlite.

The lesson supplies commented schema/build/status code and 12 focused tests,
including persisted evidence, failed write/replacement preservation, changing
inputs, stale/missing indexes, manifest/count checks and warehouse preservation.
Expected totals are 40 retrieval / 72 full tests, not executed results.
Builds capture approved configuration and runtime fingerprints, verify the
temporary database before replacing the old file, and keep review notes in a
separate full-text column. Query/ranking logic is still Step 7.

Preparation checks: proposed Python module/tests parse, the 40 retrieval test
methods are counted, and the SQL schema/FTS fields were exercised in an in-memory
SQLite database. An additional isolated reference run executed the assembled
lesson examples in Linux/Python 3.12.14 with PyMuPDF 1.26.6: 40 retrieval tests
passed in 0.392 seconds, no errors/failures. Code was loaded in memory; synthetic
temporary PDFs/databases were cleaned up. No learner source/configuration/test/
ignore file was modified or created; only Markdown is published.

This is reference-example validation, not execution of the learner's Windows
application, the full 72-test suite, a real-PDF index or a Windows atomic rebuild.
Those user results remain pending.

Read the new lesson online. Do not start another documentation merge just to
receive this evidence update; batch subsequent documents at the next reviewed
implementation checkpoint. The last actual clean local head remains 98c14ec.
Step 6 implementation/execution is pending; no persisted learner index, keyword
search, model or cloud run is claimed.

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
| 27 November 2026 | Step 4B software verification | Focused suite: 13 tests OK in 0.634s; full suite: 45 tests OK in 1.620s; no failures/skips shown | Software checks passed; real-page fields, visual review and understanding pending |
| 27 November 2026 | Step 4B real-page metadata | Four expected page records supplied; monthly hashes match 4A; annual separate review fields and printed labels 43/79 recorded; Desktop shows three selected new files | Metadata passed; local checkpoint ready, commit and learner visual confirmation pending |
| 27 November 2026 | Step 4B commit/publication | Clean tracking branch and 29795de supplied; GitHub confirms published SHA; extractor/tests match lesson and JSON matches semantically; inspector present | Local/public feature checkpoint verified; documentation merge and learner visual confirmation pending |
| 27 November 2026 | Step 4B documentation synchronization | ort merge of origin/main 9a954b7 into feature; 53b9be4 pushed and clean; GitHub confirms head and Markdown-only changes since 29795de | Version-control checkpoint complete; learner source-review confirmation/understanding pending |
| 27 November 2026 | Step 4 completion / Step 5 start | Author confirms both annual notes match visible PDF pages and requests Step 5; exact chunking lesson prepared against published 53b9be4 | Step 4 closed; Step 5 implementation/execution pending |
| 27 November 2026 | Step 5 initial test diagnosis | 28 tests in 0.738s and 60 in 1.715s, each with three errors; 12 string chunk tests pass; traceback confirms missing max_chunk_chars in PageEvidenceTests fixture | Learner fixture repair and rerun pending; Step 5 open |
| 27 November 2026 | Step 5 corrected verification | 28 tests OK in 0.913s; 60 OK in 1.931s; 136 chunks (60 monthly/76 annual), 70 pages with exact coverage and stable IDs; offline f2d60348-903b-4438-a74f-ca4a01545c8a retains 18 facts/four passing checks; only three tracked implementation files modified | Execution checks passed; commit/publication/source-review pending |
| 27 November 2026 | Step 5 commit/publication/review | 42c9ceb pushed with clean tracking status; GitHub confirms SHA and three-file diff; module/tests/config match lesson apart from formatting and explanatory comments | Code checkpoint complete; batched documentation synchronization pending before Step 6 |
| 27 November 2026 | Step 5 synchronization / Step 6 preparation | 98c14ec merged/pushed and clean; GitHub confirms Markdown-only changes; Step 6 guide supplies separate atomic index, manifest/status and 12 tests; Python syntax and in-memory SQL/FTS checks passed | Step 5 complete; Step 6 learner implementation/execution pending |
