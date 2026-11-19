select observation_id, source_id, document_sha256
from {{ ref('stg_observations') }}
group by 1, 2, 3
having count(*) > 1

