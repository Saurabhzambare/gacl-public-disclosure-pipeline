# Initial lexical retrieval evaluation — 24 November 2026

Context added 25 November: this remains a dated reference-prototype evaluation,
not learner Windows evidence or a new evaluation run. [Phase 2 build order](PHASE_2_BUILD_ORDER.md)
Steps 9–10 cover personal review and a Windows baseline; Step 15 compares semantic
retrieval. Later answer/agent criteria are in [the evaluation plan](AI_EVALUATION_PLAN.md).
The original measurements below are preserved; learner Step 1 is still pending.

Implemented and tested on the local feature/document-retrieval branch. Runtime:
Python 3.12.14, PyMuPDF 1.26.6 and SQLite 3.53.1. No model/API/cloud calls were
used. This records a pilot page-relevance benchmark, not AI answer accuracy.

## Coverage and metrics

Two checksum-pinned real PDFs have 71 physical pages. The index contains 70
text pages and 136 exact-text chunks; the image-only monthly cover is skipped.
BRSR pages 1 and 37 have short, explicitly reviewed annotations, separately
labelled from extracted text. All expected evidence anchors and mapped printed
pages in the reference set resolve against the approved index.

| Split | Cases | Answerable/scored | Diagnostic only | Page Recall@5 | MRR@5 |
|---|---:|---:|---:|---:|---:|
| Development | 24 | 16 | 8 | 15/16 = 93.75% | 0.812500 |
| Holdout partition | 16 | 12 | 4 | 11/12 = 91.67% | 0.777778 |
| Combined | 40 | 28 | 12 | 26/28 = 92.86% | 0.797619 |

Each answerable case has one expected source/page, so page hit rate and page
recall coincide here. MRR@5 is the mean reciprocal rank of the first relevant
page in the first five results; a miss contributes zero. Results are deduplicated
by source/page before the cutoff. All cases use the same natural-language query
policy; there are no expected-page filters injected into search.

The 40 questions are assistant-authored and source-checked; independent human
review remains pending. The holdout is a partition of the same two-document
corpus, not an external blind evaluation. The benchmark concentrates on the
reviewed water/energy facts and a few reporting definitions; it does not establish
retrieval performance over every topic across the reports. The initial ranking
policy was retained after observing the heldout results. Future changes should
use new independent cases for stronger claims.

A reference-page hit does not establish that the returned chunk contains the
complete table or answer. Full page context, year/unit interpretation and a
validated fact lookup are necessary before answering numerical questions.

## Observed misses

- fact-16: total annual water discharged in FY 2025–2026. The expected BRSR
  PDF page 38 was outside the first five returned pages.
- definition-02: the financial year covered by the BRSR. The expected PDF
  page 1 was outside the first five returned pages.

The exact ranked page IDs are retained in
the local prototype's `evaluation/baseline_results.json`. That JSON and the
prototype implementation are not included in this documentation-only publication.
These are baseline limitations for the later semantic-retrieval comparison.

## What was not measured

The 8 unsupported and 4 adversarial cases ran as retrieval diagnostics. They
were excluded from recall denominators. No answers, refusals or agent actions
were generated; answer accuracy and abstention accuracy are null. SQL-like
query text is treated as quoted retrieval terms, not executed as SQL. This does
not constitute an evaluation of an LLM's resistance to prompt injection.

There is no trained forecasting model, embeddings benchmark, RAG answer model,
agent or hosted search interface in this milestone.

## Regression and reliability checks

- All 60 Python tests passed locally: 32 existing and 28 retrieval tests.
- Synthetic PDF fixtures test page/citation integrity, unknown printed pages,
  missing/changed sources, blank required pages, stable chunk IDs, atomic
  replacement failure/retry, read isolation, query injection handling, filters,
  stale configuration and evaluation-version/evidence checks.
- A real cached-PDF extraction succeeded: local run
  0aec3b53-d3a7-42fe-a419-b7af1fe7f6ed, 18 extracted/loaded/stored and all
  four existing dataset checks passed. All 18 complete re-extracted records
  equal the reviewed CSV snapshots, including provenance fields.
- Existing cloud/report verification remains recorded separately in
  [the completed first-version run](VERIFICATION_2026-11-24.md).
- This feature's Windows execution/CI and independent reference review remain
  pending. Public GitHub publication is not claimed by this local test record.

Commands and implementation boundaries: [retrieval guide](RETRIEVAL.md).
