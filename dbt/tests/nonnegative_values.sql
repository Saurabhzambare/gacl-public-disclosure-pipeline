select *
from {{ ref('stg_observations') }}
where value < 0 or period_start > period_end

