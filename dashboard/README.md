# Power BI report — planned milestone

Status: specification prepared; no PBIX report has been created yet.

## Page 1: Reported trends

Import the generated monthly_site_observations.csv and annual_company_observations.csv separately. Set period fields to Date and value to Decimal Number. Preserve raw_value for audit.

- Monthly line chart: period_start vs average daily freshwater consumption, KL/day.
- Annual comparison: renewable/non-renewable energy, GJ, by financial year.
- Annual water totals: withdrawal, consumption and discharge, KL.
- Visible reporting scope and original source links.
- Do not use a summed daily-average card across months.
- Do not combine annual company totals and monthly site rates in the same measure.

## Page 2: Data quality and provenance

- Observation counts and covered periods.
- Latest successful run and dataset-check results.
- Source URLs with PDF page and printed page.
- Extraction method and report version.
- Any missing coverage or rejected input.

CSV import gives a credential-free first version. BigQuery direct connectivity comes after cloud validation. Ensure any financial-year label follows April–March, not calendar-year grouping.

Acceptance: every displayed value reconciles to SQL/CSV and the report refreshes successfully after an offline rerun.

