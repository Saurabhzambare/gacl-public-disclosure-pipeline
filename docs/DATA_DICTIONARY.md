# Data dictionary

## Observation contract

| Field | Type | Meaning |
|---|---|---|
| observation_id | SHA-256 string | Canonical identity from scope, metric, period, unit and statistic |
| source_id | string | Report identifier from source manifest |
| document_sha256 | SHA-256 string | Exact source-document version |
| source_url | URL | Official GACL PDF |
| pdf_page | integer | One-based page in the PDF file |
| printed_page | integer | Page number printed on that page |
| reporting_scope | enum | gacl_standalone or dahej_plot3_report |
| metric_id | string | Stable definition in config/metrics.json |
| period_start / period_end | ISO date | Inclusive reporting interval |
| frequency | enum | monthly or annual |
| statistic_type | enum | monthly_average_daily_rate or annual_total |
| unit | enum | KL/day, GJ or KL |
| raw_value | string | Extracted number as printed, including commas |
| value | decimal string | Normalized exact value; no comma separators |
| extraction_method | string | pdf_text_regex for this implementation |
| parser_version | string | Named document-specific parser |

## Metrics

| metric_id | Unit | Grain |
|---|---|---|
| freshwater_average_daily | KL/day | One month in the Dahej Plot 3 report |
| energy_renewable_total | GJ | Standalone company financial year |
| energy_nonrenewable_total | GJ | Standalone company financial year |
| energy_total | GJ | Standalone company financial year |
| water_withdrawal_total | KL | Standalone company financial year |
| water_consumption_total | KL | Standalone company financial year |
| water_discharge_total | KL | Standalone company financial year |

The selected BRSR reports FY 2025–26 and comparative FY 2024–25. Annual period boundaries are 1 April through 31 March. Monthly rates retain their month intervals; they are not measured daily events.

## Nulls and precision

parse_number distinguishes NA/dash/blank from zero. Required selected observations with missing values are rejected rather than silently filled. No interpolation is implemented. Retain the raw string so normalization is auditable.

Use Decimal for reconciliation. For energy, the FY 2024–25 disclosed subtotals have three-versus-two-decimal precision: their sum differs from the displayed total by 0.002 GJ. The documented arithmetic tolerance is 0.01 GJ.

## Safe analysis

Do not sum monthly daily averages as a six-month volume. Do not combine annual company water with monthly Dahej-only rates. Do not assume all products represent independent physical output: intermediate and final chemical products may overlap.

The two-year BRSR comparison is as disclosed in the latest report, not a guarantee that earlier reports used identical methodology.


Comparative-basis note: printed BRSR pages 79–80 state that FY 2024–25 disclosures were recalculated for reporting-boundary and methodology alignment. Water consumption for that year was revised using withdrawal minus discharge. The project retains the latest report's disclosed figures and does not overwrite earlier-source history.
