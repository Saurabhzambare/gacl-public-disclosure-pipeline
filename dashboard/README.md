# Power BI report — planned milestone

Status: specification prepared; no PBIX report has been created yet.

## Connect Power BI Desktop to the validated dbt views

On 22 November, the user verified all eight BigQuery reference checks. Power BI
connectivity and report creation are not yet verified. Start a blank report:

1. Home > Get data > More > Google BigQuery > Connect.
2. In Advanced options, set Billing Project ID to instacart-analytics-practice
   and Use Storage API to false. The billing-project field selects the project
   used for queries; it does not enable billing. False uses REST rather than the
   Storage API. These options follow Microsoft's connector documentation.
3. Sign in with the Google account that can access the existing project.
4. In Navigator, expand instacart-analytics-practice > gacl_public_disclosures.
   Select monthly_site_observations and annual_company_observations.
5. Choose Import when asked about connectivity mode, then Transform Data to
   inspect the imported views before applying changes.

If the Storage API option is absent, inspect the connection's Source step in
Power Query. Its options record can include:

```powerquery
GoogleBigQuery.Database([
    BillingProject = "instacart-analytics-practice",
    UseStorageApi = false
])
```

Keep the Navigator-generated project/schema/view steps. Connector versions and
available UI fields vary; diagnose the actual message rather than enabling
billing. No DirectQuery or paid-capacity setup is needed for this small report.
Reference: https://learn.microsoft.com/en-us/power-query/connectors/google-bigquery

Import acceptance: 6 monthly rows and 12 annual rows; period_start/period_end
are Date; value is Decimal Number; source_url and page references are retained.
Leave the two fact tables unrelated: they have different reporting scopes and
grains. No automatic relationship should be used to combine their measurements.

If direct connectivity is unavailable in the sandbox, run SELECT * against each
validated dbt view in BigQuery and download its query results as CSV. Import those
cloud-view exports into Power BI and document the manual export/refresh step.
This differs from importing the pre-cloud local exports below.

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

Local CSV import gives a credential-free alternative. BigQuery views now pass the reference checks; direct Power BI connectivity is the next verification step. Ensure any financial-year label follows April–March, not calendar-year grouping.

Acceptance: every displayed value reconciles to SQL/CSV and the report refreshes successfully after an offline rerun.

