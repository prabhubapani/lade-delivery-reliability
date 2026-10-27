-- Exploratory aggregates from the provisional package-grain Jilin model.
-- Groups with fewer than 200 packages are omitted. Acceptance hour uses the source
-- clock string; the source timezone is not documented. These are not SLA metrics.

COPY (
    SELECT
        extract(hour FROM accept_timestamp_2022_provisional)::INTEGER AS accept_hour_source_clock,
        count(*) AS packages,
        quantile_cont(accept_to_delivery_elapsed_minutes, 0.50) AS median_elapsed_minutes,
        quantile_cont(accept_to_delivery_elapsed_minutes, 0.90) AS p90_elapsed_minutes,
        quantile_cont(accept_to_delivery_elapsed_minutes, 0.95) AS p95_elapsed_minutes
    FROM read_parquet('work/data/staged/jilin_package_fact.parquet')
    GROUP BY 1
    HAVING count(*) >= 200
    ORDER BY 1
) TO 'work/data/aggregates/jilin_by_accept_hour.parquet'
(FORMAT PARQUET, COMPRESSION ZSTD);

COPY (
    SELECT
        month(accept_timestamp_2022_provisional)::INTEGER AS accept_month_2022_provisional,
        region_id,
        count(*) AS packages,
        quantile_cont(accept_to_delivery_elapsed_minutes, 0.50) AS median_elapsed_minutes,
        quantile_cont(accept_to_delivery_elapsed_minutes, 0.90) AS p90_elapsed_minutes
    FROM read_parquet('work/data/staged/jilin_package_fact.parquet')
    GROUP BY 1, 2
    HAVING count(*) >= 200
    ORDER BY 1, 2
) TO 'work/data/aggregates/jilin_by_region_month.parquet'
(FORMAT PARQUET, COMPRESSION ZSTD);

COPY (
    SELECT
        region_id,
        extract(hour FROM accept_timestamp_2022_provisional)::INTEGER AS accept_hour_source_clock,
        count(*) AS packages,
        quantile_cont(accept_to_delivery_elapsed_minutes, 0.50) AS median_elapsed_minutes,
        quantile_cont(accept_to_delivery_elapsed_minutes, 0.90) AS p90_elapsed_minutes
    FROM read_parquet('work/data/staged/jilin_package_fact.parquet')
    GROUP BY 1, 2
    HAVING count(*) >= 200
    ORDER BY 1, 2
) TO 'work/data/aggregates/jilin_by_region_hour.parquet'
(FORMAT PARQUET, COMPRESSION ZSTD);

