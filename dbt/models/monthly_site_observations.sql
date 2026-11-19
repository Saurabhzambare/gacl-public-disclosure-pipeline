select *
from {{ ref('stg_observations') }}
where frequency = 'monthly'
  and reporting_scope = 'dahej_plot3_report'
  and statistic_type = 'monthly_average_daily_rate'
  and unit = 'KL/day'

