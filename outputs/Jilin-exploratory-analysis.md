# Jilin exploratory analysis: acceptance-to-completion interval

**Status:** Exploratory only. This is one-city historical data, not an SLA or a final operations recommendation.

## Question

How does the elapsed time between the recorded task acceptance and task completion vary by the source acceptance-hour and source region code in the Jilin sample?

## Method

- Start from 31,415 package-grain rows in the local Jilin delivery subset.
- Parse the timestamp strings by provisionally attaching year 2022. The source strings omit year and timezone, so “hour” below means the hour shown in the source clock string; timezone has not been verified.
- Compute `accept_to_delivery_elapsed_minutes = delivery_time - accept_time`. This is a timestamp interval only. It is not proof of customer waiting time, an SLA, or an on-time measure.
- Report package count, median, and 90th percentile. For segment tables, require at least 200 packages per segment. This is a simple minimum-volume screen, not a statistical power guarantee.
- Keep zero-duration and long-duration rows in the analysis. No rows are dropped or imputed.

## Findings to investigate

| Source acceptance hour | Packages | Median minutes | 90th percentile minutes |
|---:|---:|---:|---:|
| 7 | 3,388 | 193.5 | 360.0 |
| 8 | 11,813 | 204.0 | 413.0 |
| 9 | 8,308 | 181.0 | 417.0 |
| 10 | 2,090 | 166.0 | 401.0 |
| 11 | 612 | 145.0 | 408.4 |
| 12 | 626 | 109.0 | 289.5 |
| 13 | 1,354 | 111.0 | 271.0 |
| 14 | 1,343 | 112.0 | 263.0 |
| 15 | 953 | 105.0 | 249.8 |
| 16 | 467 | 94.0 | 214.4 |
| 17 | 207 | 63.0 | 148.6 |

Packages are concentrated in source hours 8 and 9. The hourly medians and 90th percentiles are generally higher for acceptance hours 7–11 than 12–17. This is a descriptive association. It could reflect workload, task mix, routing, or other conditions not represented in the inspected fields; this data alone cannot identify a cause.

Across source region codes, code **165** has a higher 90th percentile than the other codes in each month May through September:

| Acceptance month (provisional 2022) | Region code 165 packages | Region 165 p90 minutes | Highest other-region p90 minutes |
|---:|---:|---:|---:|
| May | 474 | 608.0 | 319.7 |
| June | 698 | 474.6 | 403.1 |
| July | 730 | 449.0 | 354.0 |
| August | 827 | 495.4 | 410.0 |
| September | 698 | 415.0 | 388.0 |

This repeated upper-tail pattern is a **lead for further investigation**, not evidence that the region caused longer delivery intervals. The source provides no region-name lookup, route/capacity details, or demand mix. October is unsuitable for this comparison in the current sample: it has only 1,089 total rows, 23 active dates, and no rows for region codes 53 or 165. Empty dates may represent no Jilin package rows; we cannot classify them as missing records without source context.

## Limits and safe interpretation

- These observations cover Jilin only and describe 2022 China operations. They do not establish patterns in other LaDe cities or in India.
- The source `ds` key is documented as a delivery date but matches the acceptance date in all 31,415 Jilin rows. Analysis dates here come from the acceptance timestamp, not `ds`.
- No promised delivery deadline/SLA or customer review field is present in the inspected schema. Do not translate an interval threshold into a “late” or customer-satisfaction KPI.
- The source region and AOI codes are identifiers, not human-readable areas. No category names have been inferred.
- The smallest accepted segment has 207 records. Continue with uncertainty checks and held-out date comparisons before presenting a finding as stable.

## Next analysis step

Check whether the hourly and region-code patterns hold when split by date periods and whether the region 165 upper tail remains visible after reviewing the long-duration and zero-duration records. Then decide if the definitions and coverage are solid enough to add a second city. Do not yet make an operational intervention recommendation.

