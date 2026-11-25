# Retrieval reference cases

Documentation-publication note, 25 November: the JSON files described below
remain in the unpublished local prototype. This documentation-only update adds
this guide, not the cases, baseline JSON or evaluator implementation. Use the
linked dated pilot report for the curated human-readable results.

retrieval_cases.json contains 40 assistant-authored, source-checked reference
cases for the two pinned public documents. Numeric targets come from the
already reviewed CSV facts. Page references, extracted anchors and two clearly
separated visual-review annotations are validated by the evaluator. They are
not synthetic GACL observations or a labelled forecasting dataset.

| Category | Development | Holdout | Total | Scored now |
|---|---:|---:|---:|---|
| Numeric/reference | 12 | 8 | 20 | Reference-page retrieval |
| Boundary/definition | 4 | 4 | 8 | Reference-page retrieval |
| Unsupported | 6 | 2 | 8 | Diagnostic only |
| Adversarial | 2 | 2 | 4 | Diagnostic only |

The partition is explicit, but both splits cover the same two documents and were
authored by the same assistant. No independent human review or external blind
validation is claimed. Query/chunk parameters were not tuned to repair the
observed holdout miss. New retrieval experiments must record which questions
were used for development and reserve a new independent set for stronger claims.

expected_answer is reference documentation, not a generated answer and not a
quantity scored by the current evaluator. Answer accuracy, abstention and
agent-security evaluation remain unimplemented. References target pages,
not a guarantee that every retrieved chunk includes all relevant evidence.

baseline_results.json is a curated snapshot of observed aggregate metrics and
missed-case page IDs. It contains no raw source passages, credentials or raw
execution logs. Full per-case diagnostic outputs remain under ignored
 data/retrieval/. See docs/RETRIEVAL.md and docs/RETRIEVAL_EVALUATION.md.

## Phase 2 learning and later evaluation

This pilot is reference material. Learner Step 1 is pending; personal case review
and Windows baseline execution are Steps 9–10 in the
[Master Build Order](../docs/PHASE_2_BUILD_ORDER.md). Do not mark those lessons
complete because this file exists. Preserve the dated historical results.

The [AI evaluation plan](../docs/AI_EVALUATION_PLAN.md) defines a newly reviewed
reserved set and separate semantic-retrieval, numerical, generated-answer,
citation, abstention and agent evaluations. Those sets/tools are planned, not
created here. Do not repeatedly tune against the observed pilot holdout and
still call it unseen. No final-answer or security pass rate follows from the
current 26/28 page-retrieval result.
