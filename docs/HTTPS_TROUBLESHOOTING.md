# HTTPS download troubleshooting

## Symptom and meaning

Python installs and unit tests may succeed while downloading a GACL PDF fails
with CERTIFICATE_VERIFY_FAILED and “certificate has expired”. This means a
certificate in the validation chain was rejected. The terminal message alone
does not establish whether it is the website leaf certificate, an intermediate,
a local interception certificate, or an incorrect computer clock.

The report URLs were reachable with normal certificate verification from the
development environment on 19 November 2026. That does not establish what
certificate chain a different Windows network receives.

## Verified Windows resolution — 20 November 2026

The user's Windows Python 3.11/OpenSSL 1.1.1u rejected both gacl.com and
www.gacl.com with verification code 10 (certificate has expired), while the
browser opened the report normally. The diagnostic clock showed 20 November
2026. This does not identify the particular certificate responsible.

A one-process launcher using truststore 0.10.5 native Windows verification
successfully refreshed both pinned PDFs, extracted and loaded 18 observations,
retained 18 warehouse rows and passed all four aggregate checks. User-reported
run ID: 4a949773-e15d-4b6a-a7fb-6cb83d55ee6f; input_mode=verified_pdfs;
pdfs_verified_this_run=true. This is evidence from the user's terminal output.

The downloader now supplies an explicit truststore.SSLContext with
ssl.PROTOCOL_TLS_CLIENT on Windows. Other platforms use ssl.create_default_context.
There is no global SSL injection or automatic switch to reviewed CSVs.
Install the updated dependency metadata before using the normal command:

```powershell
git pull --ff-only
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m gacl_pipeline --refresh
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The integrated normal `--refresh` command was subsequently confirmed on the
user's Windows laptop on 20 November (run
a027f1fa-4961-4cce-b2cd-bb976f54a860); see [status](STATUS.md). This historical
success does not guarantee the current website/network certificate chain.
Certificate failures still stop immediately; source hashes remain required.
Native validation does not renew expired certificates. If validation still
fails, diagnose the received certificate chain rather than bypassing checks.

Reference: https://truststore.readthedocs.io/en/latest/

## Continue with reviewed data

Update the clone with git pull --ff-only, then run:

```powershell
.\.venv\Scripts\python.exe -m gacl_pipeline --from-examples
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

No dependency change is required for this mode. Editable installs use the updated
Python files automatically.

Expected: 18 loaded rows, 18 warehouse rows, four passing aggregate checks and
input_mode = reviewed_extracts. extracted_rows = 0 and pdfs_verified_this_run =
false are intentional: this run did not parse or verify the original PDFs.

The two factual CSV extracts were generated and reviewed during initial setup.
config/examples.json pins their normalized UTF-8/LF checksums so Windows CRLF
line endings do not cause a false mismatch. Source URLs, page numbers, raw
values and original document hashes remain available. Contract and aggregate
checks still run; modified snapshots fail before observation loading.

There is no automatic switch from live download to reviewed extracts. The user
must choose the mode explicitly, and logs, run history and the processed
run_manifest.json record it. Repeated loads are duplicate-safe.

## Diagnose HTTPS separately

1. Run Get-Date in PowerShell and confirm that the computer date, time and time
   zone are correct. Correct them if they are wrong.
2. Open the exact report URL from config/sources.json in the normal browser.
   Inspect the certificate issuer and validity dates if a warning appears;
   do not proceed through a certificate warning to obtain the file.
3. If the browser succeeds but Python fails, investigate the Python/Windows
   certificate chain or any managed network/antivirus HTTPS inspection. Update
   the intended trust chain through its normal vendor or administrator process.
4. If the website certificate is expired for the normal connection, the site
   operator must renew it. Updating pip does not renew a website certificate.
5. Return to the default PDF pipeline once the connection validates normally.

The code does not disable TLS verification, use an unverified SSL context, or
switch to HTTP. Certificate errors fail immediately instead of wasting retries.
Source checksum validation is preserved.

## Phase 2 distinction

The assistant's document index needs actual checksum-verified cached PDF bytes.
`--from-examples` can preserve access to the 18 structured observations but does
not supply document text, pages or an embedding corpus. Do not bypass TLS or
silently substitute generated passages when a source is unavailable. Model
downloads, if later selected, need their own trusted distribution/license review;
they are not part of this report-download fix. Follow
[build-order Step 1](PHASE_2_BUILD_ORDER.md) before making environment changes.

Python reference: https://docs.python.org/3.11/library/ssl.html
