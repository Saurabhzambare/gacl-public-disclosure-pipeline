-- SQLite inspection queries. Do not sum across different scopes or source versions.
SELECT reporting_scope, metric_id, period_start, unit, value, source_url, pdf_page
FROM observations
ORDER BY frequency, metric_id, period_start;

SELECT status, COUNT(*) AS runs FROM pipeline_runs GROUP BY status;

SELECT observation_id, COUNT(DISTINCT document_sha256) AS source_versions
FROM observations GROUP BY observation_id HAVING source_versions > 1;

