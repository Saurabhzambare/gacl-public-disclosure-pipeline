# Contributing

1. Create a feature branch.
2. Keep the selected metrics, source attribution and reporting boundaries intact.
3. Make a focused change; add tests for changed extraction or validation behavior.
4. Run the unit suite and a real pipeline extraction when source parsing changes.
5. Inspect git diff and ensure secrets/generated PDFs are not staged.
6. Update STATUS.md and relevant setup/data documentation.
7. Open a pull request describing the problem, resulting behavior and checks performed.

No credentials are required for the unit suite. Do not commit synthetic values into the real-data examples. If a source changes, document old/new hashes and why the parser still interprets it correctly.

