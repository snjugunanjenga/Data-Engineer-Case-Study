"""Annotated pseudocode for the ABC Phones batch ETL pipeline.

This file documents the critical transformation path. It is intentionally
pseudocode-oriented so implementation details can be mapped to pandas, SQL,
dbt, Spark, or a cloud warehouse without changing the business logic.
"""


def run_batch_etl(run_date):
    """Run one idempotent batch for the requested run date."""

    # 1. Discover source files and record lineage metadata.
    # Manifest fields: source_name, file_path, checksum, row_count,
    # reporting_date, load_timestamp, ingestion_version, status.
    manifest = build_file_manifest(run_date)

    # 2. Stop early if required files are missing or malformed.
    # This prevents partial outputs from reaching analysts.
    validate_required_sources(
        manifest,
        required_sources=["credit_snapshots", "sales_customer_workbook", "nps_workbook"],
    )

    # 3. Load raw data exactly as received into bronze tables.
    # Bronze tables retain source file name, source row number, and raw values.
    bronze_credit = load_credit_csv_snapshots(manifest.credit_files)
    bronze_sales = load_excel_sheet(manifest.sales_customer_workbook, "Sales Details")
    bronze_gender = load_excel_sheet(manifest.sales_customer_workbook, "Gender")
    bronze_dob = load_excel_sheet(manifest.sales_customer_workbook, "DOB")
    bronze_income = load_excel_sheet(manifest.sales_customer_workbook, "Income Level")
    bronze_nps = load_excel_sheet(manifest.nps_workbook, "Sheet1")

    # 4. Standardize and clean each source independently.
    # No enrichment happens until IDs, dates, and numeric fields are typed.
    silver_credit = (
        bronze_credit
        .pipe(standardize_column_names)
        .pipe(normalize_loan_id)
        .pipe(parse_credit_dates)
        .pipe(parse_credit_numeric_fields)
        .pipe(dedupe_by_keys, keys=["loan_id", "reporting_date"])
    )
    silver_sales = (
        bronze_sales
        .pipe(standardize_column_names)
        .pipe(normalize_loan_id)
        .pipe(parse_sales_dates)
        .pipe(parse_sales_prices)
        .pipe(select_primary_sale_record)
    )
    silver_dob = (
        bronze_dob
        .pipe(standardize_column_names)
        .pipe(normalize_loan_id)
        .pipe(parse_dob_dates)
        .pipe(keep_latest_record, key="loan_id", order_by="createdat_utc")
    )
    silver_income = (
        bronze_income
        .pipe(standardize_column_names)
        .pipe(normalize_loan_id)
        .pipe(parse_income_numeric_fields)
        .pipe(aggregate_income_by_loan)
    )
    silver_nps = (
        bronze_nps
        .pipe(standardize_column_names)
        .pipe(normalize_loan_id)
        .pipe(parse_submitted_at)
        .pipe(dedupe_by_keys, keys=["submission_id"])
    )

    # 5. Enrich credit snapshots with customer attributes.
    # Credit remains the left side so portfolio reporting does not drop
    # accounts that lack customer or NPS enrichment.
    enriched_credit = (
        silver_credit
        .merge(silver_sales, on="loan_id", how="left")
        .merge(silver_dob, on="loan_id", how="left")
        .merge(silver_income, on="loan_id", how="left")
    )

    # 6. Create required analytics features.
    gold_credit_snapshot = (
        enriched_credit
        .pipe(add_age_band)
        .pipe(add_avg_monthly_income_band)
        .pipe(add_days_past_due)
        .pipe(add_risk_category)
    )

    # 7. Run data quality checks before publication.
    quality_results = run_quality_checks(
        tables={
            "gold_credit_snapshot": gold_credit_snapshot,
            "silver_nps": silver_nps,
        }
    )
    if quality_results.has_blocking_failures():
        write_quality_results(quality_results)
        alert_data_engineer_and_stakeholders(quality_results)
        raise RuntimeError("Blocking data quality checks failed; gold publish skipped.")

    # 8. Publish analytics-ready outputs by replacing only affected partitions.
    publish_partitioned_table(
        gold_credit_snapshot,
        table="gold_credit_account_snapshot",
        partition_by="reporting_date",
        mode="replace_matching_partitions",
    )
    publish_table(
        build_portfolio_metrics(gold_credit_snapshot),
        table="gold_portfolio_metrics_daily",
    )
    publish_table(
        build_credit_nps_view(gold_credit_snapshot, silver_nps),
        table="gold_credit_nps_customer_view",
    )
