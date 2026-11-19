select
    observation_id,
    source_id,
    document_sha256,
    source_url,
    pdf_page,
    printed_page,
    reporting_scope,
    metric_id,
    cast(period_start as date) as period_start,
    cast(period_end as date) as period_end,
    frequency,
    statistic_type,
    unit,
    raw_value,
    cast(value as numeric) as value,
    extraction_method,
    parser_version
from {{ source('gacl_raw', 'observations') }}

