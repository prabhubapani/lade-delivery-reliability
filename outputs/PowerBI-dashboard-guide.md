# Power BI report guide

Open `LaDe-Delivery-Reliability.pbix` in Power BI Desktop. The report uses three prepared aggregate tables from `LaDe-PowerBI-aggregates.xlsx`; it does not contain raw package or courier event rows.

## Pages

### Page 1: Monthly delivery interval

The line chart shows the monthly median acceptance-to-task-completion interval by city. It uses the maximum aggregation of the precomputed median because each city has one row per month. The chart is filtered to source acceptance months 5–10 (May–October). A footer explains that the source contains some dates outside that range and that no SLA or customer satisfaction is measured.

### Page 2: Region-month detail

The table lists `city`, `region_id`, source `accept_month`, `median_elapsed_min`, and summed `package_count`. Region codes remain identifiers because the source does not supply verified neighborhood names here. The table retains available source months outside May–October, so interpret it alongside the documented date anomalies. Segment aggregates are volume screened: groups below 200 packages are omitted from the prepared segment files.

## Interpretation and limits

- LaDe-D is historical data from China in 2022, not a current Indian operations benchmark.
- The interval is acceptance-to-task-completion based on the inspected event schema. It is not delivery promise compliance or an SLA measure.
- There are no customer reviews; do not claim measured customer satisfaction.
- Timestamp year is assigned provisionally as 2022; timezone is undocumented. Source hour should not be described as local time.
- Some records fall outside the source's stated May–October window, and three elapsed intervals are negative under the provisional parse.
- Precomputed medians and P90s are valid for their displayed group only. Do not average group percentiles to claim an exact overall percentile.
- Package counts may be summed across distinct groups. For one row per city-month or city-region-month, use a non-summing aggregation for median/P90 fields.

## Source and data handling

Review the LaDe-D dataset card, original project README, and [`DATA-AND-CODE-NOTICE.md`](../DATA-AND-CODE-NOTICE.md) before reuse. Their licensing/use statements are inconsistent; the project is limited to a free educational portfolio and does not redistribute raw shards. The PBIX includes prepared aggregate tables only.

