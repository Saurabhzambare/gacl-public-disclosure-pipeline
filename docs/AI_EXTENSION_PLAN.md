# Phase 2 — AI-assisted public-disclosure analysis

Prepared: 24 November 2026.
Updated: 25 November 2026. This is the Phase 2 product/architecture scope. Execute
the [Master Build Order](PHASE_2_BUILD_ORDER.md) version 1.0: 30 stable steps,
eight stages, learner Step 1 pending. Saurabh implements code/configuration/tests;
the assistant maintains documentation and teaches one step at a time. The
earlier prototype remains reference material, not learner completion evidence.
Status: Milestone 1 lexical retrieval is implemented and locally verified on
feature/document-retrieval; see RETRIEVAL.md and RETRIEVAL_EVALUATION.md.
Embeddings, generation, numerical answer tools and agents remain planned. The completed Python/SQLite/BigQuery/dbt/Power BI foundation
remains the verified first version. This plan does not publish a new release,
change data sources, install models, enable cloud billing or call paid model APIs.

## Product and intended user

Build a Public-Disclosure Research Assistant that helps a reviewer answer:

- What did GACL disclose about water and energy, and where is the evidence?
- How do two compatible disclosed measurements compare?
- What reporting boundary or methodology qualifies an answer?
- Which recorded data checks passed or failed, and what evidence explains them?

Use the existing approved public documents and validated observations first.
Retain the independent portfolio identity. Historical public data does not
provide live plant access, equipment labels or evidence of operational causes.

## Features and their meaning

| Capability | Proposed implementation | Evidence required before completion claim |
|---|---|---|
| ML for retrieval | Use a pretrained embedding model to rank page-aware text chunks; compare against lexical retrieval | Held-out question/page judgments, retrieval metrics and recorded model revision |
| RAG | Retrieve relevant evidence, then generate a concise answer with report/page citations | Citation correctness, factual support and appropriate abstention on unanswered questions |
| Numerical analysis | Read approved metrics through parameterized read-only functions; calculate with Decimal | Every supported numerical answer agrees with validated facts and retains units/scope |
| GenAI summaries | Generate explanations of retrieved passages and calculated comparisons | No invented causal explanation, certification or operational claim; references support each factual assertion |
| Agentic investigation | Let a tool-calling model choose approved read tools and follow-up queries within a bounded budget | Trace demonstrates dynamic tool selection, correct results, stop behavior and reproducible replay |
| Future custom predictive ML | Obtain compatible history/labels, define a target and evaluate against simple baselines | Separate approved dataset, chronological/group holdout where appropriate, baseline comparison and error analysis |

Pretrained embeddings constitute an ML application, not a model trained on these
18 observations. The first extension should not claim forecasting, predictive
maintenance, anomaly-detection performance or a custom trained model. Current
facts cover only six monthly points and two annual periods across different
metrics and grains. More varied records are not automatically more training
examples for one target.

## Architecture and contracts

Keep two evidence routes:

1. Document route: verified PDF bytes → page text → page-aware chunks →
   lexical and embedding retrieval → optional reranking → cited passages.
2. Facts route: validated SQLite observations → parameterized metric retrieval →
   deterministic comparison → cited values and calculation provenance.

The answer service selects the relevant route, or combines both. A model may
explain a calculation but must not supply its authoritative input values or
perform the final numerical arithmetic. Annual and monthly results must retain
separate labels and cannot be summed together.

The current lexical prototype uses exact, line-aware character windows, not
general heading/table reconstruction. Preserving complete year/unit/header
context is an explicit implementation/review requirement; do not describe all
tables as parsed merely because their pages were indexed. Detailed evidence and
proposed tool contracts are in [AI_CONTRACTS.md](AI_CONTRACTS.md).

Every chunk should carry: chunk_id, source_id, document_sha256, PDF page,
printed page if known, section, reporting_scope where established, exact text,
text hash, and extraction/index version. A chunk ID must change if content or
its source version changes. Printed-page mapping is explicit metadata; do not
assume a universal offset across the reports.

Store document/index artifacts locally outside Git and separately from the
validated observation warehouse. An index build verifies source bytes, records
its embedding model revision, parameters and a manifest, and fails visibly when
required extraction is missing. Preserve table headings, year columns, units and
footnotes; image-only or garbled passages need explicit review/OCR handling.
Chunking all pages must not silently imply every table was parsed correctly.

For this small corpus, exact vector similarity is enough for a first embedding
baseline. A vector database is an optional later persistence choice, not a
prerequisite. Index all usable pages from the two already approved documents;
measure retrieval before adding further reports. Any new source requires its
own provenance/boundary/version review.

## Read tools for a bounded assistant

Proposed interfaces:

- search_documents(query, source_id, reporting_scope, top_k)
- get_source_page(source_id, document_sha256, pdf_page)
- get_metric(metric_id, reporting_scope, period_start, period_end)
- compare_metric(metric_id, reporting_scope, earlier_period, later_period)
- get_check_results(run_id)

Functions validate parameters and return structured evidence. The first release
has no arbitrary shell, write-SQL, manifest editing, external messaging or plant
control tool. Enforce a maximum number of tool calls, timeout, output size and
model-token budget. Record tool names, validated arguments, evidence IDs and
outcome. A fixed sequence is a workflow; use the term agentic only after a model
actually selects tools and follow-up steps dynamically in a tested run.

Treat document text as evidence, never as operating instructions. Embedded
requests to ignore policies, run code or reveal credentials must not alter tool
permissions. Absent facts produce an explicit insufficient-evidence answer.
Document versions and comparative-year notes must remain visible. Model output
cannot certify environmental compliance or explain plant causes without evidence.

