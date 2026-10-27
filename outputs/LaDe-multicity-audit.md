# LaDe-D five-city delivery audit

**Status:** Local analysis completed; dashboard and publication review remain. **Data period:** Historical source release described as May–October 2022 in China. Timestamp strings omit year and timezone, and observed rows include dates outside that description. Treat all parsed calendar dates as provisional.

## Source terms and handling

The [LaDe-D dataset card](https://huggingface.co/datasets/Cainiao-AI/LaDe-D) labels the repository Apache-2.0 while also instructing users to read research-use terms. The [LaDe project README](https://github.com/wenhaomin/LaDe) describes the dataset as for research use. I did not find a separately linked terms document on the card at review time. This project keeps all downloaded parquet source files local and ignored by Git; only code, documentation, and non-identifying aggregates are candidates for publication. Recheck source terms and attribution immediately before publication. Do not upload or redistribute raw data.

## Downloads and integrity

Five official delivery shards were downloaded individually from the dataset's [data directory](https://huggingface.co/datasets/Cainiao-AI/LaDe-D/tree/main/data). Local byte sizes and SHA-256 values match the Hugging Face dataset API listing at time of download.

| File | Bytes | SHA-256 |
|---|---:|---|
| `delivery_cq-00000-of-00001-465887add76aeabc.parquet` | 61,844,340 | `ea503be5d475aa9a3ceb27f09ce6f910f48a02e78122428fbb4f9c724820323b` |
| `delivery_hz-00000-of-00001-8090c86f64781f71.parquet` | 116,465,564 | `00b6b4dca471cadee796a3fc7f07dcd919499ec58459ea67db784dcb06089e75` |
| `delivery_jl.parquet` (source shard retains official Jilin identity) | 2,271,457 | `ed0296b83d84f739bb91ab3d3cf1a430cf71e3793e25ddf50f88aa3ef34b51fc` |
| `delivery_sh-00000-of-00001-ad9a4b1d79823540.parquet` | 94,841,102 | `a0561b186b924ffb6ac2612acbd8fd94ab75a752b3bd70276e5fa7b335a778f7` |
| `delivery_yt-00000-of-00001-cc85c1fcb1d10955.parquet` | 14,807,092 | `2c5e5566ca8e4976e215822d8d5f3d5db157aba0dfe85a952b0cb357dee0ec5d` |

## Actual schema and key checks

All five files have the same 17 columns and types: `order_id` BIGINT, `region_id` BIGINT, `city` VARCHAR, `courier_id` BIGINT, `lng`/`lat` DOUBLE, `aoi_id`/`aoi_type` BIGINT, accept and delivery event/GPS times VARCHAR, GPS coordinate pairs DOUBLE, and `ds` BIGINT. Each city has one observed city label, no null/duplicate `order_id`, and no null acceptance or completion timestamps. Every timestamp parsed with the provisional year 2022. Source strings contain month/day/time but no year or timezone.

Across all cities, key fields (`order_id`, `city`, `region_id`, `courier_id`, stop coordinates, AOI fields, and task timestamps) have no nulls. Coordinates pass broad longitude/latitude range checks; this does not validate the coordinate reference system. Acceptance GPS coordinates are absent as a complete pair for 955 Jilin rows and 2,422 Yantai rows; no partial pairs occur. Other cities have complete acceptance GPS pairs, and all delivery GPS coordinate pairs are complete. AOI type counts range from 14 to 16 codes by city; their meanings remain undocumented.

The source card says `ds` is a delivery date. In every city `ds` matches the acceptance date more often than the completion date; it is not safe to use `ds` as a verified delivery date. The values are numeric `MDD`-style keys (for example 501, 1031), not full dates. Keep the original value and use acceptance timestamps only for provisional time grouping.

## Per-city results

Elapsed minutes are calculated from acceptance to task completion after attaching year 2022. Negative and long intervals remain in the data. These are task-time intervals, not SLA or customer-wait measures.

| City | Packages | Couriers* | Median min | P90 min | `ds` matches acceptance | `ds` matches completion | Later calendar date | Over 24 hours | Negative intervals |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Chongqing | 931,351 | 1,494 | 151 | 488 | 931,338 | 890,154 | 41,183 | 31,231 | 3 |
| Hangzhou | 1,861,600 | 1,392 | 115 | 303 | 1,861,597 | 1,846,785 | 14,812 | 11,123 | 0 |
| Jilin | 31,415 | 57 | 175 | 387 | 31,415 | 31,396 | 19 | 8 | 0 |
| Shanghai | 1,483,864 | 1,733 | 72 | 211 | 1,483,864 | 1,477,690 | 6,174 | 3,578 | 0 |
| Yantai | 206,431 | 205 | 208 | 496 | 206,431 | 203,444 | 2,987 | 2,650 | 0 |

\*Courier counts are distinct IDs within each city; do not sum them as globally unique people because ID scope is not documented.

Total: **4,514,661 package rows**, **9,029,322 event rows** (one acceptance and one task-completion event per city-qualified package). Order IDs are unique within each city; the model keys packages as `(city, order_id)` because global ID uniqueness has not been established. Model checks passed for row counts, timestamp parseability, and exactly two event records of the expected type per package.

## Audit issues that shape interpretation

- Provisional acceptance dates run beyond the overall period described in the source: Chongqing includes two records in November/December; completion dates extend to December in Chongqing and Hangzhou. The source date range therefore does not fully describe observed timestamps, or the date semantics need clarification.
- Chongqing has three negative durations where October acceptance is paired with January completion when both are assigned 2022. Do not infer the correct year. Flag them and exclude from elapsed-time measures only if an explicit, documented rule is approved later.
- Long elapsed times are common enough to matter: each city has rows over 24 hours. Keep them and use robust percentiles alongside medians; do not silently trim.
- In Chongqing, 41,183 rows have a completion timestamp on a later calendar date than the provisional acceptance timestamp. This is not necessarily an error; it is a prompt to verify task-date semantics and source coverage.
- Region and AOI values are codes without verified labels. Do not invent geography or explain performance through unsupported maps.
- There are no customer reviews, promised deadlines, or service-level target fields. This project measures neither customer satisfaction nor on-time compliance.

## Files built locally

- Package model: `work/data/staged/multicity_package_fact.parquet` (source columns plus provisional parsed fields, elapsed minutes, comparison flags).
- Event model: `work/data/staged/multicity_delivery_events.parquet` (two event rows per package).
- Aggregate-only CSVs for Power BI: `city_month.csv`, `city_accept_hour.csv`, `city_region_month.csv` under `work/data/aggregates/`. Hour and region/month groups below 200 packages are omitted. These contain no order or courier IDs and are ignored by Git along with all raw/staged data.
- Rebuild: `python scripts/build_multicity_models.py`, then `python scripts/build_multicity_aggregates.py` after installing `requirements.txt` and putting the five source files in `work/data/raw/delivery/`.

## Responsible takeaway

The city-level medians range from 72 to 208 minutes and upper-tail percentiles also vary, but this is a descriptive comparison across historical Chinese city subsets with data-date issues. It does not show which city is “best,” establish causes, demonstrate reliability against a promise, or transfer directly to Indian delivery operations. A defensible interview story is the audit and modeling process, plus the decision to expose data limitations before building KPIs.


