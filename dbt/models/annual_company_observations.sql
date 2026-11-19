select *
from {{ ref('stg_observations') }}
where frequency = 'annual'
  and reporting_scope = 'gacl_standalone'
  and statistic_type = 'annual_total'

