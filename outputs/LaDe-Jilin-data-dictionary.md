# LaDe-D Jilin delivery sample: data dictionary

## Source and scope

- **Source:** [Cainiao-AI LaDe-D on Hugging Face](https://huggingface.co/datasets/Cainiao-AI/LaDe-D); source documentation in the dataset card and [LaDe project README](https://github.com/wenhaomin/LaDe).
- **Local sample:** One Jilin delivery shard, `delivery_jl-00000-of-00001-a4fbefe3c368583c.parquet` (2,271,457 bytes), downloaded 2026-10-26. SHA-256: `ed0296b83d84f739bb91ab3d3cf1a430cf71e3793e25ddf50f88aa3ef34b51fc`. It matches the file hash listed by the Hugging Face dataset repository.
- **Use:** The project README says research purposes. Keep raw data local; publish code and aggregated findings only, with attribution. The Hugging Face card labels the repo Apache-2.0 but also asks users to read “these terms”; a separate terms document was not exposed on the card when checked. Recheck before public release.
- **Sample grain:** One row per observed `order_id` in this Jilin shard (31,415 rows and 31,415 distinct IDs). The source describes a package identifier, but calls it `package_id`; this shard uses `order_id`. Treat package/order equivalence as likely but unresolved. Each row holds package attributes plus accept and delivery event fields. It is not yet a normalized one-row-per-event table.
- **Date assumption:** Timestamp strings omit year and timezone. Parsing with year 2022 is provisional, based on the overall dataset period documented as 2022-05-01 through 2022-10-31.

## Field definitions

“Source definition” summarizes the dataset card. “Observed in Jilin” reports what is present in this single shard. A documented label does not resolve discrepancies or establish causal/business meaning.

| Field | Observed type | Source definition | Observed in Jilin | Status / handling |
|---|---|---|---|---|
| `order_id` | BIGINT | Card prose identifies `package_id` as unique package ID. | 31,415 non-null, unique values. | **Naming unresolved:** preserve `order_id`; do not silently rename to `package_id`. Check other city files before unioning. |
| `region_id` | BIGINT | Region identifier. | Four distinct codes; values range 31–165. | **Documented ID, mapping unknown:** do not infer region names. |
| `city` | VARCHAR | City. | Every row is `Jilin`. | **Documented and observed.** |
| `courier_id` | BIGINT | Courier identifier. | 57 distinct, no nulls. | **Documented ID:** no personal identity or courier attributes provided by this field. Do not publish row-level courier findings. |
| `lng`, `lat` | DOUBLE | Coordinates of the stop. | No nulls; longitude 126.41956–126.81905, latitude 43.68460–44.22335. | **Documented, interpretation provisional:** values look like longitude/latitude degrees and fall within broad geographic ranges. CRS and exact stop meaning need confirmation. |
| `aoi_id` | BIGINT | Area-of-interest (AOI) identifier. | 1,259 distinct values, no nulls. | **Documented ID, spatial mapping unknown.** |
| `aoi_type` | BIGINT | Categorical AOI type. | 14 observed codes: 0–5 and 7–14; no nulls. | **Category meanings unresolved:** the card does not provide a code lookup in the inspected material. Keep as codes. |
| `accept_time` | VARCHAR | Time courier accepts the task. | Format `MM-DD HH:MM:SS`; no nulls; parses under provisional 2022 assumption. | **Documented event, date context unresolved:** no year or timezone in the string. |
| `accept_gps_time` | VARCHAR | GPS point time closest to acceptance. | Non-null and exactly equal to `accept_time` in all 31,415 rows. | **Documented and observed:** equality in this shard does not guarantee equality in other cities. |
| `accept_gps_lng`, `accept_gps_lat` | DOUBLE | Coordinates associated with courier acceptance. | Both missing together in 955 rows (~3.0%); no partial pairs. | **Documented, coordinate meaning provisional:** absent GPS coordinates should remain missing, not be imputed without a rule. |
| `delivery_time` | VARCHAR | Time courier finishes the delivery task. | Format `MM-DD HH:MM:SS`; no nulls; parses under provisional 2022 assumption. | **Documented event, date context unresolved:** no year or timezone in the string. |
| `delivery_gps_time` | VARCHAR | GPS point time closest to delivery completion. | Non-null and exactly equal to `delivery_time` in all 31,415 rows. | **Documented and observed** in this shard. |
| `delivery_gps_lng`, `delivery_gps_lat` | DOUBLE | Coordinates associated with delivery completion. | No missing pairs; values pass broad longitude/latitude range checks. | **Documented, coordinate meaning provisional:** no CRS or exact matching tolerance provided. |
| `ds` | BIGINT | Card says date of package delivery. | Integer values look like `MDD` (e.g. 925). All 31,415 values match the month/day in `accept_time`; 31,396 match `delivery_time`. Nineteen delivery timestamps are on a later calendar date. | **Unresolved discrepancy:** preserve as source date key; do not treat as verified delivery date or use for delivery-date analysis until clarified. |

## First-pass audit results

- **Keys and missingness:** no duplicate or null `order_id`; no null city, region, courier, AOI fields, stop coordinates, or accept/delivery time fields. Accept-GPS coordinates are missing as a pair on 955 rows. Delivery-GPS coordinates are complete.
- **Dates:** 163 distinct `ds` dates observed. There are no Jilin rows on 21 calendar dates in the overall six-month period. Seven of those dates fall between the first and last observed dates; the others are before the first observed Jilin date (2022-05-12) or after the last (2022-10-28). No-row dates are not automatically missing records; they may have had no Jilin deliveries.
- **Event order and duration:** under provisional 2022 parsing, no accept/delivery timestamps failed to parse, no acceptance occurs after delivery, 50 rows have zero-minute elapsed time at source precision, 1,417 exceed eight hours, and eight exceed 24 hours. Median elapsed time is 175 minutes; 95th percentile 469 minutes; maximum 3,573 minutes. These are descriptive intervals from task acceptance to completion, not SLA compliance or measured customer experience.
- **Cross-date rows:** 19 delivery timestamps fall on a later calendar date than `ds` (17 by one date, two by two dates). The two longest intervals are 2,948 minutes and 3,573 minutes. Their GPS event times match the task timestamps, so the long spans are not explained by an observed GPS timestamp mismatch. Keep them for review; do not automatically discard or label them errors.
- **Geography and codes:** one city, four region IDs, 57 couriers, 1,259 AOIs. Stop coordinates pass broad longitude/latitude range checks. No region boundaries, AOI lookups, or AOI type definitions were available in the inspected source card, so no code labels or spatial performance explanations are assigned.

## Analysis rules until uncertainties are resolved

1. Keep source fields unchanged and retain a separate documented, cleaned layer.
2. Build event timestamps from `accept_time` and `delivery_time` with an explicit provisional 2022 year; do not derive delivery dates from `ds` yet.
3. Name their difference `accept_to_delivery_elapsed_minutes` rather than “SLA time,” “late delivery,” or “customer wait” until the intended population and operational definition are verified.
4. Keep zero-duration, cross-date, long-duration, and missing-GPS rows flagged for review; do not silently drop or impute them.
5. No customer reviews or promised delivery deadline are present in this shard. Do not claim measured customer satisfaction or on-time performance.
6. Recheck schema and meanings before combining more cities. Do not publish raw rows or courier-level results.

## Local derived models

The first model build is reproducible with `python scripts/build_jilin_models.py` after installing `requirements.txt` and placing the source shard at the documented local path. The model SQL is in `sql/02_jilin_model.sql`.

- `jilin_package_fact.parquet`: 31,415 rows, one per source `order_id`; preserves source columns and adds provisional parsed timestamps, elapsed minutes, and review/date comparison flags.
- `jilin_delivery_events.parquet`: 62,830 rows, exactly two per source order. Event types are `task_accepted` and `delivery_task_finished`, 31,415 each. It preserves raw timestamp text, provisional parsed times, GPS times/coordinates, the source `ds` key, and package context.
- Validation passed: every source order has exactly one event of each type; no event/package timestamps failed the provisional parse; and GPS timestamps equal their associated event timestamps in this Jilin file.
- Local aggregate tables are generated for acceptance hour, region-by-month, and region-by-hour. Groups below 200 packages are omitted. Preliminary results and caveats are in the [Jilin exploratory analysis](Jilin-exploratory-analysis.md).

Both derived Parquet files are local, ignored by Git, and reproducible from the source file. The checks confirm shape and timestamp parsing, not business meaning or SLA compliance.

