# Design decisions

1. **Public disclosures only.** No authorization or access to internal GACL systems is assumed.
2. **Core first.** Two reports and 18 observations defined the original 22 November
   target; that historical estimate is not the Phase 2 deadline.
3. **Separate grains.** Monthly site KL/day rates and annual standalone company GJ/KL totals never share an aggregation.
4. **Exact values.** Decimal strings preserve disclosed precision; presentation rounding is separate.
5. **Pinned documents.** SHA-256 verification makes layout-specific extraction reproducible and flags revisions.
6. **Local first.** SQLite and CSV give a working demonstration before cloud authentication is configured.
7. **Targeted extraction.** Explicit labels, page references, expected row counts and year-column checks are easier to review than a general PDF parser.
8. **No invented scale.** Small data demonstrates correctness; there is no throughput, cost-saving or operational impact claim.
9. **No premature forecasting.** Six monthly averages are insufficient evidence for predictive maintenance.
10. **Public portfolio.** The user made the repository public after initial setup. Source attribution and current feature status remain explicit.
11. **Source licensing stays separate.** MIT applies only to original project code.

12. **Billing-free cloud route.** On 20 November the user chose the BigQuery sandbox. An explicit --mode snapshot uses a full validated batch replacement; --mode merge remains an optional DML path. The snapshot is not described as an incremental upsert or independent historical archive.

## Phase 2 decisions — 25 November 2026

13. **Learner implements.** Saurabh writes code/configuration/tests; the assistant
    maintains documentation, explains and reviews one step at a time. The
    [30-step build order](PHASE_2_BUILD_ORDER.md) version 1.0 has stable IDs;
    current learner progress is recorded in AI_LEARNING_LOG.md. Prototype
    results are separate evidence.
14. **Two evidence routes.** Search cited pages for text; read validated facts
    and calculate with Decimal for numbers. A model explains but cannot become
    the authoritative source of operands, scope or arithmetic.
15. **Baseline before ML.** Preserve lexical pilot results and compare pretrained
    semantic retrieval using explicit evaluation versions. Embedding inference
    is an ML application, not training a custom model on 18 observations.
16. **Minimal local infrastructure.** Exact vector comparison is sufficient for
    the small corpus; hosted vector databases, new cloud billing and large
    frameworks are not prerequisites. Select/pin each model/runtime only after
    license, compatibility and real resource review.
17. **Workflow before agent.** Verify cited answers first; call behavior agentic
    only after dynamic model-selected tools execute within enforced limits.
18. **Separate scores.** Software tests, page relevance, numerical correctness,
    claim/citation support, abstention and tool security need separate evidence.
    New independently reviewed reserved cases are needed for stronger claims
    after the original holdout has been inspected.
19. **Keep scope honest.** No OCR, live plant access, custom forecasting,
    production savings, compliance certification or public deployment is implied.
    A future trained model requires a suitable separately reviewed dataset.
20. **No silent costs or publication.** Provider calls that incur costs, public
    release and outreach are distinct decisions; documentation authorizes none
    of them. No completion deadline is invented for Phase 2.

Model/provider/UI selections remain open at their numbered lessons. Record
future decisions here with evidence; do not turn placeholders into installed
dependencies. Detailed boundaries: [contracts](AI_CONTRACTS.md).
