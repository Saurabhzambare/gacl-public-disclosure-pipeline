-- Read-only GoogleSQL verification for the user's billing-free project.
-- Expected facts come from checksum-pinned data/examples CSVs, reviewed against
-- the two official GACL PDF tables. They are not synthetic measurements.
-- FY 2024-25 values retain the comparative basis disclosed in the latest BRSR.
-- This query checks all 18 values, dates, units and scopes through the raw table
-- and three dbt views. It does not measure operational/compliance performance.
-- Expected: 8 rows, all passed=true. Rows counts: 18 / 18 / 6 / 12;
-- comparison differences: 0 for every relation. Uses sandbox SELECT query quota.
WITH expected AS (
  SELECT * FROM UNNEST(ARRAY<STRUCT<
    reporting_scope STRING, metric_id STRING, period_start DATE,
    period_end DATE, value NUMERIC, unit STRING
  >>[
    ('dahej_plot3_report', 'freshwater_average_daily', DATE '2025-04-01', DATE '2025-04-30', NUMERIC '12540.8', 'KL/day'),
    ('dahej_plot3_report', 'freshwater_average_daily', DATE '2025-05-01', DATE '2025-05-31', NUMERIC '12621.3', 'KL/day'),
    ('dahej_plot3_report', 'freshwater_average_daily', DATE '2025-06-01', DATE '2025-06-30', NUMERIC '12452.7', 'KL/day'),
    ('dahej_plot3_report', 'freshwater_average_daily', DATE '2025-07-01', DATE '2025-07-31', NUMERIC '11818.3', 'KL/day'),
    ('dahej_plot3_report', 'freshwater_average_daily', DATE '2025-08-01', DATE '2025-08-31', NUMERIC '11865.5', 'KL/day'),
    ('dahej_plot3_report', 'freshwater_average_daily', DATE '2025-09-01', DATE '2025-09-30', NUMERIC '11738.1', 'KL/day'),
    ('gacl_standalone', 'energy_nonrenewable_total', DATE '2024-04-01', DATE '2025-03-31', NUMERIC '9258233.07', 'GJ'),
    ('gacl_standalone', 'energy_nonrenewable_total', DATE '2025-04-01', DATE '2026-03-31', NUMERIC '8304003.87', 'GJ'),
    ('gacl_standalone', 'energy_renewable_total', DATE '2024-04-01', DATE '2025-03-31', NUMERIC '1826958.988', 'GJ'),
    ('gacl_standalone', 'energy_renewable_total', DATE '2025-04-01', DATE '2026-03-31', NUMERIC '2654765.03', 'GJ'),
    ('gacl_standalone', 'energy_total', DATE '2024-04-01', DATE '2025-03-31', NUMERIC '11085192.06', 'GJ'),
    ('gacl_standalone', 'energy_total', DATE '2025-04-01', DATE '2026-03-31', NUMERIC '10958768.90', 'GJ'),
    ('gacl_standalone', 'water_consumption_total', DATE '2024-04-01', DATE '2025-03-31', NUMERIC '3300699', 'KL'),
    ('gacl_standalone', 'water_consumption_total', DATE '2025-04-01', DATE '2026-03-31', NUMERIC '3480016', 'KL'),
    ('gacl_standalone', 'water_discharge_total', DATE '2024-04-01', DATE '2025-03-31', NUMERIC '2697153', 'KL'),
    ('gacl_standalone', 'water_discharge_total', DATE '2025-04-01', DATE '2026-03-31', NUMERIC '2699559.81', 'KL'),
    ('gacl_standalone', 'water_withdrawal_total', DATE '2024-04-01', DATE '2025-03-31', NUMERIC '5997852', 'KL'),
    ('gacl_standalone', 'water_withdrawal_total', DATE '2025-04-01', DATE '2026-03-31', NUMERIC '6179576', 'KL')
  ])
),
raw_facts AS (
  SELECT reporting_scope, metric_id, CAST(period_start AS DATE) AS period_start,
    CAST(period_end AS DATE) AS period_end, CAST(value AS NUMERIC) AS value, unit
  FROM `instacart-analytics-practice.gacl_public_disclosures.observations`
),
raw_facts_differences AS (
  SELECT * FROM (SELECT * FROM expected EXCEPT DISTINCT SELECT * FROM raw_facts)
  UNION ALL
  SELECT * FROM (SELECT * FROM raw_facts EXCEPT DISTINCT SELECT * FROM expected)
),
staged_facts AS (
  SELECT reporting_scope, metric_id, period_start, period_end, value, unit
  FROM `instacart-analytics-practice.gacl_public_disclosures.stg_observations`
),
staged_facts_differences AS (
  SELECT * FROM (SELECT * FROM expected EXCEPT DISTINCT SELECT * FROM staged_facts)
  UNION ALL
  SELECT * FROM (SELECT * FROM staged_facts EXCEPT DISTINCT SELECT * FROM expected)
),
monthly_facts AS (
  SELECT reporting_scope, metric_id, period_start, period_end, value, unit
  FROM `instacart-analytics-practice.gacl_public_disclosures.monthly_site_observations`
),
monthly_facts_differences AS (
  SELECT * FROM (SELECT * FROM expected WHERE reporting_scope = 'dahej_plot3_report' EXCEPT DISTINCT SELECT * FROM monthly_facts)
  UNION ALL
  SELECT * FROM (SELECT * FROM monthly_facts EXCEPT DISTINCT SELECT * FROM expected WHERE reporting_scope = 'dahej_plot3_report')
),
annual_facts AS (
  SELECT reporting_scope, metric_id, period_start, period_end, value, unit
  FROM `instacart-analytics-practice.gacl_public_disclosures.annual_company_observations`
),
annual_facts_differences AS (
  SELECT * FROM (SELECT * FROM expected WHERE reporting_scope = 'gacl_standalone' EXCEPT DISTINCT SELECT * FROM annual_facts)
  UNION ALL
  SELECT * FROM (SELECT * FROM annual_facts EXCEPT DISTINCT SELECT * FROM expected WHERE reporting_scope = 'gacl_standalone')
)
SELECT 'observations: row count' AS check_name, COUNT(*) AS observed, 18 AS expected, COUNT(*) = 18 AS passed FROM raw_facts
UNION ALL
SELECT 'observations: differing facts', COUNT(*), 0, COUNT(*) = 0 FROM raw_facts_differences
UNION ALL
SELECT 'stg_observations: row count' AS check_name, COUNT(*) AS observed, 18 AS expected, COUNT(*) = 18 AS passed FROM staged_facts
UNION ALL
SELECT 'stg_observations: differing facts', COUNT(*), 0, COUNT(*) = 0 FROM staged_facts_differences
UNION ALL
SELECT 'monthly_site_observations: row count' AS check_name, COUNT(*) AS observed, 6 AS expected, COUNT(*) = 6 AS passed FROM monthly_facts
UNION ALL
SELECT 'monthly_site_observations: differing facts', COUNT(*), 0, COUNT(*) = 0 FROM monthly_facts_differences
UNION ALL
SELECT 'annual_company_observations: row count' AS check_name, COUNT(*) AS observed, 12 AS expected, COUNT(*) = 12 AS passed FROM annual_facts
UNION ALL
SELECT 'annual_company_observations: differing facts', COUNT(*), 0, COUNT(*) = 0 FROM annual_facts_differences
ORDER BY check_name;
