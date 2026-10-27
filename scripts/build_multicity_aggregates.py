"""Write aggregate-only CSVs for Power BI. No raw package or courier data is exported."""
from pathlib import Path
import sys,os
ROOT=Path(__file__).resolve().parents[1]
if (ROOT/'work/python-packages').exists(): sys.path.insert(0,str(ROOT/'work/python-packages'))
import duckdb

def main():
 os.chdir(ROOT); out=ROOT/'work/data/aggregates'; out.mkdir(parents=True,exist_ok=True); (ROOT/'work/tmp/duckdb').mkdir(parents=True,exist_ok=True)
 c=duckdb.connect(); c.execute("SET memory_limit='1GB'"); c.execute('SET threads=2'); c.execute("SET temp_directory='work/tmp/duckdb'")
 p="read_parquet('work/data/staged/multicity_package_fact.parquet')"
 for name, select_sql in {
  'city_month': f"SELECT city,year(accept_timestamp_2022_provisional) accept_year,month(accept_timestamp_2022_provisional) accept_month,count(*) package_count,quantile_cont(accept_to_delivery_elapsed_minutes,.5) median_elapsed_min,quantile_cont(accept_to_delivery_elapsed_minutes,.9) p90_elapsed_min,quantile_cont(accept_to_delivery_elapsed_minutes,.95) p95_elapsed_min,countif(accept_to_delivery_elapsed_minutes<0) negative_elapsed_count,countif(accept_to_delivery_elapsed_minutes=0) zero_elapsed_count,countif(accept_to_delivery_elapsed_minutes>480) over_8h_count,countif(accept_to_delivery_elapsed_minutes>1440) over_24h_count,countif(ds_matches_accept_date) ds_accept_match_count,countif(ds_matches_delivery_date) ds_delivery_match_count,countif(delivery_on_later_calendar_date) cross_calendar_date_count FROM {p} GROUP BY 1,2,3",
  'city_accept_hour': f"SELECT city,year(accept_timestamp_2022_provisional) accept_year,month(accept_timestamp_2022_provisional) accept_month,hour(accept_timestamp_2022_provisional) source_accept_hour,count(*) package_count,quantile_cont(accept_to_delivery_elapsed_minutes,.5) median_elapsed_min,quantile_cont(accept_to_delivery_elapsed_minutes,.9) p90_elapsed_min,countif(accept_to_delivery_elapsed_minutes<0) negative_elapsed_count FROM {p} GROUP BY 1,2,3,4 HAVING count(*)>=200",
  'city_region_month': f"SELECT city,region_id,year(accept_timestamp_2022_provisional) accept_year,month(accept_timestamp_2022_provisional) accept_month,count(*) package_count,quantile_cont(accept_to_delivery_elapsed_minutes,.5) median_elapsed_min,quantile_cont(accept_to_delivery_elapsed_minutes,.9) p90_elapsed_min,countif(accept_to_delivery_elapsed_minutes<0) negative_elapsed_count,countif(accept_to_delivery_elapsed_minutes>1440) over_24h_count FROM {p} GROUP BY 1,2,3,4 HAVING count(*)>=200"
 }.items():
  path=f'work/data/aggregates/{name}.csv'; c.execute(f"COPY ({select_sql}) TO '{path}' (HEADER, DELIMITER ',')"); print(name,c.execute(f"SELECT count(*) FROM read_csv_auto('{path}')").fetchone()[0],path)
 print('Aggregate CSVs contain no package IDs or courier IDs. Groups below 200 are omitted from hourly and region-month views.')
if __name__=='__main__': main()


