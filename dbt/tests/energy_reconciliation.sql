select
    source_id, document_sha256, period_start,
    sum(case when metric_id = 'energy_total' then value else 0 end) as total,
    sum(case when metric_id in ('energy_renewable_total', 'energy_nonrenewable_total') then value else 0 end) as components
from {{ ref('annual_company_observations') }}
where metric_id in ('energy_total', 'energy_renewable_total', 'energy_nonrenewable_total')
group by 1, 2, 3
having count(distinct metric_id) != 3 or abs(total - components) > 0.01

