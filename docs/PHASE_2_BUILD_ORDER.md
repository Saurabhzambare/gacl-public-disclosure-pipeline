# Phase 2 — Public-Disclosure Research Assistant: Master Build Order

Version: 1.0. Prepared: 25 November 2026 (India).
Owner/implementer: Saurabh Zambare. Assistant responsibility: explanation,
review, troubleshooting and documentation maintenance.
Controlled steps: **30**, grouped into **8 stages**.
Readiness execution: **Step 1 passed on Windows, 25 November 2026**.
Baseline execution: **Step 2 passed on Windows, 25 November 2026**.
Step 3 checkpoint: **reviewed, duplicate removed, local commit 39ceacb; clean branch**.
Documentation synchronization: **latest merge 53b9be4 pushed; clean tracking branch verified, 27 November**.
Step 4A: **execution checks passed on Windows, 27 November 2026**.
Step 4: **execution, source-review confirmation and Git checkpoint complete, 27 November**.
Current lesson: **Step 5 exact-span chunking; instructions prepared, learner implementation/execution pending**.
Step 4B all-page extraction/configuration/tests and the annual-note visual
confirmation are complete. Gate A is closed; begin Step 5 in Stage B.
Learner understanding discussion is recorded separately in the learning log.

## Purpose and finished behavior

Extend the verified public-disclosure pipeline with a local research assistant
that retrieves evidence, reads validated measurements, calculates compatible
comparisons, generates cited answers and eventually chooses bounded read tools.
Power BI remains the reporting interface. Historical public reports do not give
the assistant live plant readings or private GACL access.

ELI5: build a librarian to find pages, an accountant to read checked numbers,
a calculator for comparisons and a writer to explain the evidence. Only after
those work do we let a coordinator decide which tools a question needs.

## Snapshot, not a completion claim

- Phase 1: 18 verified observations; local pipeline, BigQuery/dbt reference
  checks and Desktop refresh recorded in [verification](VERIFICATION_2026-11-24.md).
- A reference prototype exists locally on `feature/document-retrieval`: 70
  indexed text pages, 136 chunks and a 40-case page-retrieval pilot. Its Windows
  execution and public publication are pending. See [pilot results](RETRIEVAL_EVALUATION.md).
- Learner completion is tracked separately. No Phase 2 learner step is marked
  complete merely because the assistant previously prepared a prototype.
- Embeddings, generated answers, numerical assistant tools, agents and UI remain
  planned. No model/provider, UI framework or additional dependency is selected
  by this document. There is no committed Phase 2 deadline or runtime promise.

## Execution and teaching rules

Work on **one current step at a time**. For each lesson use this order:
concept → ELI5 → technical purpose → architecture position → prerequisites →
exact file/insertion instructions → commented implementation → run → verify →
review output → understanding check → documentation/checkpoint → next step.

Saurabh edits application code, tests, configuration and dependency files.
The assistant edits documentation independently. Do not install packages,
overwrite prototype modules, refactor, create future source files, run paid
services or advance several lessons autonomously. Classes are optional; use
one only when it makes the current responsibility clearer.

Every lesson supplies commented code explaining function/class responsibilities,
parameters, return values and important variables. Exact code is supplied for
the active lesson after inspecting the learner's checkout; this roadmap is not
an instruction to paste a complete application or create every listed file now.
If a target already exists, inspect it first and specify a bounded insertion or
replacement; never instruct the learner to overwrite an unexplained module.

Each step closes with actual output and a short explanation from the learner.
An error or missing prerequisite keeps the step open. Commit messages below are
suggestions after reviewed local changes; no automatic push, merge, publication
or deployment is authorized. Do not discard existing uncommitted work.

Stable numbering: preserve Steps 1–30. Explain and document any proposed change
before adopting it. A necessary small substep can use an identifier such as
12a without silently renumbering later lessons. Update version and learning log
when the agreed sequence changes.

## Stage overview and gates

