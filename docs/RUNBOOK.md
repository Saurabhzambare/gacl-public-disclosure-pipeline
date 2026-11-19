# Operations runbook

## Normal run

From the repository root, run python -m gacl_pipeline using the project virtual environment. The default run downloads missing PDFs and verifies cached files. Exit code 0 means success; 1 means failure.

Read logs/latest_run.json first. Detailed logs and check/quarantine files use the run_id.

## Offline rerun

Use --offline after a successful download. Every cached PDF must match its configured checksum.

## Historical reload

Use --source gacl_dahej_plot3_ec_2025_h1 or --source gacl_brsr_2025_26. This reloads that complete source period. It does not delete observations from other sources.

## Refresh

Use --refresh to fetch the supported reports again. Checksums remain pinned. A source change is a review event, not an instruction to replace the expected hash automatically.

## Common problems

| Symptom | Action |
|---|---|
| Module not found | Use the same virtual-environment interpreter for install and execution; install -e . |
| Offline source missing | Run online once or restore the exact verified PDF. |
| Checksum mismatch | Inspect the local file/source. Do not disable verification. |
| Expected row/column context missing | Inspect the cited page; adjust parser only after confirming the layout and numbers. |
| Monthly coverage or energy check fails | Inspect quarantine and checks; compare raw values with the source. |
| Windows CSV/database locked | Close applications using the generated file, then rerun. |
| Power BI stale data | Refresh only after a successful pipeline run. |
| Cloud credentials missing | Keep working locally; follow BIGQUERY_DBT.md when ready. |

## Recovery and source revision

The observation load is transactional. A later export failure may leave valid warehouse rows committed; rerun to regenerate exports. Downloads use temporary files and verify content before replacement.

Source versions remain separate in SQLite. There is no automatic choice of preferred revision. Before adding a revised source, document selection rules and extend reporting views so multiple revisions cannot be summed accidentally.

Do not publish logs that expose credentials. The current logs contain source identifiers and errors, but should still be reviewed before sharing.


## Reviewed-extract input mode

Use --from-examples when the report website is unavailable. It validates the pinned repository CSV snapshots, runs the normal data checks and loads the warehouse without downloading PDFs. Run history and data/processed/run_manifest.json record input_mode=reviewed_extracts and pdfs_verified_this_run=false. This is distinct from --offline, which verifies cached source PDFs. The 22-test suite includes no-network execution, duplicate-safe reruns, altered-snapshot rejection, Windows newline handling, certificate failure handling and migration of existing run history. See docs/HTTPS_TROUBLESHOOTING.md from the repository root.
