# Power BI dashboard build guide

## Import the prepared aggregate workbook

In Power BI Desktop, cancel the open Text/CSV dialog, then choose **Home → Excel workbook** and open `outputs/LaDe-PowerBI-aggregates.xlsx`. In Navigator, select the three aggregate sheets: `CityMonth`, `AcceptanceHour`, and `RegionMonth`.

These sheets contain aggregate-only metrics. Do not load raw package or courier rows into a public report. Keep the model local until terms and attribution have been rechecked.

## Page 1: Delivery interval overview

- KPI cards: package count and over-24-hour interval rate. Show median and P90 on the grouped chart, not as all-period KPI cards.
- Line chart from `CityMonth`: `accept_month` on X; median and P90 elapsed minutes as values; `city` as legend. Put package count in the tooltip.
- Avoid an all-period city ranking from the precomputed percentiles; those aggregates cannot be combined into an exact full-period P90.
- Add a visible note: “Historical LaDe-D data from China (2022); acceptance-to-task-completion interval; timestamp year provisionally set to 2022; not SLA/on-time or customer satisfaction.”

## Page 2: Operating pattern exploration

- Matrix or line chart from `AcceptanceHour`: source acceptance hour by city, with median/P90 and package count. Use city and month slicers.
- Use `RegionMonth` for a region-code matrix by month. Label region as **region_id**, not a neighborhood name.
- Groups below 200 have already been omitted from these segment files. Display a note that this is a volume screen, not a statistical guarantee.

## Suggested measures

For the city/month table, a package-weighted rate is valid across the selected rows:

```DAX
Packages = SUM(CityMonth[package_count])
Over 24h rate = DIVIDE(SUM(CityMonth[over_24h_count]), [Packages])
```

Use the precomputed median and P90 columns within the city/month, city/hour, or city/region/month group shown on the visual. Do not average monthly medians or group P90 values to claim an exact all-period percentile. If you need an overall percentile, calculate it from the local package fact in DuckDB and expose only the aggregate result.
## Visual and interpretation checks

- Avoid red/green “late/on-time” labels; no deadline is in the data.
- Show the package count next to every percentile so small groups are visible.
- Filter out incomplete or anomalous dates only with a written rule. Keep negative elapsed count visible as a data-quality indicator.
- Do not interpret source clock hours as local time until timezone is documented.
- Do not present the city ranking as causal or as a current India benchmark.
- Save a `.pbix` only after visual review. Publish screenshots/PDF and aggregate CSVs only after terms/attribution review; never include raw shards.


