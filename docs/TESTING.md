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

Monthly and annual tables are small enough for every selected value to be manually reconciled to the source. See examples/README and STATUS.md for actual evidence.

## Failure behavior

An invalid contract or failed aggregate check fails the run before observation loading. Quarantine/check artifacts explain the problem. Download/parse failures are recorded in run history. A valid retry is safe.

Current limitation: raw parsing errors stop before a row can be constructed, so they appear as failed-run errors rather than fabricated quarantine rows.

