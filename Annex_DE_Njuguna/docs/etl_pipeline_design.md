# Batch ETL Pipeline Design

## Objective

Design a repeatable batch pipeline that ingests the three ABC Phones sources and produces clean, analytics-ready tables for credit portfolio monitoring, customer enrichment, NPS analysis, and downstream reporting.

## Source Systems

| Source | File pattern | Grain | Primary key candidate | Load type |
|:--|:--|:--|:--|:--|
| Credit snapshots | `Credit Data/*.csv` | One row per `loan_id` per reporting snapshot | `loan_id`, `reporting_date` | Incremental snapshot append |
| Sales/customer workbook | `Sales and Customer Data.xlsx` | Multiple sheets: sales, gender, DOB, income | `loan_id` | Full refresh with deterministic deduplication |
| NPS workbook | `NPS Data (1).xlsx` | One survey submission per response | `submission_id`; analytical join on `loan_id` | Incremental append or full refresh depending on source delivery |

## Architecture

The pipeline follows a bronze/silver/gold pattern:

1. Source files are delivered to a raw landing area.
2. Ingestion validates file presence, schema, size, checksum, and expected naming.
3. Raw records are loaded into bronze tables with file metadata.
4. Cleaning and standardization create silver tables with typed columns, normalized IDs, deduplicated records, and validation flags.
5. Enrichment joins credit snapshots to DOB, income, sales, and NPS records by normalized `loan_id`.
6. Feature engineering creates required analytical fields.
7. Data quality checks gate publication to gold tables.
8. Analysts query gold tables/views partitioned by `reporting_date` and useful segments.

Architecture diagram: `pipeline_design/architecture.png`.

## Ingestion Strategy

### Credit Snapshots

- Use incremental append by `reporting_date` parsed from the filename.
- Expected cadence: daily or weekly in production; the case study uses supplied point-in-time snapshots.
- Natural uniqueness rule: one record per `loan_id` and `reporting_date`.
- Late-arriving snapshots are accepted if the snapshot date is new or if the file checksum changes for an existing date.
- Duplicate files are skipped when checksum and row count match a previously ingested source file.
- Reprocessed files are written as a new ingestion version and only promoted after validation passes.

### Sales and Customer Workbook

- Use full refresh because the workbook contains dimension-style sheets that may be corrected historically.
- Expected cadence: daily if maintained operationally; weekly is acceptable if source changes slowly.
- Each sheet is loaded independently into bronze tables.
- Deduplication is handled per sheet:
  - Sales Details: keep the most complete latest row per `loan_id` when a single sales dimension row is required.
  - DOB: keep the latest `createdat_utc` record per `loan_id`.
  - Income Level: aggregate repeated records by `loan_id`; sum income columns and keep the maximum duration.
  - Gender: keep the most frequent non-null gender/citizenship value per `loan_id` or latest record if a timestamp becomes available.

### NPS Workbook

- Prefer incremental append by `submission_id` and `submitted_at`.
- If the source arrives only as a full export, load it as full refresh into bronze and deduplicate by `submission_id`.
- Treat NPS as optional enrichment because not every credit customer will have a survey response.
- Preserve repeated survey responses per `loan_id`; create latest-response and aggregated-response views for analysts.

## Scheduling

| Task | Cadence | Reason |
|:--|:--|:--|
| File sensor and ingestion | Daily by 06:00 | Detect missing or malformed source files early. |
| Cleaning and silver transforms | After successful ingestion | Avoid publishing partial or invalid source updates. |
| Feature engineering | After silver transforms | Features depend on cleaned dates, IDs, income, arrears, and status fields. |
| Data quality checks | Before gold publication | Prevent bad data from reaching analysts. |
| Portfolio marts and BI extracts | Daily by 08:00 | Support daily portfolio monitoring and stakeholder reporting. |

## Transformation Logic

### Cleaning and Standardization

- Standardize column names to snake_case.
- Normalize `loan_id` values by trimming whitespace and using consistent string type.
- Parse date fields using explicit `pd.to_datetime(..., errors="coerce", utc=True)` where timezone values are possible.
- Parse numeric and currency fields after removing formatting characters.
- Preserve source file name, ingestion timestamp, reporting date, and source row number for lineage.
- Do not impute missing values during cleaning; create missingness flags and document treatment.
- Drop empty `unnamed_*` columns only when they have no data dictionary definition and all values are null.

### Deduplication Rules

| Table | Rule | Rationale |
|:--|:--|:--|
| Credit snapshots | Deduplicate by `loan_id`, `reporting_date`; keep latest ingestion version. | Snapshot grain should be unique by account and reporting date. |
| Sales Details | Deduplicate by `loan_id`; keep most complete/latest sales row. | Analysts need one primary sale record per credit account. |
| DOB | Deduplicate by `loan_id`; keep latest `createdat_utc`. | Later source records are more likely to reflect corrected identity data. |
| Income Level | Aggregate repeated `loan_id` rows. | Multiple rows appear to represent repeated income observations. |
| NPS | Deduplicate by `submission_id`; preserve repeated `loan_id` responses. | Multiple surveys per customer may be analytically meaningful. |

### Enrichment

- Join credit snapshots to sales/customer dimensions using normalized `loan_id`.
- Join DOB for `age_band`.
- Join income features for `avg_monthly_income_band`.
- Join NPS by `loan_id` for customer experience analysis, while retaining unmatched credit accounts.
- Build both latest-NPS and all-NPS views to support different analytical questions.

