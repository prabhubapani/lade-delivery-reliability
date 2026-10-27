# LaDe Last-Mile Delivery Reliability: project brief

## Goal

Build one advanced, interview-ready Data Analyst / BI portfolio project from Cainiao-AI's public LaDe delivery data, focusing on delivery reliability and operational performance from event-level package records. The work uses Python for profiling/cleaning, DuckDB and SQL for local modeling, Power BI Desktop for aggregate dashboards, and GitHub for code/documentation publishing.

The original planning estimate was **5–6 weeks at 8–10 hours per week**: source review and one-city audit; multi-city profiling and model; operational analysis; Power BI dashboard; then documentation, interview preparation, and repository review.

## Dataset and responsible use

LaDe is a historical Chinese delivery dataset. The source overview describes approximately 10.7 million packages, around 21,000 couriers, five Chinese cities, and the period 2022-05-01 through 2022-10-31. This portfolio analysis uses the five official delivery city shards (4,514,661 rows in the inspected files), not a claim that these shards cover every package in LaDe. Timestamp fields omit year and timezone. Observed timestamps extend outside the documented period, so year 2022 is provisional.

The dataset card marks the repository Apache-2.0 and also refers readers to research-use terms; the LaDe project README describes research use. Keep raw data local and excluded from Git. Recheck terms and attribution before publishing any derived output. No raw data should be redistributed.

There are no customer reviews, promised deadlines, or verified SLA fields in the inspected delivery schema. Do not claim measured customer satisfaction or on-time performance. The source says `ds` is a delivery date, but the observed values match acceptance dates more often; retain the field and show the mismatch.

## Completed work

1. Reviewed source terms and started with one Jilin delivery shard.
2. Inspected the actual 17-column schema and first-city quality before expansion.
3. Downloaded the remaining four city delivery shards and checked local file sizes and SHA-256 hashes against the official dataset listing.
4. Confirmed all five schemas match; built a city-qualified package fact and two-row event model in DuckDB.
5. Found per-city `order_id` uniqueness and no timestamp parse failures under provisional year 2022. Three Chongqing records become negative elapsed time under that assumption; they remain flagged and unmodified.
6. Built aggregate-only CSVs for city/month, city/source-acceptance-hour, and city/region/month. No order IDs or courier IDs are included.
7. Wrote the five-city audit, Power BI dashboard guide, and interview walkthrough.
8. Created an Excel workbook with three aggregate-only sheets for a one-step Power BI import.

## Core exploratory metric

`accept_to_delivery_elapsed_minutes` is the interval from recorded task acceptance to recorded task completion, computed from timestamp strings after provisionally adding 2022. It is not proven customer wait time, a promise-based SLA, or an on-time indicator. Retain zero, long, and negative records with quality flags; do not silently remove or repair.

## Portfolio deliverables

- Root README and reproducible Python/DuckDB scripts.
- Five-city audit report and source integrity record.
- Power BI-ready aggregate CSVs and [aggregate workbook](LaDe-PowerBI-aggregates.xlsx), plus the dashboard build guide.
- Interview narrative that explains the analytical question, modeling choices, audit issue, limits, and next source-owner questions.
- GitHub-ready code and documentation; raw source, staged model data, and aggregate CSVs remain ignored by Git pending terms/attribution review.

## Remaining steps to call the project complete

- Import the three sheets from `outputs/LaDe-PowerBI-aggregates.xlsx` in Power BI Desktop, then build and visually review a `.pbix`.
- Check the rendered visuals for counts, labels, filters, and caveats.
- Review Git ignore behavior and repository contents; initialize a local repository if desired.
- Recheck dataset terms and attribution before any public release. Do not publish raw data.

