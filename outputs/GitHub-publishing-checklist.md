# GitHub publishing checklist

## Repository summary

**Suggested repository name:** `lade-delivery-reliability`  
**Description:** `A Python, DuckDB, SQL, and Power BI portfolio project auditing historical LaDe-D last-mile delivery data from five Chinese cities.`  
**Topics:** `data-analysis`, `duckdb`, `sql`, `power-bi`, `last-mile-delivery`, `data-quality`, `portfolio-project`

## Before the first push

- Recheck the [LaDe-D dataset card](https://huggingface.co/datasets/Cainiao-AI/LaDe-D), its linked research-use terms, and the [LaDe project README](https://github.com/wenhaomin/LaDe). Confirm that the README's attribution and research-use statement are appropriate for the intended public repository.
- Keep raw parquet files, staged package/event data, and all local DuckDB files out of Git. The project `.gitignore` excludes `work/` and Power BI's local settings/cache files.
- Review the aggregate workbook and any screenshots. They must contain no `order_id`, `courier_id`, package-level records, or raw-data snippets.
- Keep the China and 2022 caveats prominent. Don't imply customer satisfaction, SLA compliance, causality, or transferability to Indian delivery operations.
- Do not add an open-source license until the project code's license choice is deliberate. The dataset's license metadata does not automatically license this project's code or the source data.
- Confirm there are no credentials or personal details in files, Git configuration, or commit history.

## GitHub connection and destination

The local project is initialized and its code/documentation files are staged, but no commit identity or remote repository is configured. Connect the GitHub integration and provide the destination repository (or confirm the exact name and visibility if a new repository should be created) before publishing. Do not push the raw data directory.

## Suggested first commit

`Build LaDe-D delivery operations portfolio project`

