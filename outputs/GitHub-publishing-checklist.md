# GitHub publishing checklist

## Repository summary

**Repository:** [prabhubapani/lade-delivery-reliability](https://github.com/prabhubapani/lade-delivery-reliability)  
**Visibility:** Public  
**Description:** `A Python, DuckDB, SQL, and Power BI portfolio project auditing historical LaDe-D last-mile delivery data from five Chinese cities.`

## Published content and data boundary

- The repository contains project code, SQL, documentation, an aggregate-only workbook, and reviewed aggregate outputs.
- It does not contain raw parquet shards, package-level/event-level records, or local DuckDB databases. Keep them in ignored `work/` storage.
- Review the [LaDe-D dataset card](https://huggingface.co/datasets/Cainiao-AI/LaDe-D), its linked research-use terms, the [LaDe project README](https://github.com/wenhaomin/LaDe), and [DATA-AND-CODE-NOTICE.md](../DATA-AND-CODE-NOTICE.md) before reuse. The dataset card and original paper describe different terms; this project conservatively limits use to a free educational portfolio and does not redistribute source data.
- Keep the China and 2022 caveats prominent. The data is historical and does not represent Indian delivery operations.
- The inspected schema contains no customer reviews, promised delivery deadline, or SLA field. Do not claim measured satisfaction or on-time/SLA compliance.
- Do not add an open-source license until the project's code-license choice is deliberate. Dataset license metadata does not automatically license this project's code or source data.

## Account email privacy

GitHub's “Keep my email addresses private” setting is enabled. New GitHub web/API commits use the account's `users.noreply.github.com` address. The very first public commit predates that setting and retains the primary email in its historical author metadata. The setting does not rewrite old commits. If that email was sensitive, GitHub commit history can be rewritten, but it may affect clones and links to old commits.

## Remaining portfolio step

The repository is published, but a native Power BI `.pbix` was not created in this session. Use [PowerBI-dashboard-guide.md](PowerBI-dashboard-guide.md) with the aggregate workbook to build and visually review the two report pages in Power BI Desktop. Do not publish report screenshots or a `.pbix` until source-term and attribution review is complete.

