"""Build local, derived Parquet models from the one-city LaDe-D sample."""

from pathlib import Path
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "work" / "data" / "raw" / "delivery" / "delivery_jl.parquet"
STAGED_DIR = ROOT / "work" / "data" / "staged"
MODEL_SQL = ROOT / "sql" / "02_jilin_model.sql"
LOCAL_PACKAGES = ROOT / "work" / "python-packages"

if LOCAL_PACKAGES.exists():
    sys.path.insert(0, str(LOCAL_PACKAGES))

import duckdb


def main() -> None:
    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Jilin source file not found: {RAW_FILE}\n"
            "Read the LaDe-D research-use terms and place only the Jilin delivery shard there."
        )

    STAGED_DIR.mkdir(parents=True, exist_ok=True)
    os.chdir(ROOT)
    con = duckdb.connect()
    for statement in con.extract_statements(MODEL_SQL.read_text(encoding="utf-8")):
        con.execute(statement)

    package_path = "work/data/staged/jilin_package_fact.parquet"
    event_path = "work/data/staged/jilin_delivery_events.parquet"

    package = con.execute(
        f"""SELECT count(*) AS rows,
                   count(DISTINCT order_id) AS distinct_orders,
                   countif(accept_timestamp_2022_provisional IS NULL
                       OR delivery_timestamp_2022_provisional IS NULL) AS unparsed_timestamps
            FROM read_parquet('{package_path}')"""
    ).fetchone()
    events = con.execute(
        f"""SELECT count(*) AS rows,
                   count(DISTINCT order_id) AS distinct_orders,
                   countif(event_timestamp_2022_provisional IS NULL) AS unparsed_timestamps,
                   countif(event_gps_timestamp_2022_provisional
                       != event_timestamp_2022_provisional) AS gps_time_mismatches
            FROM read_parquet('{event_path}')"""
    ).fetchone()
    cardinality = con.execute(
        f"""SELECT count(*) AS orders,
                   countif(event_count != 2) AS orders_not_two_events,
                   countif(accept_events != 1 OR finish_events != 1) AS wrong_event_composition
            FROM (
                SELECT order_id,
                       count(*) AS event_count,
                       countif(event_type = 'task_accepted') AS accept_events,
                       countif(event_type = 'delivery_task_finished') AS finish_events
                FROM read_parquet('{event_path}')
                GROUP BY order_id
            )"""
    ).fetchone()

    expected_events = package[0] * 2
    if package[0] != package[1] or package[2] != 0:
        raise RuntimeError(f"Package model quality check failed: {package}")
    if events[0] != expected_events or events[1] != package[0] or events[2:] != (0, 0):
        raise RuntimeError(f"Event model quality check failed: {events}")
    if cardinality[1:] != (0, 0):
        raise RuntimeError(f"Per-package event cardinality check failed: {cardinality}")

    print(f"Package model: {package[0]:,} rows, {package[1]:,} distinct orders")
    print(f"Event model: {events[0]:,} rows ({events[0] // 2:,} acceptance + {events[0] // 2:,} completion events)")
    print("Checks passed: parsed timestamps, one of each event type per order, GPS/event times aligned.")
    print("Timestamp year 2022 remains provisional; this is not an SLA or customer-satisfaction model.")
    print(f"Staged outputs: {STAGED_DIR}")


if __name__ == "__main__":
    main()

