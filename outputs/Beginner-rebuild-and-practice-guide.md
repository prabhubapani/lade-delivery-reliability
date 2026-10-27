# Beginner rebuild and practice guide

This guide explains how to reproduce the LaDe-D delivery analysis from the beginning on Windows. It names the official source, shows how to download one city first, then how to run the project code and inspect the outputs. It is written for learning: read each step, run it, and compare your result with the expected checks below.

## 1. What you are building

You are building an operational data audit and two aggregate dashboards from historical LaDe-D package records. The main measure is the elapsed time between a recorded task-acceptance timestamp and a recorded task-completion timestamp. The measure is descriptive. The inspected schema has no promised delivery deadline, SLA, or customer-review field, so it cannot prove on-time performance or customer satisfaction.

This project analyzes the five official city delivery shards inspected here: Chongqing, Hangzhou, Jilin, Shanghai, and Yantai. They contain 4,514,661 package rows in total. The source describes the broader LaDe dataset as about 10.7 million packages, but this analysis does not claim to cover all of those packages. The data is historical and from China; it is not an India benchmark.

## 2. Review the source before downloading

Open the [LaDe-D dataset card](https://huggingface.co/datasets/Cainiao-AI/LaDe-D), the [official files page](https://huggingface.co/datasets/Cainiao-AI/LaDe-D/tree/main/data), the [LaDe project page](https://github.com/wenhaomin/LaDe), and this repository's [data and code notice](../DATA-AND-CODE-NOTICE.md).

The Hugging Face card currently labels LaDe-D Apache-2.0. The LaDe project describes research use, and the original paper's datasheet has also been described as CC BY-NC 4.0. These statements are inconsistent; this project does not decide which terms control. Keep the original files local. Never put raw Parquet files, package IDs, courier IDs, or local database files into this public repository. Recheck the current source terms and attribution before adapting or redistributing derived work, especially for commercial use.

## 3. Prepare the project on Windows

1. Install Python and Power BI Desktop if you do not already have them.
2. Download or clone this GitHub repository, then open PowerShell in the repository's top-level folder—the folder containing `README.md`, `scripts`, `sql`, and `outputs`.
3. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

   The requirements install DuckDB for Parquet/SQL work and OpenPyXL for writing the Excel workbook. If PowerShell blocks virtual-environment activation, use the Python executable directly: `.\.venv\Scripts\python.exe`.

4. Create the local raw-data folder:

   ```powershell
   New-Item -ItemType Directory -Force work\data\raw\delivery | Out-Null
   ```

   `work/` is local storage and is excluded from Git. Keep your source files there.

## 4. Download Jilin first, then inspect the actual file

On the Hugging Face files page, choose the Jilin Parquet delivery shard. At the time this guide was written, the official filename was `delivery_jl-00000-of-00001-a4fbefe3c368583c.parquet`. Download it directly into the project folder with PowerShell:

```powershell
$url = 'https://huggingface.co/datasets/Cainiao-AI/LaDe-D/resolve/main/data/delivery_jl-00000-of-00001-a4fbefe3c368583c.parquet'
$out = 'work\data\raw\delivery\delivery_jl-00000-of-00001-a4fbefe3c368583c.parquet'
Invoke-WebRequest -Uri $url -OutFile $out
Get-Item $out | Select-Object Name,Length
Get-FileHash $out -Algorithm SHA256
```

Compare the SHA-256 to the official file metadata when available. For the inspected Jilin file it was `ed0296b83d84f739bb91ab3d3cf1a430cf71e3793e25ddf50f88aa3ef34b51fc`. A file hash checks that your download matches the source file; it does not validate the meaning of the columns.

Create a small inspection script such as `work/inspect_jilin.py`:

```python
from pathlib import Path
import duckdb

file_path = Path(
    "work/data/raw/delivery/"
    "delivery_jl-00000-of-00001-a4fbefe3c368583c.parquet"
)
con = duckdb.connect()
data = con.read_parquet(str(file_path))

print("Columns:", data.columns)
print("Types:", data.types)
print("First five rows:")
print(data.limit(5).df().to_string(index=False))
print("Row count:", con.execute(
    "SELECT COUNT(*) FROM read_parquet(?)", [str(file_path)]
).fetchone()[0])
```

Run it from the repository root:

```powershell
python work\inspect_jilin.py
```

Look at the output before proceeding. The inspected files had 17 fields, including `order_id`, `city`, `region_id`, `courier_id`, `accept_time`, `delivery_time`, GPS fields, and `ds`. The timestamp strings have month/day/time but no year or timezone. Column names are clues, not enough proof of field meaning; compare the schema with the source card and keep uncertain definitions visible.

## 5. Expand to all five official delivery files

Download only the five Parquet delivery shards from the official LaDe-D `data` folder. At the time of inspection their filenames and SHA-256 values were:

| City | File | SHA-256 |
|---|---|---|
| Chongqing | `delivery_cq-00000-of-00001-465887add76aeabc.parquet` | `ea503be5d475aa9a3ceb27f09ce6f910f48a02e78122428fbb4f9c724820323b` |
| Hangzhou | `delivery_hz-00000-of-00001-8090c86f64781f71.parquet` | `00b6b4dca471cadee796a3fc7f07dcd919499ec58459ea67db784dcb06089e75` |
| Jilin | `delivery_jl-00000-of-00001-a4fbefe3c368583c.parquet` | `ed0296b83d84f739bb91ab3d3cf1a430cf71e3793e25ddf50f88aa3ef34b51fc` |
| Shanghai | `delivery_sh-00000-of-00001-ad9a4b1d79823540.parquet` | `a0561b186b924ffb6ac2612acbd8fd94ab75a752b3bd70276e5fa7b335a778f7` |
| Yantai | `delivery_yt-00000-of-00001-cc85c1fcb1d10955.parquet` | `2c5e5566ca8e4976e215822d8d5f3d5db157aba0dfe85a952b0cb357dee0ec5d` |

Use the files page for the current filenames and download links. These names may change if the source republishes the files. Download each into `work/data/raw/delivery/`, then run:

```powershell
$base = 'https://huggingface.co/datasets/Cainiao-AI/LaDe-D/resolve/main/data/'
$files = @(
    'delivery_cq-00000-of-00001-465887add76aeabc.parquet',
    'delivery_hz-00000-of-00001-8090c86f64781f71.parquet',
    'delivery_jl-00000-of-00001-a4fbefe3c368583c.parquet',
    'delivery_sh-00000-of-00001-ad9a4b1d79823540.parquet',
    'delivery_yt-00000-of-00001-cc85c1fcb1d10955.parquet'
)
foreach ($name in $files) {
    Invoke-WebRequest -Uri ($base + $name) -OutFile (Join-Path 'work\data\raw\delivery' $name)
}
```

This downloads approximately 290 MB across all five files. If a download fails or a filename has changed, use the current official files page rather than guessing a replacement URL.

```powershell
Get-ChildItem work\data\raw\delivery\delivery*.parquet
Get-FileHash work\data\raw\delivery\delivery*.parquet -Algorithm SHA256
```

The model-building script expects exactly five `delivery*.parquet` files in that folder. It also checks the city labels, so do not add unrelated files with a `delivery` prefix there.

## 6. Build and audit the local DuckDB models

First read [`sql/04_multicity_model.sql`](../sql/04_multicity_model.sql). It reads the five Parquet shards, provisionally attaches 2022 to the event timestamp strings, calculates elapsed minutes, and writes two local Parquet models:

- `work/data/staged/multicity_package_fact.parquet`: one row per package with source columns and audit flags.
- `work/data/staged/multicity_delivery_events.parquet`: two rows per package—one acceptance event and one completion event.

Run the Python driver:

```powershell
python scripts\build_multicity_models.py
```

Python is coordinating the job; DuckDB executes most of the data work in SQL. The script limits DuckDB to 1 GB memory and two threads. It checks that the five expected cities are present, package keys are unique at `(city, order_id)`, event rows total twice the package count, and each package has one event of each type. Expected summary: **4,514,661 package rows** and **9,029,322 event rows**. Three Chongqing rows have negative elapsed time with the provisional year. The script preserves and reports those anomalies rather than silently deleting them.

Useful beginner SQL examples you can run with Python/DuckDB after the models exist:

```python
import duckdb

con = duckdb.connect()
packages = "work/data/staged/multicity_package_fact.parquet"

# Count packages by city.
print(con.execute("""
    SELECT city, COUNT(*) AS packages
    FROM read_parquet(?)
    GROUP BY city
    ORDER BY city
""", [packages]).df())

# Find records that need date-semantic review.
print(con.execute("""
    SELECT city, COUNT(*) AS negative_intervals
    FROM read_parquet(?)
    WHERE accept_to_delivery_elapsed_minutes < 0
    GROUP BY city
""", [packages]).df())
```

Read [`scripts/build_multicity_models.py`](../scripts/build_multicity_models.py) beside the SQL file. The Python script loads the SQL statements, runs them, prints per-city medians and P90s, and stops if its structural checks fail.

## 7. Create aggregate tables for reporting

Run:

```powershell
python scripts\build_multicity_aggregates.py
```

This script groups the package model into three different grains (the meaning of “grain” is what one output row represents):

- `city_month.csv`: one row per city and acceptance month.
- `city_accept_hour.csv`: one row per city, acceptance month, and source acceptance hour.
- `city_region_month.csv`: one row per city, region code, and acceptance month.

Each table includes package counts and precomputed median/P90 interval fields. Hour and region-month groups under 200 packages are omitted as a small-volume screen. It is not a statistical significance test. The CSV files are written under `work/data/aggregates/`, not committed to Git.

Then create the import workbook:

```powershell
python scripts\export_multicity_excel.py
```

It writes `outputs/LaDe-PowerBI-aggregates.xlsx`. Open it in Excel and inspect the `ReadMe`, `CityMonth`, `AcceptanceHour`, and `RegionMonth` sheets. Excel is used here as a convenient handoff/inspection format; DuckDB did the large-table analysis.

## 8. Build the HTML preview

Run:

```powershell
python scripts\build_dashboard_preview.py
```

The Python script reads the three local aggregate CSVs, embeds only aggregate values in a standalone HTML file, and writes `outputs/LaDe-interactive-dashboard.html`. Open that file in a browser. Try the city and month filters and the median/P90 switches. Read [`scripts/build_dashboard_preview.py`](../scripts/build_dashboard_preview.py) to see the data-loading step; the HTML's embedded JavaScript filters the already-aggregated rows and draws the charts.

## 9. Inspect the Power BI report

Open `outputs/LaDe-Delivery-Reliability.pbix` in Power BI Desktop. The report file already exists in this repository. If rebuilding it yourself from the workbook:

1. Select **Get data → Excel workbook** and choose `LaDe-PowerBI-aggregates.xlsx`.
2. Select the `CityMonth`, `AcceptanceHour`, and `RegionMonth` sheets, then load.
3. Keep the aggregate tables disconnected unless you create a valid shared dimension. These tables have different grains; relating count metrics to each other creates misleading filter behavior.
4. Page 1 uses city/month median elapsed interval. Each city-month has one precomputed median, so taking the row's maximum returns that stored value; do not average monthly medians to claim an exact overall median.
5. Page 2 shows city, region code, acceptance month, median interval, and summed package count. Keep median and P90 columns from being summed.
6. Check titles, axes, filters, row counts, and the interpretation notes. Region IDs are codes, not verified neighborhood names.
7. Save as `outputs/LaDe-Delivery-Reliability.pbix`.

The current two-page report and its intended interpretation are described in [`outputs/PowerBI-dashboard-guide.md`](PowerBI-dashboard-guide.md). A Power BI Desktop license/service account is not needed to read the local PBIX in Desktop, but the report is not automatically a hosted web dashboard.

## 10. Publish responsibly with GitHub

Review `.gitignore` before committing. It excludes local raw/staged/aggregate data and database files under `work/`. Before pushing, inspect:

```powershell
git status --short
git check-ignore -v work\data\raw\delivery\delivery_jl-00000-of-00001-a4fbefe3c368583c.parquet
```

The second command should show that the raw file is ignored. Do not force-add it. Commit scripts, SQL, documentation, and reviewed aggregate-only portfolio outputs only after checking source terms and attribution. Review `outputs/GitHub-publishing-checklist.md` and `DATA-AND-CODE-NOTICE.md` before publishing changes. The public project is at <https://github.com/prabhubapani/lade-delivery-reliability>.

## 11. Files to study and what to learn from each

| File | Study it to understand |
|---|---|
| `sql/04_multicity_model.sql` | How source rows become package and event models; how dates and quality flags are derived. |
| `scripts/build_multicity_models.py` | How Python runs SQL and checks model counts and event composition. |
| `scripts/build_multicity_aggregates.py` | How `GROUP BY`, medians/P90s, counts, and the 200-package screen create report tables. |
| `scripts/export_multicity_excel.py` | How Python/OpenPyXL writes workbook sheets and formatted tables. |
| `scripts/build_dashboard_preview.py` | How aggregate CSVs become a self-contained HTML dashboard. |
| `outputs/LaDe-multicity-audit.md` | What was checked, what was found, and how to describe uncertainty. |
| `outputs/PowerBI-dashboard-guide.md` | What the two Power BI pages show and how to interpret them. |
| `outputs/Interview-walkthrough.md` | A short explanation and answers to common interview follow-ups. |

## 12. Practice plan

1. Run the Jilin inspection before downloading the other four files. Explain each column only after comparing it with source documentation.
2. Run the model script. Explain why package keys include both city and order ID, and why each package becomes two event rows.
3. Run the aggregate script. Explain what one row represents in each CSV and why you should not average precomputed percentiles.
4. Open the workbook, HTML preview, and PBIX. Explain one visual and one limitation from each.
5. Rehearse this answer: “The interval runs from recorded task acceptance to recorded task completion. It is not customer wait time or promised-delivery compliance. Dates are provisional because the source timestamps omit year and timezone.”

If your counts differ, stop and check that you downloaded exactly the five delivery Parquet shards, that all five share the inspected schema, and that no old or duplicate file is in `work/data/raw/delivery/`.