| Stage | Steps | Dependency | Exit evidence |
|---|---|---|---|
| A. Readiness and source evidence | 1–4 | Existing Phase 1 project | Correct environment; verified page text and provenance |
| B. Keyword retrieval and baseline | 5–10 | Gate A | Reproducible index, safe search, reviewed cases and Windows results |
| C. Pretrained semantic retrieval | 11–15 | Gate B | Pinned model/index and measured comparison with lexical baseline |
| D. Numerical evidence tools | 16–18 | Gate C | Read-only exact values, comparisons and identified check evidence |
| E. Cited generative answers | 19–22 | Gate D | Tested generation contract, useful answers and honest abstention |
| F. Bounded agent | 23–25 | Gate E | Model-selected tool traces, limits and evaluated stop behavior |
| G. Demonstration interface | 26–27 | Gate F | Local UI exposes evidence, calculations and tool results |
| H. Verification and packaging | 28–30 | Gate G | Regression/evaluation evidence, demonstration and reviewed release candidate |

All paths below are relative to the repository root, normally
`D:\gacl-public-disclosure-pipeline` on the learner's Windows laptop. Paths
marked **planned** are design targets, not files generated by this documentation
update. Exact future commands are introduced only when their modules exist.

## Stage A — Readiness and source evidence

### Step 1 — Inspect the existing Windows environment

- **Depends on:** no new Phase 2 step.
- **Purpose / why:** identify the branch, changes, interpreter, PDF library,
  SQLite FTS5 support and configured cached PDFs before changing code.
- **ELI5:** check the toolbox and the two books.
- **Files / installation:** read `pyproject.toml`, `config/sources.json`,
  `.venv` and `data/raw`; create no source file. Reuse Python 3.11+ and existing
  PyMuPDF 1.26.6. Repair only a demonstrated missing prerequisite.
- **Action / output:** run the PowerShell/in-memory readiness check supplied in
  [the standalone Step 1 lesson](PHASE_2_STEP_01.md); share branch/commit,
  versions, FTS5 result and PDF presence.
- **Gate / understanding:** explain why the project interpreter matters and why
  a present PDF is not yet a verified PDF. Record output in the learning log.

### Step 2 — Record a baseline and isolate personal implementation

- **Depends on:** Step 1 passing or its missing prerequisites resolved.
- **Purpose / why:** protect working Phase 1 behavior and establish which
  reference files exist in the learner's actual checkout.
- **ELI5:** photograph the working machine before attaching a new part.
- **Files / installation:** inspect Git changes, existing retrieval modules,
  `tests/` and core outputs. No new package. Branch choice follows inventory;
  never switch with unexplained changes or copy the entire prototype blindly.
- **Action / output:** follow [the Step 2 lesson](PHASE_2_STEP_02.md), run the
  existing unit suite and an offline core run; retain counts and actual failures.
- **Gate / understanding:** identify 18 observations versus software-test count;
  explain the difference between the assistant's local prototype and your work.
  Checkpoint suggestion: `docs: record guided AI implementation baseline`.

### Step 3 — Verify and inspect one known PDF page

- **Depends on:** Step 2.
- **Purpose / why:** personally trace bytes → approved hash → page → raw text.
- **ELI5:** check the book's fingerprint, then read the correct page.
- **Files / installation:** **planned** `scripts/inspect_source_page.py`; read
  `config/sources.json` and the cached monthly PDF. Reuse PyMuPDF and standard
  library hashing; no model or OCR dependency.
- **Action / output:** follow [the Step 3 lesson](PHASE_2_STEP_03.md), implement a
  small commented inspector, verify SHA-256 before reading, and print PDF page 5
  text and known printed-page metadata.
- **Gate / understanding:** find April's disclosed 12,540.8 KL/day and distinguish
  human page 5 from zero-based library index 4. A wrong hash must stop extraction.
  This is a learning inspector, not a replacement for the existing fact parser.

### Step 4 — Define page evidence and extract usable pages

- **Depends on:** Step 3.
- **Purpose / why:** preserve source/version/page addresses before searching.
- **ELI5:** every reading card must have a trustworthy address.
- **Files / installation:** existing/reference `src/gacl_pipeline/retrieval.py`
  and `config/retrieval.json`, introduced incrementally if absent; focused tests
  in `tests/test_retrieval.py`. See [contracts](AI_CONTRACTS.md).
