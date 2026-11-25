# Phase 2 — Evidence, numerical and assistant contracts

Version: 1.0. Prepared: 25 November 2026.
Status: current retrieval fields below describe the local reference prototype;
semantic, numerical-tool, generation and agent contracts are design requirements,
not implemented interfaces. See [build order](PHASE_2_BUILD_ORDER.md) and
[current evidence](STATUS.md).

## Non-negotiable boundaries

Use only approved document versions. Preserve exact extracted text separately
from reviewed annotations. Unknown printed pages remain unknown. Monthly
`dahej_plot3_report` daily-average KL/day rates and annual `gacl_standalone`
GJ/KL totals remain distinct. No source expansion, implicit preferred revision,
synthetic GACL measurement, live reading, compliance certification or unsupported
causal explanation is introduced by these contracts.

## Guided implementation versus the reference prototype

The learner is beginning Step 4A after verified local merge a5001c0. Its proposed
extract_page(root, source_id, pdf_page) returns one page dictionary with PDF/text
hashes, explicit page/scope metadata, extraction/library versions and a citation
URL. It has no chunks, index, reviewed-note configuration or search API yet.
Those return layouts below describe the earlier local prototype, not automatic
availability in the learner's checkout. [Step 4](PHASE_2_STEP_04.md) introduces
all-page metadata and focused tests in 4B before the full gate closes.

## Current page and chunk evidence

| Field / concept | Meaning and rule |
|---|---|
| `source_id` | Approved identifier in `config/sources.json` |
| `document_sha256` | Hash of verified source bytes; a version identifier, not proof of truth |
| `source_url` | Approved official PDF URL |
| `pdf_page` | One-based physical PDF page |
| `printed_page` | Explicit reviewed mapping where known; otherwise null |
| `reporting_scope` | Established document reporting boundary; not inferred sentence-level classification |
| `text` | Exact embedded text or exact span of it, depending on page/chunk result |
| `text_sha256` | Hash of stored extracted text |
| `reviewed_note` | Separately labelled version-pinned visual-review metadata; never passed off as extracted text |
| `section` | Currently null; no inferred heading/section detection |
| `chunk_id` | Stable digest incorporating source/version, extraction/chunk version, page, offsets, content and relevant metadata |
| Start/end offsets | Positions into canonical extracted page text; round-trip equality required |
| `citation_url` | Official source URL with `#page=<physical page>`; viewer support and live URL availability are separate concerns |
| Rank/score | Retrieval order and backend-specific ranking value, not a probability |

Inspect `retrieval.py` and [the retrieval guide](RETRIEVAL.md) for actual current
JSON layouts. This table is semantic documentation, not a promise that every
endpoint emits every field at the top level. Source hashes, indexes and query
versions must agree. Hash checks detect accidental mismatch; they do not make
an editable database a signed or tamper-proof security boundary.

Current `search_documents` returns `mode=lexical_retrieval`, `answer=null` and
`answerability=not_assessed`. A keyword hit is a candidate, not an answer.
Search results are deduplicated by source/page before the top-k cutoff. Full-page
retrieval is distinct from a chunk's potentially incomplete table context.

## Planned semantic-index contract

Map every vector to an existing canonical chunk ID. Record approved source
hashes, extraction/chunk/configuration fingerprints, actual model identifier,
immutable revision where supported, runtime/dependency versions, vector dimension,
numeric representation, preprocessing/query prefixes, normalization, similarity
method and build time. The current model/index choice is unset.

Reject stale, missing, non-finite or wrong-dimension vectors. Never compare
vectors from incompatible models or silently re-download an unpinned revision.
Generated files belong under ignored local artifact storage. A successful index
build changes neither observation values nor original source hashes.

## Planned read-tool interfaces

These signatures are conceptual contracts. Final Python types and wire schemas
are introduced in the numbered lessons after inspecting actual storage.

