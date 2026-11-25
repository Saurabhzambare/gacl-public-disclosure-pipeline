# Documentation guide

Updated: 25 November 2026 (India). This project has a verified data-engineering
foundation and a planned, guided AI extension. Documentation is not evidence
that a planned feature has been implemented.

## Start here

| Read | Purpose |
|---|---|
| [Current status](STATUS.md) | Authoritative summary of verified work, environment and outstanding checks |
| [Phase 2 build order](PHASE_2_BUILD_ORDER.md) | Versioned sequence of 30 learner-implemented steps; start at Step 1 |
| [Step 1 lesson](PHASE_2_STEP_01.md) | Readiness check; Windows execution passed on 25 November |
| [Step 2 lesson](PHASE_2_STEP_02.md) | Baseline execution passed on Windows, 25 November |
| [Step 3 lesson](PHASE_2_STEP_03.md) | Verified PDF inspector and local commit checkpoint |
| [Step 4 lesson](PHASE_2_STEP_04.md) | Structured page evidence, then all-page extraction and tests |
| [AI scope](AI_EXTENSION_PLAN.md) | Product objective, architecture, boundaries and milestones |
| [Learning log](AI_LEARNING_LOG.md) | Current lesson, learner evidence, errors, decisions and next step |
| [Concept guide](AI_CONCEPTS.md) | Technical explanations with ELI5 examples |
| [Evidence and tool contracts](AI_CONTRACTS.md) | Current evidence fields and proposed numerical/answer/tool behavior |
| [AI evaluation plan](AI_EVALUATION_PLAN.md) | How retrieval, answers, calculations and agents will be evaluated separately |

## Existing system and reference implementation

| Guide | Purpose |
|---|---|
| [Setup](SETUP.md) | Existing environments, dependencies and Phase 2 readiness |
| [Architecture](ARCHITECTURE.md) | Implemented pipeline and planned two-route answer architecture |
| [Sources](SOURCES.md) | Approved reports, hashes, page mappings, extraction limitations and rights |
| [Data dictionary](DATA_DICTIONARY.md) | Authoritative facts, units and grain; AI evidence distinctions |
| [Retrieval reference](RETRIEVAL.md) | Existing local prototype commands; availability caveat applies |
| [Retrieval pilot results](RETRIEVAL_EVALUATION.md) | Dated results and limitations of the local prototype |
| [Testing](TESTING.md) | Software tests versus source checks and AI evaluation |
| [Runbook](RUNBOOK.md) | Reruns, recovery, index freshness and planned AI failure handling |
| [BigQuery/dbt](BIGQUERY_DBT.md) | Optional reporting route; not needed for local AI retrieval |
| [HTTPS troubleshooting](HTTPS_TROUBLESHOOTING.md) | Native TLS verification and explicit reviewed-extract fallback |
| [Design decisions](DECISIONS.md) | Reasons for scope, precision, local-first operation and guided delivery |
| [Walkthrough](WALKTHROUGH.md) | Phase 1 recording script and conditional Phase 2 demonstration |
| [Security](../SECURITY.md) | Public-source handling and AI/tool boundaries |
| [Contributing](../CONTRIBUTING.md) | Learner/assistant responsibilities and review workflow |

## Historical records

[The Phase 1 plan](PROJECT_PLAN.md) preserves the original November target and
dated checkpoints. Its old task lists are not the current progress tracker.
[The 24 November verification](VERIFICATION_2026-11-24.md) is a historical
execution record; it must not be edited to imply AI verification. The
[changelog](../CHANGELOG.md) likewise records what was true at each milestone.
The [dashboard guide](../dashboard/README.md) describes the actual two-page
report, not the future question-answering interface.

If guides appear inconsistent, use STATUS.md for evidence, the versioned build
order for step IDs, and the linked detailed contract for field meaning. Correct
inconsistencies rather than silently changing history or renumbering steps.
