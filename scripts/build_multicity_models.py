"""Build local five-city LaDe-D models; raw files stay local and are never modified."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
LOCAL_PACKAGES = ROOT / "work" / "python-packages"
if LOCAL_PACKAGES.exists():
    sys.path.insert(0, str(LOCAL_PACKAGES))
import duckdb


def main():
    raw_dir = ROOT / "work/data/raw/delivery"
    files = sorted(raw_dir.glob("delivery*.parquet"))
    if len(files) != 5:
        raise SystemExit(f"Expected the five official city shards; found {len(files)} in {raw_dir}")
    expected = {"Chongqing", "Hangzhou", "Jilin", "Shanghai", "Yantai"}
    out = ROOT / "work/data/staged"
    out.mkdir(parents=True, exist_ok=True)
    (ROOT / "work/tmp/duckdb").mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    con.execute("SET memory_limit='1GB'")
    con.execute("SET threads=2")
    con.execute("SET temp_directory='work/tmp/duckdb'")
    import os
    os.chdir(ROOT)
    sql = (ROOT / "sql/04_multicity_model.sql").read_text(encoding="utf-8-sig")
    for statement in con.extract_statements(sql):
        con.execute(statement)
    pkg = "work/data/staged/multicity_package_fact.parquet"
    evt = "work/data/staged/multicity_delivery_events.parquet"
    cities = con.execute(f"SELECT city,count(*) n,count(DISTINCT order_id) orders,count(DISTINCT courier_id) couriers,min(accept_timestamp_2022_provisional),max(accept_timestamp_2022_provisional),quantile_cont(accept_to_delivery_elapsed_minutes,.5),quantile_cont(accept_to_delivery_elapsed_minutes,.9),countif(ds_matches_accept_date),countif(ds_matches_delivery_date),countif(delivery_on_later_calendar_date),countif(accept_to_delivery_elapsed_minutes>1440) FROM read_parquet('{pkg}') GROUP BY city ORDER BY city").fetchall()
    found = {r[0] for r in cities}
    if found != expected:
        raise SystemExit(f"Unexpected city labels: {found}")
    n, nd = con.execute(f"SELECT count(*),count(DISTINCT city||':'||order_id) FROM read_parquet('{pkg}')").fetchone()
    en, ed = con.execute(f"SELECT count(*),count(DISTINCT city||':'||order_id) FROM read_parquet('{evt}')").fetchone()
    errors = con.execute(f"SELECT countif(accept_timestamp_2022_provisional IS NULL OR delivery_timestamp_2022_provisional IS NULL),countif(accept_to_delivery_elapsed_minutes<0),countif(accept_to_delivery_elapsed_minutes IS NULL) FROM read_parquet('{pkg}')").fetchone()
    cardinality = con.execute(f"SELECT countif(event_count != 2 OR accepted != 1 OR finished != 1) FROM (SELECT city,order_id,count(*) event_count,countif(event_type='task_accepted') accepted,countif(event_type='delivery_task_finished') finished FROM read_parquet('{evt}') GROUP BY city,order_id)").fetchone()[0]
    print("City profile columns: city, rows, distinct orders, couriers, accept min/max (provisional), median/p90 elapsed min, ds-accept matches, ds-delivery matches, later delivery date, >24h")
    for row in cities: print(row)
    print(f"PACKAGE_MODEL rows={n:,} distinct_city_order={nd:,}; EVENT_MODEL rows={en:,} distinct_city_order={ed:,}; parse_errors/negative/null_elapsed={errors}; bad_event_composition={cardinality}")
    if n != nd or en != 2*n or ed != n or errors[0] or errors[2] or cardinality:
        raise SystemExit("Multicity model checks failed")
    print("Negative elapsed values are preserved for investigation; do not drop or repair without authoritative date logic.")
    print("Model checks passed. 2022 year remains provisional; intervals are not SLA/customer satisfaction measures.")

if __name__ == "__main__": main()



