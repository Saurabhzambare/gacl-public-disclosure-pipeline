# Power BI report

The author built **GACL_Public_Disclosure_Report** in Power BI Desktop and
confirmed a successful refresh. The actual exported PDF was reviewed on
24 November 2026. This is an independent portfolio report using public GACL
disclosures, not an internal GACL application.

[Open the two-page PDF](GACL_Public_Disclosure_Report.pdf) ·
[Overview preview](screenshots/water-energy-overview.png) ·
[Sources preview](screenshots/sources-coverage.png) ·
[Walkthrough script](../docs/WALKTHROUGH.md)

The previews are rendered from the supplied PDF. The editable PBIX remains on
the author's laptop and is excluded by the repository's existing ignore rule.
The PDF is unchanged, including a small grey heading mark retained by the author.
These files are static exports; interactive filtering and Desktop refresh require
the original report or reconstruction using the details below.

## Actual pages

| Page | Contents |
|---|---|
| Water & Energy Overview | Monthly Dahej Plot 3 freshwater line; stacked annual renewable/non-renewable energy; clustered annual water consumption, discharge and withdrawal; units, reporting scopes, comparative-year note and source links |
| Sources & Coverage | Monthly/annual/total observation counts; source report names, measurement groups, PDF/printed pages; covered periods, units and reading notes; source links |

Page 2 is a coverage/provenance page. Latest-run status, validation outcomes,
quarantine counts and extraction-method fields from the original design are not
live report visuals. Observation counts are not validation-test results.

## Data connection and grain

The user's Desktop workflow showed Google BigQuery navigation to project
`instacart-analytics-practice`, dataset `gacl_public_disclosures`, and the two dbt
reporting views:

| Table | Rows | Grain and unit |
|---|---:|---|
| monthly_site_observations | 6 | One monthly average daily freshwater rate for Dahej Plot 3, KL/day |
| annual_company_observations | 12 | Six annual standalone company energy/water metrics across two financial years, GJ or KL |

The user confirmed a successful Desktop refresh. Exact connection options and
Import/DirectQuery mode have not been independently inspected from PBIX source.
For reconstruction, connect through Home > Get data > Google BigQuery, select the
same two views and use Import for this small report. The earlier connection
recommendation was Billing Project ID `instacart-analytics-practice` and
`UseStorageApi=false`; these are recommended setup options, not verified settings
from the supplied PDF. See [cloud setup](../docs/BIGQUERY_DBT.md).

Set period_start/period_end to Date and value to Decimal Number. Retain raw_value,
source_url, source_id, reporting_scope, document_sha256 and page fields for
traceability. Keep the fact tables separate when reconstructing: their grains
and boundaries differ. Do not join annual company totals to monthly site rates
as though they describe the same observation.

## Measures used in the report

```dax
Monthly Freshwater (KL/day) =
SELECTEDVALUE('monthly_site_observations'[value])

Annual Reported Value =
SELECTEDVALUE('annual_company_observations'[value])

Monthly Observations =
COUNTROWS('monthly_site_observations')

Annual Observations =
COUNTROWS('annual_company_observations')

Total Observations =
[Monthly Observations] + [Annual Observations]
```

SELECTEDVALUE returns a value only when the visual context identifies one distinct
value. Monthly points use period_start. Annual visuals use Financial Year and
Metric Label, with the appropriate metric filter. Do not replace the monthly
measure with a sum across months. Counts respond to report filter context.

The annual table's calculated Financial Year column follows April–March:

```dax
Financial Year =
"FY " & YEAR([period_start]) & "–" & YEAR([period_end])
```

The annual Metric Label helper maps identifiers as follows:

| metric_id | Metric Label | Measurement Group |
|---|---|---|
| energy_nonrenewable_total | Non-renewable energy | Energy |
| energy_renewable_total | Renewable energy | Energy |
| energy_total | Total energy | Energy |
| water_withdrawal_total | Water withdrawal | Water withdrawal & consumption |
| water_consumption_total | Water consumption | Water withdrawal & consumption |
| water_discharge_total | Water discharge | Water discharge |

Annual Report Name is `BRSR 2025–2026`. The monthly Report Name is
`EC compliance · Apr–Sep 2025`, and its Measurement Group is
`Average daily freshwater use`. These are display helpers, not extra source facts.

## Visual configuration

- Monthly line: period_start as month/year; Monthly Freshwater (KL/day) as value;
  straight blue line with markers; six exact labels to one decimal place.
- Annual energy: stacked columns by Financial Year, Metric Label as legend,
  Annual Reported Value as value. Include only renewable and non-renewable
  metrics; exclude energy_total to avoid double counting. Labels use millions
  to two decimal places. Non-renewable is blue; renewable is teal.
- Annual water: clustered columns by Financial Year, Metric Label as legend,
  Annual Reported Value as value. Include consumption, discharge and withdrawal.
  Labels use millions to two decimal places; orange, purple and blue respectively.
- Source tables: Report Name, Measurement Group, pdf_page and printed_page;
  page fields set to Don't summarize, totals off. Rename page headers for display.
  The annual references collapse repeated financial-year/metric records to the
  three unique displayed source-page groups; they are not observation counts.
- Both pages: 1280 × 720 canvas; background #F4F7FB; navy #073763 title bars;
  dark #10243A text; pale blue notes; white panels. Monthly axis is cropped
  around the observed range; annual column axes start at zero.

## Checked values and source references

Monthly values, April to September 2025, are respectively
12,540.8; 12,621.3; 12,452.7; 11,818.3; 11,865.5; 11,738.1 KL/day.
Annual chart labels are rounded display values; unrounded observations and raw
source strings remain in the pipeline. Financial years cover 2024–2025 and
2025–2026; the earlier year uses recalculated comparatives from the latest BRSR.

| Reference | PDF page | Printed page |
|---|---:|---:|
| Annual energy | 36 | 78 |
| Annual water withdrawal and consumption | 37 | 79 |
| Annual water discharge | 38 | 80 |
| Monthly average daily freshwater use | 5 | 4 |

Both pages contain an Annual source PDF and Monthly source PDF hyperlink:

- https://gacl.com/wp-content/uploads/2026/08/53RD-AR-BRSR.pdf
- https://gacl.com/wp-content/uploads/2026/04/EC_Compliance_Plot-3_April-to-Sept-25.pdf

All four exported PDF link annotations retain those destinations. This checks
the stored URLs, not ongoing website availability. Every monthly point, rounded
annual label, source reference and 6/12/18 count was checked in the supplied export.

## Refresh and export

1. Complete a successful local pipeline run. Use the existing virtual environment;
   `--offline` requires the previously verified PDFs in the local cache.
2. Load the complete local export with the explicit BigQuery snapshot command in
   [cloud setup](../docs/BIGQUERY_DBT.md). This replaces the cloud snapshot.
3. Run the pinned dbt build, then the read-only
   [reference comparison](../sql/bigquery_verification.sql). Stop if any stage fails.
4. In Power BI Desktop, open the local PBIX and choose Home > Refresh. Confirm
   success, six monthly points, two annual periods, and counts 6/12/18 with
   relevant filters cleared. A refresh against unchanged pinned sources should
   retain the same facts.
5. Save the PBIX, export both pages to PDF, and review every label, reference and
   footer. Update the repository PDF and previews together when the report changes.

Individual cloud/dbt checks and Desktop refresh are evidenced; the complete
sequence above has not yet been captured as one end-to-end run. Automated
scheduling, Power BI Service deployment and scheduled Service refresh are not
implemented. The source PDFs and selected history change only through a reviewed
manifest/parser update; refreshing does not discover new reports automatically.
