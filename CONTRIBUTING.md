# Contributing

1. Create a feature branch.
2. Keep the selected metrics, source attribution and reporting boundaries intact.
3. Make a focused change; add tests for changed extraction or validation behavior.
4. Run the unit suite and a real pipeline extraction when source parsing changes.
5. Inspect git diff and ensure secrets/generated PDFs are not staged.
6. Update STATUS.md and relevant setup/data documentation.
7. Open a pull request describing the problem, resulting behavior and checks performed.

No credentials are required for the unit suite. Do not commit synthetic values into the real-data examples. If a source changes, document old/new hashes and why the parser still interprets it correctly.

## Guided Phase 2 workflow

Saurabh personally implements code, tests, configuration and dependency changes.
The assistant maintains documentation and supplies one current lesson at a time:
purpose, ELI5, architecture context, installation requirements, exact paths and
insertion points, commented code, run/check commands and an understanding check.
Do not independently implement future lessons or overwrite existing prototype
modules. Classes and frameworks need a concrete purpose, not keyword coverage.

Follow [Master Build Order](docs/PHASE_2_BUILD_ORDER.md) version 1.0, Steps 1–30.
Record learner output in [the learning log](docs/AI_LEARNING_LOG.md) and verified
capability separately in [status](docs/STATUS.md). Explain changes to the sequence
before adopting them; preserve established IDs. A reference implementation is not
evidence the learner wrote or ran that step.

At code checkpoints, run relevant meaningful tests and the required regression
suite; parsing changes require real source reconciliation. Future model smoke
tests are separate from mocked unit tests. Keep curated evaluation cases/results
versioned with model, index and prompt provenance. Documentation-only changes
need link, scope/status and whitespace checks, not invented new runtime results.

Review staged files and their rights before any local commit. The author may
create a draft PR or publish when explicitly requested; this workflow does not
automatically push, merge, deploy or send messages. Generated source PDFs, models,
indexes, secrets and unreviewed logs are not repository deliverables. The reviewed
dashboard PDF/previews are intentional existing exceptions.