- **Action / output:** extract page text, retain hashes, use explicit printed
  mappings, separate reviewed notes and record image-only/insufficient pages.
- **Gate / understanding:** explain extraction versus OCR and unknown printed
  pages; reject missing required evidence instead of inventing text or labels.
  Gate A: source/version/page metadata is inspectable and correct.
- **Teaching subdivisions:** [4A](PHASE_2_STEP_04.md) returns one structured page;
  [4B](PHASE_2_STEP_04B.md) supplies all-page extraction, metadata configuration
  and focused tests after review of the learner's actual 4A module. These
  preserve the same 30 numbered steps. Do not mark Step 4 complete after 4A alone.

## Stage B — Keyword retrieval and baseline

### Step 5 — Implement exact-span chunking with overlap

- **Depends on:** Step 4, now complete.
- **Lesson / status:** [Step 5 detailed lesson](PHASE_2_STEP_05.md), prepared after
  inspecting the published 53b9be4 files; implementation/execution pending.
- **Purpose / why:** create manageable passages without losing their locations.
- **ELI5:** split a long page into overlapping reading cards.
- **Files / installation:** `retrieval.py` chunking helpers, `config/retrieval.json`
  and focused chunk tests; no dependency change.
- **Action / output:** use the reference baseline's 1,800-character maximum and
  250-character target overlap, prefer line boundaries and stay within a page.
- **Gate / understanding:** recover every chunk from its recorded page offsets;
  test forward progress and boundary cases. Explain why overlap is approximate
  and why a chunk may still lack the table's header or year context.

### Step 6 — Build a separate, replaceable search index

- **Depends on:** Step 5.
- **Purpose / why:** persist evidence without modifying the observation warehouse.
- **ELI5:** build a catalogue beside the checked ledger.
- **Files / installation:** `retrieval.py` index builder; generated
  `data/retrieval/index.sqlite` stays ignored. SQLite comes with Python; verify
  FTS5 capability rather than installing an unrelated package.
- **Action / output:** store documents, pages, chunks and versioned manifest;
  build into a temporary file, close it, then replace the target after success.
- **Gate / understanding:** same inputs give stable chunk IDs; failed rebuild
  preserves the old index; stale configuration requires rebuild. Explain atomic
  replacement and why a hash is integrity evidence, not a security signature.

### Step 7 — Add safe keyword retrieval and ranking

- **Depends on:** Step 6.
- **Purpose / why:** create a simple measurable search baseline before ML.
- **ELI5:** find passages using matching words, then order the candidates.
- **Files / installation:** `retrieval.py` query processing/search and its tests.
- **Action / output:** tokenize questions, quote literal terms, use parameterized
  source/scope filters, Porter stemming and BM25; return distinct source/pages.
- **Gate / understanding:** test malformed inputs and SQL/FTS-like text; verify
  filters apply before ranking/cutoff. Explain that a rank is not confidence and
  a relevant passage is not automatically a supported answer.

### Step 8 — Expose page lookup and search commands

- **Depends on:** Step 7.
- **Purpose / why:** make evidence inspectable before adding generated language.
- **ELI5:** let a reviewer open the actual page behind a search result.
- **Files / installation:** `retrieval.py` CLI/page reader and tests. Existing
  interface uses build/info/search/page/evaluate subcommands; keep compatibility
  when an existing implementation is present.
- **Action / output:** return exact passage, document hash, page and official
  citation URL; validate chunk/page consistency; report errors clearly.
- **Gate / understanding:** open the monthly PDF page 5 evidence and explain
  `answer=null` / `answerability=not_assessed` in current search output. Missing
  index should explain the repair and must not create an empty warehouse.

### Step 9 — Review and version evaluation questions

- **Depends on:** Step 8.
- **Purpose / why:** define useful and unsupported questions before tuning.
- **ELI5:** write the marking guide before grading the search engine.
- **Files / installation:** `evaluation/retrieval_cases.json`, evaluation docs
  and a **planned** independently reviewed case file, named at this lesson.
- **Action / output:** inspect all 40 pilot cases and expected source/pages,
  numeric references and separate annotations; correct documented mistakes.
  Reserve newly authored, independently reviewed questions for stronger final
  evaluation; record who reviewed them and freeze their version.
