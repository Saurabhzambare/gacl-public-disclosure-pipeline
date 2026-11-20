# Local development setup

## Requirements

- Python 3.11+; Python 3.12 is the verified development target.
- Git or GitHub Desktop; the repository is public.
- Internet for the first PDF download and package installation.
- Power BI Desktop on Windows for the reporting milestone.
- No BigQuery account is needed for local development.

## Windows with GitHub Desktop

1. Open GitHub Desktop with the Saurabhzambare account.
2. File → Clone repository → URL → enter https://github.com/Saurabhzambare/gacl-public-disclosure-pipeline.
3. Choose a local folder, for example Documents/GitHub.
4. Repository → Open in your editor or open PowerShell in that folder.
5. Run the commands below. They call the virtual environment directly, so PowerShell script activation is unnecessary.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m gacl_pipeline
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Use `py -0p` to inspect installed versions. Python 3.11 is supported; Python 3.12 also works. Select an installed version explicitly rather than reinstalling Python unnecessarily.

If the website download fails certificate validation, use:

```powershell
.\.venv\Scripts\python.exe -m gacl_pipeline --from-examples
```

This loads the reviewed repository CSV extracts without networking. It is distinct from `--offline`, which requires previously downloaded, checksum-verified PDFs. Certificate diagnosis and the distinction are documented in HTTPS_TROUBLESHOOTING.md.

## macOS / Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/python -m gacl_pipeline
.venv/bin/python -m unittest discover -s tests -v
```

Run from the project directory. Alternatively pass `--root /absolute/path/to/project`.

## Verify setup

- The pipeline reports 18 extracted and 18 stored observations on a clean run.
- The four dataset-level checks pass.
- Rerun offline; the warehouse still contains 18 observations.
- Run the unit suite; see STATUS.md for the last verified test count.
- Open the two processed CSV files to inspect the dataset.

## Environments and versions

Core runtime dependencies: PyMuPDF 1.26.6, plus truststore 0.10.5 on Windows only. Both are pinned in pyproject.toml. The Windows downloader uses an explicit native-verification SSLContext; it does not patch process-wide SSL settings. After pulling dependency changes, rerun the editable installation command. The test suite uses Python's standard-library unittest. Optional cloud/dbt dependencies are declared separately and must be resolved in a separate environment or installed explicitly; they were not needed for local verification.

The .env.example file is documentation only: the application does not automatically load .env files.

## Sharing and syncing

Use feature branches for further work and keep generated PDFs, credentials and logs outside Git. A local SQLite database belongs to each clone. The remote repository stores code, documentation and a small reviewed example export, not a copy of every local output.

The workspace setup does not automatically install anything on another computer. Clone the repository and run these commands on the intended Windows machine.

