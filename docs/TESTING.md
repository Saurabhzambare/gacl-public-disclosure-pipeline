# Data quality and testing

## Commands

Windows:
```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m gacl_pipeline
.\.venv\Scripts\python.exe -m gacl_pipeline --offline
```

Linux/macOS: replace the interpreter path with .venv/bin/python.

## Unit tests

The suite checks:
- Indian numeric formatting and preservation of decimal precision.
- Missing values versus zero; malformed numbers.
- Valid observation acceptance.
- Rejection of bad units, scopes, page references, periods and negative values.
- Duplicate quarantine.
- Missing monthly coverage.
- Energy rounding tolerance and a real reconciliation mismatch.
- Duplicate-safe local loading and retention of distinct source versions.
- Bounded retries and refusal to overwrite a cached file with changed bytes.
- Recording of a failed offline run.
- Unknown source selection and mutually exclusive CLI options.

Tests use isolated temporary databases and deliberately broken fixtures. They do not modify real GACL reports.

## Integration verification

A real run must produce 18 observations: 6 monthly + 12 annual. Run it twice and compare warehouse counts and normalized rows. Both runs must succeed without adding duplicates.

The download/extraction integration is not part of the default offline CI suite because it depends on an external website. Run it locally or deliberately when updating sources.

## Dataset-level checks

- Six distinct monthly records covering April–September 2025.
- Twelve selected annual records.
- Renewable + non-renewable energy equals total within 0.01 GJ, separately for each financial year.

Monthly and annual tables are small enough for every selected value to be manually
reconciled to the source. See [reviewed examples](../data/examples/README.md) and
[status](STATUS.md) for actual evidence.

## Failure behavior

An invalid contract or failed aggregate check fails the run before observation loading. Quarantine/check artifacts explain the problem. Download/parse failures are recorded in run history. A valid retry is safe.

Current limitation: raw parsing errors stop before a row can be constructed, so they appear as failed-run errors rather than fabricated quarantine rows.


## Reviewed-extract input mode

Use --from-examples when the report website is unavailable. It validates the pinned repository CSV snapshots, runs the normal data checks and loads the warehouse without downloading PDFs. Run history and data/processed/run_manifest.json record input_mode=reviewed_extracts and pdfs_verified_this_run=false. This is distinct from --offline, which verifies cached source PDFs. The core test suite includes no-network execution, duplicate-safe reruns, altered-snapshot rejection, Windows newline handling, certificate failure handling and migration of existing run history. See docs/HTTPS_TROUBLESHOOTING.md from the repository root.

## Native HTTPS verification

Windows selects a truststore client SSLContext and passes it explicitly to
urlopen. Other platforms retain required certificate and hostname checks.
Tests verify context selection/forwarding, document hashing and immediate
certificate-error failure. CI covers Windows/Python 3.11 and Linux/Python 3.12
without depending on the external report website. Native Windows download
success was reported with the temporary launcher and then confirmed with the
integrated normal --refresh command on 20 November; see STATUS.md.

## BigQuery snapshot boundary tests

Install the cloud extra to run all 32 tests; core-only installs run 25 and skip
the seven cloud tests. CI installs the pinned BigQuery 3.47.0 SDK on Windows and
Linux. The SDK types are real, but the client is mocked: no credentials or Google
Cloud calls are used. Checks cover explicit mode selection, replacement on rerun
without DML/deletion, empty/partial/malformed/duplicate export rejection before
cloud access, location mismatch, job failure, post-load row-count mismatch and
retention of explicit MERGE staging/cleanup behavior. These tests do not prove
live sandbox permissions or deployment. Those require the user's cloud run.

## Live dbt and final reference check

On 22 November the user supplied a successful Windows dbt build: three views,
seven passing SQL tests, PASS=10 WARN=0 ERROR=0 SKIP=0. These are separate
from the 32 Python software tests.

The manual GoogleSQL script sql/bigquery_verification.sql provides eight
read-only checks: count and bidirectional reference comparison for the raw
table and each dbt view. It embeds the 18 genuine reviewed facts from pinned
CSV snapshots (not synthetic test input). Source date/value/unit/scope facts
were validated before generating the script; its syntax parsed with sqlglot.
On 22 November the user screenshot confirmed all eight passed=true,
with 18/18/6/12 rows and zero differing facts for all four relations. The manual script
does not add eight Python tests or change the seven dbt tests.

## Power BI report evidence

The user confirmed a successful Desktop refresh. On 24 November the supplied
two-page PDF was visually reviewed and checked against the selected reference
facts: six monthly points, rounded annual labels, 6/12/18 observation counts,
source pages and units. All four source-link annotations retain the intended
URLs. These are report review checks, not additional Python or dbt tests.
The subsequent manual sequence from cached PDF extraction through BigQuery/dbt,
reference checks and Desktop refresh completed on 24 November. The author supplied
terminal output, screenshots and refresh confirmation; see
[verification evidence](VERIFICATION_2026-11-24.md). The video remains pending.

## Phase 2 software and AI evaluation

The local retrieval prototype has 28 additional tests; its verified Linux suite
had 60 total with the cloud extra: 25 core + 7 mocked cloud + 28 retrieval.
Cloud-only optional tests can be skipped without that extra; report the actual
executed/skipped counts rather than assuming 60 on every checkout. Feature
Windows verification and learner execution are pending. Previous core Windows CI
does not establish that the new feature passed there.

Retrieval tests cover provenance/offset integrity, explicit mappings, separately
labelled annotations, source changes, stale configuration, atomic replacement,
read-only isolation, safe queries, filters and evaluation-reference consistency.
Synthetic PDFs remain temporary fixtures, not additions to the real corpus.

The existing 40-case pilot measures expected page relevance: 28 answerable cases
are scored; 12 unsupported/adversarial questions are diagnostic only. It does not
measure LLM answer correctness, refusal or prompt-injection resistance. Keep
software tests, page metrics, numeric checks, generated-claim/citation review and
agent tool behavior separate. See [measured pilot](RETRIEVAL_EVALUATION.md) and
the [full AI evaluation protocol](AI_EVALUATION_PLAN.md).

Future semantic tests use controlled model substitutes plus a distinct real-model
smoke test; real inference needs reviewed installations. Numerical tools require
exact Decimal/source/unit tests. Generation needs faithful citations and useful
abstention evaluation, and agents need dynamic-routing/limit tests. These future
tests are not created or claimed as passing by this documentation update.

Follow [build order](PHASE_2_BUILD_ORDER.md). The learner writes and runs relevant
tests at each code step. Documentation-only updates use link/consistency/diff
checks; they are not a new pipeline, cloud, model or Windows verification run.