### Feature Engineering Automation

- `age_band`: calculate age from DOB as of `reporting_date`, then bucket.
- `avg_monthly_income_band`: sum income columns and divide by duration, then bucket.
- `days_past_due`: infer payment due date from source aging and reporting date; force 0 where arrears are 0.
- `risk_category`: combine account status, arrears, DPD, and payment pattern into Low, Medium, High, Critical.

Implemented logic: `scripts/feature_engineering.py`.

## Storage and Output Design

### Bronze Tables

- `bronze_credit_snapshot_raw`
- `bronze_sales_details_raw`
- `bronze_customer_gender_raw`
- `bronze_customer_dob_raw`
- `bronze_customer_income_raw`
- `bronze_nps_raw`
- `bronze_file_manifest`

Bronze tables are append-only and retain raw values plus lineage metadata.

### Silver Tables

- `silver_credit_snapshot_clean`
- `silver_sales_account`
- `silver_customer_demographics`
- `silver_customer_income`
- `silver_nps_response`
- `silver_data_quality_results`

Silver tables contain typed fields, normalized IDs, deduplicated dimensions, validation flags, and standardized categories.

### Gold Tables and Views

- `gold_credit_account_snapshot`: one row per `loan_id` and `reporting_date` with engineered features.
- `gold_portfolio_metrics_daily`: portfolio KPIs by reporting date.
- `gold_risk_segment_metrics`: risk metrics by age band, income band, status, and reporting date.
- `gold_credit_nps_customer_view`: credit outcomes joined to NPS outcomes.
- `gold_data_quality_dashboard`: latest quality check results and source freshness.

### Analyst Query Pattern

Analysts should query gold tables/views. Example:

```sql
SELECT
    reporting_date,
    risk_category,
    COUNT(*) AS account_count,
    AVG(CASE WHEN days_past_due > 0 THEN 1 ELSE 0 END) AS delinquency_rate
FROM gold_credit_account_snapshot
GROUP BY reporting_date, risk_category
ORDER BY reporting_date, risk_category;
```

### Partitioning Strategy

- Partition credit snapshot and portfolio metric tables by `reporting_date`.
- Cluster or index by `loan_id`, `risk_category`, `age_band`, and `avg_monthly_income_band`.
- Partition NPS by `submitted_at` month and cluster/index by `loan_id`.
- Retain ingestion version columns to support replay and rollback.

## Error Handling and Recovery

### Missing Source File

- Fail the ingestion task before transformations start.
- Record failure in `silver_data_quality_results`.
- Alert the data engineer and business stakeholder by email/Slack.
- Keep the previous gold tables available; do not publish partial outputs.

### Malformed Source File

- Quarantine the file in a rejected-source location with validation errors.
- Persist the parsing error, file name, checksum, and failing row/column where available.
- Stop downstream transforms for the affected source.
- Allow replay after the corrected file is delivered.

### Failed Data Quality Check

- Severity 1 checks, such as missing credit snapshot, broken schema, or severe referential integrity failure, block gold publication.
- Severity 2 checks, such as moderate null threshold drift, publish with warnings only if business-approved.
- Severity 3 checks, such as non-critical survey missingness, publish with report annotations.

### Consistency Controls

- Use a file manifest with source file name, checksum, row count, reporting date, load timestamp, and load status.
- Make transforms idempotent by writing partitioned outputs with replace-by-partition semantics.
- Promote gold tables only after all required silver tables and quality checks pass.
- Keep prior successful gold partition versions for rollback.

## Critical Transformation Pseudocode

```python
def run_daily_batch(run_date):
    manifest = ingest_source_files(run_date)
    validate_required_files(manifest)

    bronze_credit = load_credit_snapshots(manifest.credit_files)
    bronze_sales = load_workbook_sheet(manifest.sales_workbook, "Sales Details")
    bronze_dob = load_workbook_sheet(manifest.sales_workbook, "DOB")
    bronze_income = load_workbook_sheet(manifest.sales_workbook, "Income Level")
    bronze_nps = load_workbook_sheet(manifest.nps_workbook, "Sheet1")

    silver_credit = clean_credit(bronze_credit)
    silver_sales = dedupe_sales(bronze_sales)
    silver_dob = keep_latest_dob_by_loan(bronze_dob)
    silver_income = aggregate_income_by_loan(bronze_income)
    silver_nps = dedupe_nps_by_submission(bronze_nps)

    gold_snapshot = (
        silver_credit
        .merge(silver_sales, on="loan_id", how="left")
        .merge(silver_dob, on="loan_id", how="left")
        .merge(silver_income, on="loan_id", how="left")
        .pipe(add_age_band)
        .pipe(add_avg_monthly_income_band)
        .pipe(add_days_past_due)
        .pipe(add_risk_category)
    )

    quality_results = run_quality_checks(gold_snapshot, silver_nps)
    if quality_results.has_blocking_failures():
        alert_stakeholders(quality_results)
        stop_without_publishing()

    publish_partition(gold_snapshot, partition="reporting_date")
    publish_portfolio_metrics(gold_snapshot)
    publish_credit_nps_view(gold_snapshot, silver_nps)
```

## Deliverables Created

- Architecture diagram: `pipeline_design/architecture.png`
- ETL design slides: `slides/etl_pipeline_design_slides.pdf`
- Annotated pseudocode: `docs/etl_transformation_pseudocode.py`
- Design document: `docs/etl_pipeline_design.md`