Example tasks:

- 'What was April 2025 freshwater use?' → metric function, 12,540.8 KL/day,
  Dahej Plot 3 report, PDF page 5/printed page 4.
- 'How did April compare with September?' → compatible monthly rates,
  deterministic difference/percentage, both references and rate interpretation.
- 'What is the annual reporting boundary?' → source page identifying standalone.
- 'Why did water use fall?' → report any explicit retrieved explanation, or say
  that the available evidence does not establish the cause.
- 'Which April–September coverage check passed?' → existing run evidence.

## Delivery order and gates

The milestones below group capabilities. The numbered build order controls
individual lessons and adds a separate validated-numerical-tools stage before
answer generation. Gate targets are prospective; evaluation protocols and
denominators are specified in [AI_EVALUATION_PLAN.md](AI_EVALUATION_PLAN.md).
There is no new fixed completion deadline, model purchase or deployment decision.

### Milestone 1 — Evidence index and evaluation set

Deliver verified page/chunk ingestion, explicit page metadata, a lexical baseline,
40 source-checked question/evidence cases, and an evaluation command.
Independent human annotation review is a separate pending gate.
Use 20 numeric/reference, 8 boundary/definition, 8 unsupported and 4 adversarial
cases. Keep development/tuning cases separate from final evaluation questions.
The local implementation now contains these 40 cases and an evaluation command;
the questions are assistant-authored/source-checked, not independently human-reviewed.

Gate: chunks resolve to the correct pinned documents and pages; no fabricated
page mappings; repeated indexing yields stable content IDs; changed source bytes
are rejected. Include missing-page, malformed-table and source-version cases.
Run existing core tests after meaningful implementation changes.

### Milestone 2 — Semantic retrieval and RAG

Add a small local pretrained embedding model, pin its model revision and compare
lexical versus embedding retrieval. Consider reranking only if measured results
justify it. Add a provider-neutral generation interface after retrieval works.
Benchmark the chosen local generator before making laptop-performance claims;
any paid API route is a separate explicit cost decision.

Proposed acceptance targets: Recall@5 at least 90% on answerable held-out cases;
all returned citation IDs resolve to indexed evidence; all supported numerical
answers agree with the authoritative facts; at least 95% of generated factual
claims supported in manual review. Record actual results and failures, without
relabeling these targets as achieved. Measure latency and memory rather than
inventing service-level promises. Report abstention performance separately;
answering nothing cannot satisfy usefulness criteria.

### Milestone 3 — Tool-using investigation

Add model-selected read tools, run traces and bounded execution. Evaluate correct
tool routing, malformed arguments, unsupported scopes, repeated calls, timeouts,
prompt injection and faithful final answers. A fixed fallback can provide metric
answers when generation is unavailable, labelled accordingly. Proposed tool-call
cap: 6 per question; tune after measuring actual tasks.

Gate: representative traces show useful multi-step tool selection; numerical and
citation checks still pass; unsupported requests stop with an explanation. A
reviewer must be able to inspect the trace and reproduce the source facts.

### Milestone 4 — Demonstration interface

Provide a local page with question input, answer, citations, retrieved passages,
calculation details and tool trace. Show scope/year filters and evidence/model
versions. Keep Power BI for the existing quantitative report. Record a demo and
publish only actual evaluation results. Choose the UI framework after the answer
contracts work; it is not the first engineering milestone.

### Later — Custom ML with enough suitable data

Select one task before collecting data: document-section classification with
reviewed labels, or a forecasting experiment with substantially longer compatible
history. Keep added sources reviewed and disjoint from synthetic test fixtures.
Use held-out documents for text generalization and chronological splits for
forecasting; compare with lexical/majority or naive historical baselines as
appropriate. Check leakage across report revisions and repeated comparative
years. Publish sample counts, splits, uncertainty and failure analysis. A feature
store or model deployment platform is justified only by a demonstrated need.

## Cost and reproducibility

Start with local retrieval and read-only SQLite facts. No hosted vector database
or new cloud billing is required to define/build the baseline. Model download,
license, CPU/RAM behavior and optional runtime must be checked before selecting
specific artifacts. Model files, indexes and raw PDFs stay outside Git. Keep
versioned manifests, prompts, evaluated questions where rights permit, expected
source IDs/pages, code and curated evaluation summaries in Git.

## Learning and file responsibilities

Use [AI_CONCEPTS.md](AI_CONCEPTS.md) for technical/ELI5 explanations and
[AI_LEARNING_LOG.md](AI_LEARNING_LOG.md) for learner output, questions and fixes.
The build order names existing reference paths and future target paths; planned
modules/configuration/model files are created by the learner at their lesson,
not generated pre-emptively by this documentation update. Reuse the existing
Windows `.venv` for readiness and lexical work; choose exact additional model
dependencies only after compatibility, rights and local-resource review.

## Technical references

- Sentence Transformers, retrieve and rerank:
  https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html
- LangGraph, workflows and agents:
  https://docs.langchain.com/oss/python/langgraph/workflows-agents
- LangGraph, pause/resume and review controls:
  https://docs.langchain.com/oss/python/langgraph/interrupts
- scikit-learn, evaluation and chronological/group splits:
  https://scikit-learn.org/stable/modules/cross_validation.html

Frameworks are possible implementation choices, not dependencies installed by
this planning document. Model/provider selection, generated-answer evaluation and deployment
remain unverified. Milestone 1 is implemented in an isolated local development branch. Next actions:
independent reference review and Windows verification, then semantic retrieval
compared with the recorded lexical baseline. Keep the completed first-version
report reproducible.
