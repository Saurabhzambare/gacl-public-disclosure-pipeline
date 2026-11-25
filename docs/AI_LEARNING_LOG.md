# AI extension — guided implementation log

Started: 25 November 2026 (India).

Build-order reference: [Master Build Order](PHASE_2_BUILD_ORDER.md), version 1.0,
30 stable steps in eight stages. Step 1 readiness execution: **passed**.
Next: **Step 2, instructions prepared; learner execution pending**. Existing
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

## Next lesson — Step 2: baseline and personal implementation branch

Follow [Step 2](PHASE_2_STEP_02.md): inspect the checkout, receive the documentation
update while clean/on main, create a personal branch, inventory prototype-file
presence, run existing tests and the original offline pipeline. All Step 2
results remain pending. Do not skip directly to PDF code: the inspector is
**Step 3** in the stable build order.

Understanding check to discuss with the Step 2 results: why does PRESENT not
prove that a PDF has the approved content, and why do we use the project's
virtual-environment interpreter rather than a generic python command?

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
| 25 November 2026 | Step 2 | Baseline/branch lesson prepared; no learner test, pipeline or branch output supplied yet | Pending execution |
