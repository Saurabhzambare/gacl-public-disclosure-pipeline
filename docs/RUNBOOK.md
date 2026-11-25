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

Use --from-examples when the report website is unavailable. It validates the
pinned repository CSV snapshots, runs the normal data checks and loads the
warehouse without downloading PDFs. Run history and the processed run manifest
record input_mode=reviewed_extracts and pdfs_verified_this_run=false. This differs
from --offline, which verifies cached source PDFs. Tests cover no-network
execution, duplicate-safe reruns, altered snapshots, Windows newline handling,
certificate failures and run-history migration. Use [status](STATUS.md) for dated
test counts and [HTTPS troubleshooting](HTTPS_TROUBLESHOOTING.md) for recovery.

## Phase 2 — local retrieval operations

Only run prototype commands when those modules exist in the checkout; see
[retrieval commands](RETRIEVAL.md). No public feature branch or learner Windows
run is implied. The current guided step remains Step 1 in the
[build order](PHASE_2_BUILD_ORDER.md).

| Symptom | Handling |
|---|---|
| Missing cached PDF | Obtain the approved verified PDF through the original pipeline; reviewed CSVs cannot supply document pages |
| Missing retrieval index | Build it after source verification; do not create a substitute empty warehouse |
| Changed source/configuration | Inspect versions and rebuild only from approved inputs; do not disable checks or silently update pins |
| Image-only or incomplete text | Record limitations; mapped required evidence must not be silently skipped or reconstructed |
| Locked index on Windows | Close readers/inspection tools and retry; retain the previous good index if replacement fails |
| Related search hit, unclear answer | Inspect full-page year/unit context; search does not assess answerability |

The index lives separately under ignored `data/retrieval/`; it can be regenerated
from approved inputs. Rebuilding must preserve authoritative observations. Build
timestamps do not become new PDF retrieval timestamps. Keep curated evaluation
results separate from raw local diagnostics.

## Planned model and answer recovery

The following policies are requirements for later implementation, not available
commands today: reject model/index dimension or revision mismatch; bound provider
and tool calls; return explicit missing-model, timeout, insufficient-evidence or
clarification states; never silently switch models, paid providers or sources.
Generation failure must not produce an invented result. A deterministic fact
fallback, if implemented, must be labelled as such.

No cloud load or Power BI refresh is needed for each local AI question. Preserve
the original refresh sequence when the reporting facts actually change. Actual
model/runtime operations and UI launch commands will be documented only after
the learner implements and verifies them. See [contracts](AI_CONTRACTS.md) and
[security](../SECURITY.md).
