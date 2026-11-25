# AI extension — guided implementation log

Started: 25 November 2026 (India).

Build-order reference: [Master Build Order](PHASE_2_BUILD_ORDER.md), version 1.0,
30 stable steps in eight stages. Step 1 readiness execution: **passed**.
Step 2 baseline execution: **passed**.
Next: **Step 3, inspector code/instructions prepared; learner implementation pending**. Existing
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

## Next lesson — Step 3: verify and inspect one known PDF page

Follow [Step 3](PHASE_2_STEP_03.md) and personally create
scripts/inspect_source_page.py. Read the approved source configuration, hash and
parse the same cached PDF bytes, distinguish physical page 5 from library index
4, and print text with explicit printed-page metadata. No new dependency or
model is required. The assistant publishes documentation/code examples only,
not the application file. Learner implementation and execution are pending.

Before editing, receive the new documentation into the still-clean personal
branch using the lesson's Git instructions. Subsequent synchronization after
code commits must be reviewed rather than blindly assuming fast-forward.
Share results and explain why presence is weaker than hash verification,
why identical bytes are hashed/parsed, and why page numbering is converted.

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
| 25 November 2026 | Step 3 | Commented PDF-inspector lesson prepared; no application file created or executed by the assistant | Pending learner implementation |
