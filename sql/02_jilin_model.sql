-- Build package-grain and event-grain Parquet models from the single raw Jilin shard.
-- Source data remains read-only. The year 2022 is provisional; timestamps have no year/timezone.

COPY (
    WITH parsed AS (
        SELECT
            *,
            try_strptime('2022-' || accept_time, '%Y-%m-%d %H:%M:%S') AS accept_timestamp_2022_provisional,
            try_strptime('2022-' || delivery_time, '%Y-%m-%d %H:%M:%S') AS delivery_timestamp_2022_provisional
        FROM read_parquet('work/data/raw/delivery/delivery_jl.parquet')
    )
    SELECT
        *,
        date_diff('minute', accept_timestamp_2022_provisional, delivery_timestamp_2022_provisional)
            AS accept_to_delivery_elapsed_minutes,
        (ds // 100 = month(accept_timestamp_2022_provisional)
            AND ds % 100 = day(accept_timestamp_2022_provisional)) AS ds_matches_accept_date,
        (ds // 100 = month(delivery_timestamp_2022_provisional)
            AND ds % 100 = day(delivery_timestamp_2022_provisional)) AS ds_matches_delivery_date,
        (accept_timestamp_2022_provisional = delivery_timestamp_2022_provisional)
            AS zero_minute_at_source_precision,
        (date_diff('minute', accept_timestamp_2022_provisional, delivery_timestamp_2022_provisional) > 8 * 60)
            AS review_elapsed_over_8h,
        (CAST(delivery_timestamp_2022_provisional AS DATE) > CAST(accept_timestamp_2022_provisional AS DATE))
            AS delivery_timestamp_on_later_calendar_date
    FROM parsed
) TO 'work/data/staged/jilin_package_fact.parquet'
(FORMAT PARQUET, COMPRESSION ZSTD);

COPY (
    WITH source_rows AS (
        SELECT
            order_id, region_id, city, courier_id, lng AS package_stop_lng, lat AS package_stop_lat,
            aoi_id, aoi_type, ds AS ds_raw,
            accept_time, accept_gps_time, accept_gps_lng, accept_gps_lat,
            delivery_time, delivery_gps_time, delivery_gps_lng, delivery_gps_lat,
            try_strptime('2022-' || accept_time, '%Y-%m-%d %H:%M:%S') AS accept_timestamp_2022_provisional,
            try_strptime('2022-' || delivery_time, '%Y-%m-%d %H:%M:%S') AS delivery_timestamp_2022_provisional,
            try_strptime('2022-' || accept_gps_time, '%Y-%m-%d %H:%M:%S') AS accept_gps_timestamp_2022_provisional,
            try_strptime('2022-' || delivery_gps_time, '%Y-%m-%d %H:%M:%S') AS delivery_gps_timestamp_2022_provisional
        FROM read_parquet('work/data/raw/delivery/delivery_jl.parquet')
    ),
    events AS (
        SELECT
            order_id, city, region_id, courier_id, aoi_id, aoi_type, ds_raw,
            1 AS event_order,
            'task_accepted' AS event_type,
            accept_time AS event_time_text,
            accept_timestamp_2022_provisional AS event_timestamp_2022_provisional,
            accept_gps_time AS event_gps_time_text,
            accept_gps_timestamp_2022_provisional AS event_gps_timestamp_2022_provisional,
            accept_gps_lng AS event_gps_lng,
            accept_gps_lat AS event_gps_lat,
            package_stop_lng,
            package_stop_lat
        FROM source_rows

        UNION ALL

        SELECT
            order_id, city, region_id, courier_id, aoi_id, aoi_type, ds_raw,
            2 AS event_order,
            'delivery_task_finished' AS event_type,
            delivery_time AS event_time_text,
            delivery_timestamp_2022_provisional AS event_timestamp_2022_provisional,
            delivery_gps_time AS event_gps_time_text,
            delivery_gps_timestamp_2022_provisional AS event_gps_timestamp_2022_provisional,
            delivery_gps_lng AS event_gps_lng,
            delivery_gps_lat AS event_gps_lat,
            package_stop_lng,
            package_stop_lat
        FROM source_rows
    )
    SELECT * FROM events
) TO 'work/data/staged/jilin_delivery_events.parquet'
(FORMAT PARQUET, COMPRESSION ZSTD);