- **Gate / understanding:** explain development versus holdout and why the
  already-inspected two-document pilot is not an independent unseen exam.

### Step 10 — Measure and freeze the Windows lexical baseline

- **Depends on:** Step 9.
- **Purpose / why:** establish a reproducible benchmark before adding embeddings.
- **ELI5:** time and score the first librarian before hiring a second.
- **Files / installation:** `retrieval_eval.py`, tests and curated evaluation
  documentation. No model dependency; raw run outputs remain ignored.
- **Action / output:** build on the learner's Windows machine, measure page
  Recall@5/MRR@5, inspect misses and run regression tests. Record versions and
  timings rather than assuming the Linux prototype's counts or results.
- **Gate / understanding:** explain page retrieval versus answer accuracy and
  keep 12 diagnostic cases separate from the 28 scored pilot cases.
  Gate B checkpoint suggestion: `feat: verify cited lexical retrieval on Windows`.

## Stage C — Pretrained semantic retrieval

### Step 11 — Select and benchmark an embedding model

- **Depends on:** Step 10.
- **Purpose / why:** choose a pretrained model that fits the actual laptop and
  permits intended use before adding dependencies.
- **ELI5:** try a small meaning-matching tool before buying a larger toolbox.
- **Files / installation:** inspect official model/runtime documentation, license,
  immutable revision, download size, supported Python and CPU/RAM behavior.
  Only this lesson supplies exact vetted installation/version commands.
- **Action / output:** run a small embedding smoke test and record dimensions,
  download/runtime observations and chosen similarity convention.
- **Gate / understanding:** explain inference versus training; model selection
  must be evidence-based. No promise that a 4 GB GPU can run a chosen generator.

### Step 12 — Create a reproducible embedding adapter

- **Depends on:** Step 11.
- **Purpose / why:** isolate model loading and encode text consistently.
- **ELI5:** use the same coordinate system for every card and question.
- **Files / installation:** **planned** `src/gacl_pipeline/semantic.py`,
  `tests/test_semantic.py`, `config/ai.json` and an optional dependency group
  chosen in Step 11. No secrets in configuration.
- **Action / output:** encode chunks and queries with the selected model's
  required text prefixes, vector normalization and pinned revision.
- **Gate / understanding:** validate nonempty text, dimensions and finite values;
  tests use controlled model substitutes, with a separate real-model smoke test.
  Explain why vectors from different models cannot silently share an index.

### Step 13 — Persist a versioned semantic index

- **Depends on:** Step 12.
- **Purpose / why:** avoid re-encoding all passages on every question and detect
  changes in the model, text or extraction configuration.
- **ELI5:** save the meaning map with a label saying how it was made.
- **Files / installation:** `semantic.py` and tests; **planned** generated
  artifacts under ignored `data/retrieval/`, separate from fact storage.
- **Action / output:** map vectors to canonical chunk IDs; record model/revision,
  dimensions, normalization and source/chunk fingerprints; rebuild safely.
- **Gate / understanding:** stale or dimension-mismatched indexes fail visibly;
  rebuilding cannot mutate the 18 authoritative observations. Choose a minimal
  persistence format; a hosted vector database is not a prerequisite.

### Step 14 — Implement semantic search with matching filters

- **Depends on:** Step 13.
- **Purpose / why:** retrieve by semantic similarity while preserving the same
  source/page and scope semantics as keyword search.
- **ELI5:** find nearby cards on the meaning map and keep their addresses.
- **Files / installation:** `semantic.py`, its tests and the existing CLI only
  through an explicit reviewed addition; no future command name assumed here.
- **Action / output:** use exact vector similarity for this small corpus,
  apply allowed filters, return canonical evidence and deduplicate page results.
- **Gate / understanding:** explain cosine similarity and why it is not truth
  or calibrated answer confidence. Test unknown filters and stale model metadata.

### Step 15 — Compare methods and choose the retrieval policy

- **Depends on:** Step 14.
- **Purpose / why:** justify ML by measured usefulness, not by adding a model name.
- **ELI5:** ask both librarians comparable questions and inspect their mistakes.
- **Files / installation:** evaluation code/results and **planned**
  `src/gacl_pipeline/ai_eval.py` if an additional evaluator is needed.
