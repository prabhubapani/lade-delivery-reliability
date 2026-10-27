"""Create small, local, privacy-conscious exploratory aggregates for Jilin."""

from pathlib import Path
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
LOCAL_PACKAGES = ROOT / "work" / "python-packages"
if LOCAL_PACKAGES.exists():
    sys.path.insert(0, str(LOCAL_PACKAGES))

import duckdb


MODEL_FILE = ROOT / "work" / "data" / "staged" / "jilin_package_fact.parquet"
OUTPUT_DIR = ROOT / "work" / "data" / "aggregates"
AGGREGATE_SQL = ROOT / "sql" / "03_jilin_aggregates.sql"


def main() -> None:
    if not MODEL_FILE.exists():
        raise FileNotFoundError("Run scripts/build_jilin_models.py first.")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    os.chdir(ROOT)
    con = duckdb.connect()
    for statement in con.extract_statements(AGGREGATE_SQL.read_text(encoding="utf-8")):
        con.execute(statement)

    for name in (
        "jilin_by_accept_hour.parquet",
        "jilin_by_region_month.parquet",
        "jilin_by_region_hour.parquet",
    ):
        result = con.execute(
            f"SELECT count(*) groups, min(packages) min_packages, min(p90_elapsed_minutes) min_p90, max(p90_elapsed_minutes) max_p90 FROM read_parquet('work/data/aggregates/{name}')"
        ).fetchone()
        if result[1] < 200:
            raise RuntimeError(f"Minimum-volume rule failed for {name}: {result}")
        print(f"{name}: {result[0]} groups; each has at least {result[1]:,} packages")

    print("Aggregates use acceptance time and provisional 2022 parsing; they are not SLA metrics.")
    print(f"Local aggregate files: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

