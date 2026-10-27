# Last-Mile Delivery Reliability: LaDe-D Operational Audit

A portfolio project for entry-level Data Analyst / BI roles. It uses Cainiao-AI's LaDe-D delivery event data to demonstrate data profiling, SQL modeling, operational analysis, and Power BI reporting.

## Project question

How do observed package acceptance-to-task-completion intervals vary across the five city subsets and by source acceptance month/hour, and which data-quality issues must be resolved before using them as operational KPIs?

## Scope and responsible use

- Data: five official city delivery shards, 4,514,661 package/order rows from five Chinese cities.
- The dataset is historical. The source describes an overall period of May–October 2022, while this audit found timestamps outside that window. Timestamp strings omit year and timezone; 2022 is attached provisionally for exploration.
- The LaDe-D Hugging Face card labels the data Apache-2.0, while the original paper's datasheet describes CC BY-NC 4.0 and the project README says the data can be used for research. This repository does not redistribute raw shards. See [DATA-AND-CODE-NOTICE.md](DATA-AND-CODE-NOTICE.md) for attribution and the unresolved terms discrepancy.
- No customer reviews, promised delivery deadline, or SLA field is present in the inspected schema. This project does not measure satisfaction or on-time compliance.
- `ds` is documented as a delivery date, but observed values match acceptance dates more often. It remains an unresolved source field and is not treated as verified delivery date.

## Findings

- All five shards share the same 17-column schema; each city's `order_id` is unique within that city.
- The local model has 4,514,661 package rows and 9,029,322 event rows (acceptance and task completion per package).
- The provisional city median intervals range from 72 to 208 minutes; P90 ranges from 211 to 496 minutes. These are descriptive interval summaries, not city performance ratings.
- Three Chongqing records produce negative intervals under the provisional same-year parse, and timestamps extend beyond the documented period. These anomalies remain visible for source clarification.

Download the [interactive aggregate-only dashboard preview](outputs/LaDe-interactive-dashboard.html) and open it locally in a browser. Read the [five-city audit](outputs/LaDe-multicity-audit.md), [Power BI dashboard guide](outputs/PowerBI-dashboard-guide.md), and [interview walkthrough](outputs/Interview-walkthrough.md) for methods and interpretation limits. The earlier [project brief](outputs/marketplace-delivery-project-brief.md) records the original scope and workflow, and the [Jilin dictionary](outputs/LaDe-Jilin-data-dictionary.md) documents the first-city schema inspection.

This is a free educational portfolio project. Its historical Chinese delivery data is not a proxy for Indian operations. Review the source terms before adapting the analysis for commercial use.

## Rebuild locally

1. Review the [LaDe-D dataset card](https://huggingface.co/datasets/Cainiao-AI/LaDe-D), [data files](https://huggingface.co/datasets/Cainiao-AI/LaDe-D/tree/main/data), and [LaDe project README](https://github.com/wenhaomin/LaDe). Follow the source terms and keep raw data out of Git.
2. Put the five delivery parquet shards under `work/data/raw/delivery/`.
3. Install dependencies with `python -m pip install -r requirements.txt`.
4. Build local package/event models: `python scripts/build_multicity_models.py`.
5. Build aggregate-only Power BI CSV inputs: `python scripts/build_multicity_aggregates.py`.
6. Export the easy-import workbook: `python scripts/export_multicity_excel.py`.
7. Generate the offline dashboard preview: `python scripts/build_dashboard_preview.py`.
8. Follow [the Power BI guide](outputs/PowerBI-dashboard-guide.md) to recreate and visually review the report in Power BI Desktop. The HTML preview is not a native `.pbix`.

The SQL is in `sql/04_multicity_model.sql`. Local source, staged, and aggregate data are excluded from Git. The scripts set DuckDB to a 1 GB memory limit and two threads. The Power BI input workbook contains aggregate tables only.

## Technology

Python, DuckDB, SQL, Power BI Desktop, Git/GitHub, and a self-contained HTML preview built from aggregate tables. Raw and model data stay local; the public repository contains scripts, documentation, and reviewed aggregate outputs only.