- **Action / output:** compare lexical and semantic retrieval on the same evidence
  definitions; report development results, frozen-set protocol, latency and RAM.
  Consider hybrid retrieval or reranking only if errors justify an explicit task.
- **Gate / understanding:** publish actual wins and losses in curated local docs;
  do not tune on a final set and call it unseen. Gate C checkpoint suggestion:
  `feat: benchmark pretrained semantic retrieval against lexical search`.

## Stage D — Numerical evidence tools

### Step 16 — Implement a read-only metric lookup

- **Depends on:** Step 15.
- **Purpose / why:** numerical answers must use validated observations instead
  of guessing PDF columns or relying on a model's memory.
- **ELI5:** ask the checked ledger for the number.
- **Files / installation:** **planned** `src/gacl_pipeline/metric_tools.py` and
  `tests/test_metric_tools.py`; reuse SQLite and Decimal.
- **Action / output:** select by explicit metric, scope, period and document
  version where necessary; return exact value, unit, raw value and provenance.
- **Gate / understanding:** parameterized read-only queries; reject unsupported
  or ambiguous keys/revisions; no missing database silently created. Explain
  why a company total cannot answer a site-only question.

### Step 17 — Calculate compatible comparisons

- **Depends on:** Step 16.
- **Purpose / why:** arithmetic needs explicit inputs, matching definitions and
  reproducible formulas.
- **ELI5:** let the calculator work only on matching kinds of numbers.
- **Files / installation:** `metric_tools.py` and focused comparison tests.
- **Action / output:** use Decimal for later-minus-earlier and percentage change;
  return both source records, formula, exact results and separate display rounding.
- **Gate / understanding:** April-to-September rate change is -802.7 KL/day,
  approximately -6.40%; it is not total water saved. Handle zero denominator,
  missing values, metric/unit/scope mismatch and ambiguous document versions.

### Step 18 — Expose identified validation evidence

- **Depends on:** Step 17.
- **Purpose / why:** answer questions about recorded checks without inventing
  a new successful run or confusing counts with tests.
- **ELI5:** read the dated inspection sheet, not a guessed current status.
- **Files / installation:** `metric_tools.py` or a small explicitly justified
  check reader; inspect actual existing run/check artifacts before implementation.
- **Action / output:** require a run identifier and return check ID, result,
  detail and evidence location; distinguish unknown run and unavailable detail.
- **Gate / understanding:** last-known results are historical, not a live plant
  health verdict. Gate D checkpoint suggestion:
  `feat: add validated read-only metric and check tools`.

## Stage E — Cited generative answers

### Step 19 — Select and benchmark the generation route

- **Depends on:** Step 18.
- **Purpose / why:** choose a usable language model/runtime without assuming
  laptop performance, licenses, free API access or willingness to spend.
- **ELI5:** test whether the writer fits the desk and the budget.
- **Files / installation:** document the model/provider decision, immutable model
  version where available, context limits and exact dependencies at this lesson.
- **Action / output:** benchmark a local route first where practical; an external
  paid API is a separate explicit cost/provider decision before use. Confirm what
  text would leave the laptop. Do not create keys in committed files.
- **Gate / understanding:** explain model tokens, context, inference, generation
  and limits; record measured memory/time and actual cost basis, not a forecast.

### Step 20 — Implement the generation and answer contracts

- **Depends on:** Step 19.
- **Purpose / why:** separate provider calls from evidence assembly and output
  validation so a runtime can be replaced or unavailable without corrupting facts.
- **ELI5:** give the writer a clear assignment and a standard answer sheet.
- **Files / installation:** **planned** `src/gacl_pipeline/generation.py`,
  `tests/test_generation.py`; use [contracts](AI_CONTRACTS.md).
- **Action / output:** version instructions; bound context/output; validate cited
  evidence IDs and supported result states; label provider failures explicitly.
- **Gate / understanding:** mocked tests differ from a real-model smoke test;
  a schema-valid answer can still be factually wrong. No model-supplied number
  may replace the authoritative metric/calculation result.

### Step 21 — Assemble a fixed RAG answer workflow

