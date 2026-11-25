# Phase 2 — Evaluation and acceptance plan

Version: 1.0. Prepared: 25 November 2026.
Status: page-retrieval pilot implemented locally; semantic, answer, numerical
tool and agent evaluations remain planned. This document defines future checks,
not achieved scores. See [measured pilot](RETRIEVAL_EVALUATION.md) and
[build order](PHASE_2_BUILD_ORDER.md).

## Keep unlike evidence separate

| Evidence type | What it establishes | What it does not establish |
|---|---|---|
| Python unit tests | Specified software behavior under controlled fixtures | Real-model answer quality or live cloud permissions |
| Real source reconciliation | Selected parsed facts match reviewed sources | Universal PDF parsing or regulatory compliance |
| Retrieval evaluation | Expected evidence appears at measured ranks | Complete answer context or faithful generation |
| Numerical-tool evaluation | Correct identified values, units and arithmetic | Source claims are independently true |
| Answer review | Claims follow evidence, with meaningful citations and abstention | Performance beyond the evaluated questions/corpus |
| Agent evaluation | Permitted tool choice, limits, outcomes and final-answer quality | Unrestricted autonomy or production readiness |
| Runtime benchmark | Observed time/memory/cost under declared conditions | An invented service-level guarantee |

Do not add 18 observations, 60 software tests, seven dbt tests and eight manual
SQL checks into one score or test count. Report each denominator and environment.

## Existing pilot and its limitations

The 40 assistant-authored/source-checked cases contain 20 numeric/reference,
eight definition/boundary, eight unsupported and four adversarial questions.
Twenty-four are development and sixteen are a holdout partition. Both use the
same two documents. Independent human review is pending; expected pages are not
independent documents or evidence of generalization to all topics in the reports.

Only 28 answerable cases are scored today. Their expected page appeared in the
first five results for 26 cases (92.86% combined); MRR@5 was approximately
0.797619. Every scored case has one expected page, so page recall and page-hit
rate coincide. The two misses and split-level figures remain in the dated pilot
record. This is not generated-answer accuracy. The 12 negative/adversarial cases
are search diagnostics; no refusal or prompt-injection score exists.

The already-observed holdout cannot repeatedly guide improvements while still
being advertised as unseen. Preserve it as a historical benchmark and add a
new, independently reviewed reserved set for stronger final claims. Correct
case errors transparently with a new version; do not silently edit expectations
to fit retrieved results.

## Case construction and review

Each case needs a stable ID, category, question, approved source versions,
expected source/page evidence, scope/period/unit where relevant, answerability,
expected value/calculation if applicable and a review record. The reference
reviewer verifies original PDF context, not just extracted anchors. Separate
reviewed notes from raw source extraction. Avoid near-duplicate paraphrases
leaking between development and final partitions.

Use supported fact lookups, compatible comparisons, reporting definitions,
ambiguous scope/period, missing facts, unknown source versions, inappropriate
aggregation, unsupported causes and malicious requests. Do not invent GACL
measurements. Synthetic corrupted files/rows belong only to isolated tests.

## Retrieval protocol

Compare lexical and semantic methods using identical approved source versions,
reference definitions, filters and top-k page semantics. Do not inject expected
pages/source filters unless the user's actual question supplied those filters.
Record chunk parameters, query policy, index/model versions and page deduplication.

- Page Recall@k: retrieved relevant reference pages divided by expected relevant
  pages, averaged over answerable cases.
- MRR@k: mean reciprocal position of the first relevant page, with zero for a
  miss outside k.
- Inspect whether the returned chunk actually contains useful year/unit/table
  context. A page hit alone is insufficient for answering.
- Record per-case errors and measured query time, including cold/warm conditions.

Optional hybrid/reranking work must respond to development errors and be
evaluated as an additional method. A lower BM25 score or higher cosine similarity
is not a calibrated probability of a correct answer.

## Numerical tools and generated answers

For every supported numerical case, compare the selected observation IDs,
versions, scope, periods, unit/statistic, exact decimal value and source pages.
Comparison cases additionally check operand order, formula, exact difference,
percentage and declared display rounding. Zero baseline, missing data,
incompatible units/grains and unresolved revisions must not yield invented values.

Review generated outputs at two levels: question usefulness/correctness and
individual factual claims. Citation checks distinguish resolvable evidence IDs
from pages that actually support the associated claim. An answer cannot earn
credit merely by attaching a real but irrelevant source link.

Report separately:

1. Supported-question answer correctness and coverage, including whether a useful
   answer was produced. Refusing every question is not success.
2. Supported factual claims divided by all factual claims assessed, with reviewer
   rubric and ambiguous cases disclosed.
3. Numerical correctness across all supported numerical cases, not only selected
   successful examples.
4. Citation resolution and claim-support results with their own denominators.
5. Appropriate insufficient-evidence responses on unsupported cases and false
   abstention on answerable cases.
6. Appropriate clarification on intentionally ambiguous questions.
7. Model/provider failures and excluded/unscorable cases, reported visibly.

## Agent and adversarial evaluation

Inspect model-selected call traces, validated arguments, tool results, evidence
IDs and final answers. Test unknown/disallowed tools, SQL-write requests,
credential requests, document text posing as instructions, repeated calls,
malformed arguments, source/scope mismatch, stale index, timeouts and exhaustion
of the proposed six-call budget. Enforce limits in the application, not solely
the prompt. Test provider-call/time limits even when the model requests no tool.

Replay deterministic tools against the recorded source/index versions. Record
final stop reason and whether the response remains faithful. Do not request
hidden model reasoning or describe passing a few cases as a security guarantee.

## Proposed release gates — not yet achieved

| Layer | Proposed criterion | Evidence required |
|---|---|---|
| Retrieval | At least 90% page Recall@5 on the newly reviewed answerable evaluation set | Set size/version, relevance rules, per-case ranks and misses |
| Numerical tools | Every supported numerical answer agrees with validated facts and formulas | Exact comparisons, units, scope and source lineage |
| Citations | All returned citation IDs resolve; each factual citation is reviewed for support | Resolvability and claim-support results reported separately |
| Generated faithfulness | At least 95% of assessed factual claims supported by evidence | Explicit claim rubric, reviewer and denominator; errors retained |
| Answerability | Report abstention, false abstention and useful-answer coverage separately | All supported, unsupported and ambiguous cases, with counts |
| Agent limits | No disallowed action executes in the defined tests; bounded termination demonstrated | Trace outcomes, budgets and failure cases |
| Regression | Existing meaningful tests and real 18-record reconciliation pass | Actual Windows output, versions and identified artifacts |

Small evaluation sets limit precision. Do not imply these targets are achieved
because the historical lexical pilot exceeded 90%. If a target fails, keep the
stage open, investigate on development cases and document limitations honestly.

## Runtime, cost and reporting

Measure model loading separately from warm-query time; record device, Python,
runtime, model revision, index/case version, observed memory and actual timed
operations. No speed-up percentage without a comparable baseline. If an API is
explicitly chosen, record its actual request usage/cost basis without credentials;
no provider or billing is enabled by this plan.

Save raw local evaluation outputs under ignored artifact storage. Commit only
curated summaries and rights-appropriate case definitions after review; public
publication is a separate action. See [security](../SECURITY.md) and
[learning log](AI_LEARNING_LOG.md). A future predictive ML experiment would need
its own target, suitable dataset, chronological/group split and baseline; these
retrieval/answer tests cannot establish forecasting performance.