| Tool | Inputs | Required outcome |
|---|---|---|
| `search_documents` | Question, optional approved source/scope filters, top-k | Versioned cited candidate passages; lexical implementation already exists |
| `get_source_page` | Source ID, expected document hash, physical PDF page | Verified canonical page and separate reviewed note; current `get_page` is the reference reader, not this exact future signature |
| `get_metric` | Metric ID, reporting scope, exact period; explicit version if ambiguous | One validated observation with exact value, raw value, statistic, unit and provenance |
| `compare_metric` | Same metric/scope, earlier and later periods; explicit version policy | Both identified inputs, formula, exact change and declared display rounding |
| `get_check_results` | Actual run ID | Recorded check results with evidence location/time; unknown run is explicit |

All tools validate arguments before work. SQLite reads are read-only,
parameterized and do not create a missing database. No arbitrary SQL is accepted
from a question or model. Missing or conflicting versions require clarification,
not automatic selection. Tool naming alone does not enforce permissions.

## Planned numerical comparison

Return later minus earlier using Decimal. Compute percentage change as
`(later - earlier) / earlier * 100` only when the baseline is nonzero and the
records have compatible definitions. A zero baseline yields an explicit
undefined percentage, not infinity or a fabricated zero.

Return input observation IDs/document versions, periods, scope, unit/statistic,
raw and exact values, formula, exact result and separately rounded display text.
Never sum monthly KL/day rates into annual KL or label a rate difference as
physical water saved. Annual total energy cannot be added to its components
again. Unsupported aggregation/unit conversion must fail visibly.

Reference example: April 12,540.8 and September 11,738.1 KL/day give a change
of -802.7 KL/day and approximately -6.40%. The source is the monthly report,
PDF page 5 / printed page 4. These are example facts, not generated output.

## Planned answer result

Use distinguishable result states such as answered, insufficient evidence,
clarification required and execution error. Freeze their exact enum/JSON schema
in Step 20 rather than claiming it exists today. Each final answer should expose:

- The question and relevant explicit scope/period; clarification when ambiguous.
- Answer text whose factual claims map to returned evidence IDs.
- Source/version/page citations, passages and labelled reviewed metadata.
- Authoritative tool inputs/results for any numerical claim or calculation.
- Actual model/provider, prompt/index versions and run identifier.
- Limitations or unavailable evidence; errors must not become invented answers.
- Measured timing and tool outcomes where available, without credentials or
  hidden model reasoning.

An existing fact lookup may work when generation is unavailable, but the output
must be clearly labelled a deterministic result; do not claim the model ran.
Evidence IDs must resolve within the current request's verified evidence.
Citation existence and citation support are distinct checks.

## Planned generation boundary

A provider adapter receives bounded question/evidence/instructions and produces
validated output. Model output cannot override authoritative values or perform
the final arithmetic. Version prompts and declared runtime settings. Lower
sampling variability is not a factuality guarantee. Retrieved document text is
untrusted content, never higher-priority operating instructions.

Keep provider failures, timeouts, context overflow and invalid outputs distinct.
No silent switch to another paid service, model or document version. An external
provider requires an explicit cost/data-flow decision before requests. A local
model requires measured laptop feasibility and reviewed license/revision.

## Planned agent boundary and trace

The model may dynamically select only registered read tools. The application
validates and dispatches tool calls; it does not execute model-written Python,
shell, SQL writes, manifest changes, external messages or plant commands.
Starting proposal: at most six tool calls per question, with finite provider,
timeout, token and output limits finalized during implementation.

Record observable call name, validated arguments, evidence IDs, start/end/outcome,
errors and stop reason. Do not request or publish hidden chain-of-thought.
Replay means deterministic tool results can be checked against identified
inputs/versions; it does not promise identical stochastic language output.

## Storage and publication

Original facts remain in the existing observation warehouse. Text indexes,
vectors, downloaded models, raw prompts/responses and execution traces stay out
of Git unless a specific curated artifact has been reviewed. Publish code,
configuration without secrets, case definitions within source rights, model
choices and honest aggregate evidence only after separate authorization.

Contract changes require an explained design decision and updated tests/docs;
they must not silently invalidate stored indexes or existing retrieval commands.