- **Depends on:** Step 20.
- **Purpose / why:** combine retrieval, full-page context where needed, facts
  and generated explanation before introducing autonomous tool selection.
- **ELI5:** librarian and accountant give evidence to the writer in a known order.
- **Files / installation:** **planned** `src/gacl_pipeline/assistant.py` and
  `tests/test_assistant.py`; reuse earlier modules rather than duplicate storage.
- **Action / output:** handle documented question categories, request clarification
  for ambiguous scope/period, preserve citation/version metadata and return
  insufficient evidence when the available sources do not support an answer.
- **Gate / understanding:** show a text question, numerical comparison and unknown
  question end-to-end. Explain why this predetermined workflow is not an agent.

### Step 22 — Evaluate answers and adversarial requests

- **Depends on:** Step 21.
- **Purpose / why:** useful retrieval alone does not establish faithful answers.
- **ELI5:** check both the page the writer used and every claim it wrote.
- **Files / installation:** AI evaluation code, reviewed answer cases and curated
  results; raw prompts/responses remain ignored until reviewed for publication.
- **Action / output:** measure exact numeric correctness, citation validity and
  support, claim faithfulness, clarification/abstention and response time. Test
  injected document instructions and unsupported causes or private information.
- **Gate / understanding:** apply targets in [evaluation plan](AI_EVALUATION_PLAN.md)
  with actual denominators and failure examples. Gate E checkpoint suggestion:
  `feat: verify evidence-grounded RAG answers`.

## Stage F — Bounded agent

### Step 23 — Register validated read tools and limits

- **Depends on:** Step 22.
- **Purpose / why:** a model must choose among limited capabilities, not arbitrary
  code, SQL writes or network operations.
- **ELI5:** give the coordinator approved buttons, not keys to the whole building.
- **Files / installation:** **planned** `src/gacl_pipeline/agent.py`,
  `tests/test_agent.py`; tool schemas use the established evidence contracts.
- **Action / output:** validate names/arguments, output limits, timeouts and
  document IDs; reject shell, write-SQL, credential and external-message requests.
- **Gate / understanding:** define a starting six-call cap and bounded provider
  calls; malformed arguments and unavailable tools produce explicit results.
  Explain that tool descriptions do not replace enforcement in application code.

### Step 24 — Implement model-selected tool use and traces

- **Depends on:** Step 23.
- **Purpose / why:** let different questions trigger appropriate follow-up work
  while preserving evidence and execution limits.
- **ELI5:** the coordinator picks the next approved button based on the result.
- **Files / installation:** `agent.py` and its tests; add a framework only after
  explaining why a small explicit loop is insufficient for this task.
- **Action / output:** model selects tools, validated functions run, structured
  results return, then the model finishes or requests another allowed tool.
  Record calls, arguments, evidence and outcomes; do not request hidden reasoning.
- **Gate / understanding:** demonstrate genuinely different useful call sequences
  and termination. A fixed sequence cannot be relabelled agentic behavior.

### Step 25 — Evaluate agent routing, stopping and replay

- **Depends on:** Step 24.
- **Purpose / why:** correct answers must also come from permitted, bounded actions.
- **ELI5:** check that the coordinator presses the right buttons and stops.
- **Files / installation:** agent tests, AI evaluation cases and curated traces.
- **Action / output:** test tool choice, repeated calls, budget exhaustion,
  timeouts, injected instructions, wrong scope and numeric/citation consistency.
  Reproduce deterministic tool evidence from recorded arguments and versions.
- **Gate / understanding:** distinguish reproducible tool replay from identical
  stochastic model output; log actual failures. Gate F checkpoint suggestion:
  `feat: evaluate bounded model-selected research tools`.

## Stage G — Demonstration interface

### Step 26 — Select and create a minimal local interface

- **Depends on:** Step 25.
- **Purpose / why:** make the working assistant reviewable without burying
  incomplete contracts behind a polished screen.
- **ELI5:** add a clear front desk after the back-office tools work.
- **Files / installation:** **planned** `src/gacl_pipeline/assistant_ui.py` or an
  explicitly documented alternative if the chosen framework requires it. Select
  and pin a minimal framework only at this lesson.
