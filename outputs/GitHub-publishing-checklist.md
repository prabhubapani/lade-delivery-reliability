# GitHub publishing checklist

## Repository

**Repository:** [prabhubapani/lade-delivery-reliability](https://github.com/prabhubapani/lade-delivery-reliability)  
**Visibility:** Public  
**Description:** `A Python, DuckDB, SQL, and Power BI portfolio project auditing historical LaDe-D last-mile delivery data from five Chinese cities.`

## Published project materials

- Python profiling, modeling, aggregate-export, and interactive preview scripts.
- SQL models and project documentation, including the multi-city audit, field dictionary, and interview walkthrough.
- Reviewed aggregate-only CSV/workbook outputs, HTML preview, and the native Power BI `.pbix` report.
- No raw parquet shards, package/event-level records, or local DuckDB database files. Keep those in ignored `work/` storage.

## Data use and interpretation

- Review the [LaDe-D dataset card](https://huggingface.co/datasets/Cainiao-AI/LaDe-D), linked terms, [LaDe project README](https://github.com/wenhaomin/LaDe), and [data/code notice](../DATA-AND-CODE-NOTICE.md) before reuse. Source statements conflict; this is a free educational portfolio and raw data is not redistributed.
- The data is historical and from China (2022). It is not a proxy for Indian operations.
- The inspected schema has no customer reviews, promise deadline, or SLA field. Do not claim measured customer satisfaction or on-time/SLA compliance.
- The source states May–October 2022, while some timestamps fall outside that interval. Year 2022 is assigned provisionally and timezone is undocumented.
- Do not add an open-source license until the project's code-license choice is deliberate. Dataset metadata does not automatically license project code or source data.

## Account email privacy

GitHub's “Keep my email addresses private” setting is enabled. New GitHub web/API commits use the account's `users.noreply.github.com` address. The first public commit predates that setting and retains the primary email in historical author metadata. The setting does not rewrite old commits. Rewriting history may affect existing clones and links.

