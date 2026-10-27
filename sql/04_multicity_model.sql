-- Multi-city local delivery model. The source folder contains only the five official city shards.
-- Timestamp year 2022 is provisional; source strings contain no year or timezone.
COPY (
    WITH source_rows AS (
        SELECT *, filename AS source_file,
            try_strptime('2022-' || accept_time, '%Y-%m-%d %H:%M:%S') AS accept_timestamp_2022_provisional,
            try_strptime('2022-' || delivery_time, '%Y-%m-%d %H:%M:%S') AS delivery_timestamp_2022_provisional
        FROM read_parquet('work/data/raw/delivery/delivery*.parquet', filename=true)
    )
    SELECT *,
        date_diff('second', accept_timestamp_2022_provisional, delivery_timestamp_2022_provisional) / 60.0 AS accept_to_delivery_elapsed_minutes,
        (ds = month(accept_timestamp_2022_provisional)*100 + day(accept_timestamp_2022_provisional)) AS ds_matches_accept_date,
        (ds = month(delivery_timestamp_2022_provisional)*100 + day(delivery_timestamp_2022_provisional)) AS ds_matches_delivery_date,
        (accept_timestamp_2022_provisional = delivery_timestamp_2022_provisional) AS zero_duration_at_source_precision,
        (date_diff('second', accept_timestamp_2022_provisional, delivery_timestamp_2022_provisional) / 60.0 > 480) AS review_elapsed_over_8h,
        (CAST(delivery_timestamp_2022_provisional AS DATE) > CAST(accept_timestamp_2022_provisional AS DATE)) AS delivery_on_later_calendar_date
    FROM source_rows
) TO 'work/data/staged/multicity_package_fact.parquet' (FORMAT PARQUET, COMPRESSION ZSTD);

COPY (
    WITH source_rows AS (
        SELECT *, filename AS source_file,
            try_strptime('2022-' || accept_time, '%Y-%m-%d %H:%M:%S') AS accept_ts,
            try_strptime('2022-' || delivery_time, '%Y-%m-%d %H:%M:%S') AS delivery_ts,
            try_strptime('2022-' || accept_gps_time, '%Y-%m-%d %H:%M:%S') AS accept_gps_ts,
            try_strptime('2022-' || delivery_gps_time, '%Y-%m-%d %H:%M:%S') AS delivery_gps_ts
        FROM read_parquet('work/data/raw/delivery/delivery*.parquet', filename=true)
    ), events AS (
        SELECT order_id,city,region_id,courier_id,aoi_id,aoi_type,ds AS ds_raw,source_file,
            'task_accepted' AS event_type,accept_time AS event_time_text,accept_ts AS event_timestamp_2022_provisional,
            accept_gps_time AS event_gps_time_text,accept_gps_ts AS event_gps_timestamp_2022_provisional,
            accept_gps_lng AS event_gps_lng,accept_gps_lat AS event_gps_lat,lng AS package_stop_lng,lat AS package_stop_lat
        FROM source_rows
        UNION ALL
        SELECT order_id,city,region_id,courier_id,aoi_id,aoi_type,ds AS ds_raw,source_file,
            'delivery_task_finished',delivery_time,delivery_ts,delivery_gps_time,delivery_gps_ts,
            delivery_gps_lng,delivery_gps_lat,lng,lat
        FROM source_rows
    ) SELECT * FROM events
) TO 'work/data/staged/multicity_delivery_events.parquet' (FORMAT PARQUET, COMPRESSION ZSTD);

