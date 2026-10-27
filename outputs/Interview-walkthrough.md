# Interview walkthrough: delivery operations audit

## 30-second version

“I built a local analytics workflow around Cainiao-AI’s LaDe-D delivery data. I started by checking the research-use terms and inspecting a single city before scaling to five. Python and DuckDB helped me audit the actual schema, validate keys and timestamps, build package- and event-level models, and create aggregate-only tables for Power BI. A key finding was a data-definition mismatch: the source says `ds` is a delivery date, but the values align much more closely with acceptance dates. I kept the uncertainty visible instead of silently changing the field. The results describe historical Chinese operations and do not measure customer satisfaction or SLA compliance.”

## 2-minute structure

1. **Question:** How do observed acceptance-to-task-completion intervals vary across city, month, and source acceptance hour?
2. **Scope:** Five city delivery shards, 4.51 million rows, May–October 2022 as described by the source, with some observed dates outside that window. It is historical China data, not Indian market evidence.
3. **Process:** Reviewed research-use guidance; downloaded one city first; inspected schema and data quality; expanded only after confirming common schema; built local DuckDB package/event models; produced aggregate-only CSVs for a Power BI report.
4. **Quality:** Within-city order IDs are unique; the final event model has exactly two events per package. Timestamp strings omit year/timezone. `ds` aligns mostly with acceptance dates, not the documented delivery date. Three Chongqing rows become negative under the provisional year assignment; these remain flagged rather than repaired by guesswork.
5. **Analysis:** City medians range from 72 to 208 minutes and P90s from 211 to 496 minutes under provisional parsing. Long intervals remain included. These are descriptive comparisons, not a city performance verdict.
6. **Decision:** Show medians and upper-tail percentiles with sample counts, add data-quality context, avoid unsupported “late/on-time” labels, and recommend clarifying date semantics before operational decisions.

## Likely follow-ups

**Why not call this on-time delivery?** There is no promised delivery time or SLA field, so elapsed duration cannot tell whether a package met a commitment.

**Why trust the provisional elapsed time?** It is useful for exploration but not fully verified. The model labels the attached year as provisional, retains source strings, flags negative and long rows, and documents that timezone is unknown.

**Why did you keep very long durations?** Automatic deletion would hide a data-quality or process issue and bias the distribution. I keep them, report robust percentiles, and call for source-semantic review.

**What does `ds` mean?** The card calls it a delivery date, but observed values match acceptance dates far more often. I preserve the source value and avoid using it as the verified completion date.

**Can this tell us customer satisfaction?** No. There are no review or satisfaction fields.

**Can this guide an Indian delivery business?** It demonstrates analytical methods, not direct market transfer. The data is historical and Chinese; India-specific conclusions require local data.

**How would you improve it with source-owner access?** Confirm ID scope, year rollover, timezone, `ds` semantics, region/AOI codebooks, delivery promise definitions, and whether these rows cover all deliveries or a sample; then validate the model and KPI definitions with the operations owner.