- **Action / output:** show question input, source/scope context, result state,
  answer, evidence, calculation details and tool outcomes.
- **Gate / understanding:** label historical public data and model/index versions;
  no key displayed or hidden dependency on cloud reporting. Record local launch
  command after it exists. Do not imply public hosting.

### Step 27 — Integrate and manually review interface behavior

- **Depends on:** Step 26.
- **Purpose / why:** the reader must be able to inspect evidence and recognize
  stale data, missing models and unsupported requests.
- **ELI5:** make the front desk explain both results and problems clearly.
- **Files / installation:** UI integration, appropriate tests and runbook updates.
- **Action / output:** exercise supported/unknown/ambiguous questions, open source
  page links, inspect calculations and verify loading/error behavior.
- **Gate / understanding:** no silent fallback to fabricated answers or a different
  model; escaped text cannot become executable UI content. Gate G checkpoint
  suggestion: `feat: expose cited research answers in a local interface`.

## Stage H — Verification and packaging

### Step 28 — Run the full regression and evaluation sequence

- **Depends on:** Step 27.
- **Purpose / why:** confirm the new assistant preserves the original verified
  data/reporting foundation and passes its own acceptance checks.
- **ELI5:** inspect the complete machine, including the old parts.
- **Files / installation:** existing tests, actual model smoke tests, evaluation
  outputs and curated verification docs; no dependency upgrade just for release.
- **Action / output:** run Python tests, real cached-PDF extraction/reconciliation,
  index rebuild/search and answer/agent evaluation on Windows. Record versions,
  data/model/index IDs and exact failures. Cloud/PBI reruns are separate explicit
  checks when changed or needed, not a hidden prerequisite for every AI question.
- **Gate / understanding:** unchanged facts remain 18 selected observations;
  never add unlike test/check counts together or infer unrun cloud verification.

### Step 29 — Record the demonstration and final evidence

- **Depends on:** Step 28.
- **Purpose / why:** demonstrate inspectable behavior and learning, not only a
  feature list or target metrics.
- **ELI5:** show a real question, the evidence, the calculation and a known limit.
- **Files / installation:** update walkthrough, README, status, model/index and
  evaluation records. Save a recording locally; publish only separately authorized.
- **Action / output:** capture factual lookup, comparison, reporting definition,
  insufficient-evidence answer and bounded agent trace using the actual build.
- **Gate / understanding:** explain one failure and its limits; distinguish
  pretrained model use from custom training and search metrics from answer quality.

### Step 30 — Review a release candidate and remaining work

- **Depends on:** Step 29 and documented resolution of release-blocking failures.
- **Purpose / why:** make claims, setup and artifacts match what actually runs.
- **ELI5:** check the label matches the contents before sharing the box.
- **Files / installation:** inspect staged diff, dependency/model licenses,
  source attribution, instructions, evaluation summaries and excluded artifacts.
- **Action / output:** prepare reviewed local commits and a concise release/PR
  description with verified scope and remaining limitations. Pushing, merging,
  hosting and outreach need their own authorization; no publication is part of
  this documentation update.
- **Gate / understanding:** Gate H checkpoint suggestion:
  `docs: package verified research-assistant evidence and limitations`.
  Future forecasting needs a separately approved suitable dataset and evaluation.

## Progress and resumption

Steps 1–3 execution checks passed on Windows, and Step 3's local-file review and
commit checkpoint closed with 39ceacb on a clean personal branch. Documentation
synchronization at merge a5001c0 is also verified. Step 4A execution checks passed on 27 November. Review the learner's actual\nmodule before 4B edits; 4B and the overall Step 4 gate remain pending. Steps 5–30 remain pending. Understanding discussion remains recorded separately. Do not pre-check the roadmap
because a reference module exists. In [AI_LEARNING_LOG.md](AI_LEARNING_LOG.md),
record current step ID, actual files changed, commands/results, explanation in
the learner's words, errors/fixes and next step. [STATUS.md](STATUS.md) tracks
verified product capability separately from teaching progress.

To resume in a fresh conversation: identify build-order version 1.0, the last
completed step, the current step, relevant file contents and latest terminal
output. Continue from that step; do not regenerate a different numbered plan.
