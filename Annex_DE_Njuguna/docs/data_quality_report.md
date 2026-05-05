# Data Quality Report Summary

## Scope

This report summarizes profiling performed on the three ABC Phones source datasets:

- Credit portfolio snapshots: five CSV files covering 2025 reporting dates.
- Sales and customer data: Excel workbook with Sales Details, Gender, DOB, and Income Level sheets.
- NPS data: Excel workbook with customer survey responses.

Profiling was performed with pandas after standardizing column names to snake_case for consistency.

## Dataset Profile

| Dataset | Tables / files profiled | Rows profiled | Key columns | Data type notes |
|:--|--:|--:|:--|:--|
| Credit snapshots | 5 CSV snapshots | 71,456 | `loan_id`, `date`, `days_past_due`, `arrears`, `payment`, `expected_payment`, `account_status_l1`, `account_status_l2` | Dates load as strings before parsing; monetary and aging fields are numeric or numeric-like. |
| Sales/customer | 4 workbook sheets | 150,520 | `loan_id`, `sale_date`, `date_of_birth`, `duration`, income fields | Date fields include Excel datetimes and timezone strings; income fields are numeric but require aggregation by loan. |
| NPS | 1 workbook sheet | 4,129 | `submission_id`, `respondent_id`, `loan_id`, `submitted_at`, NPS score | Survey score is numeric; several feedback fields are sparse free text or yes/no categories. |

## Null and Completeness Findings

- Credit snapshots are mostly complete for core portfolio fields such as `loan_id`, account status, arrears, payments, balances, and days past due.
- Credit fields with high null rates include `return_date`, `payment_amount`, and `adjustment_amount`; these appear sparse by business design rather than simple data loss.
- Later credit snapshots contain an `unnamed_28` column with no useful business definition.
- Sales/customer sheets contain repeated `loan_id` values and partial coverage across DOB, gender, and income sheets.
- NPS survey text fields are highly sparse, including open-ended reason, improvement, challenge, channel, and feedback fields.
- NPS score has 3,985 valid scored responses out of 4,129 survey rows.

## Data Inconsistencies Discovered

### Date Issues

- Credit snapshot filenames contain reporting dates and are used as reliable snapshot dates.
- Source date fields use mixed formats, including slash dates, Excel datetimes, and timezone-aware ISO strings.
- DOB values include timezone-aware strings and must be normalized before age calculation.
- NPS `submitted_at` values are timestamp fields and parse cleanly.
- Payment due date is not directly provided; days-past-due logic must rely on source aging fields and arrears status.

### Currency and Numeric Issues

- Monetary fields such as balances, payments, deposits, arrears, and income fields require numeric parsing and validation.
- Some monetary fields contain negative values, especially balances, deposits, and payment-related fields.
- Negative values are not automatically invalid because they may represent refunds, reversals, corrections, or overpayments.
- Income fields require business interpretation because `duration` is not explicitly documented but is needed for average monthly income.

### Duplicate and Structural Issues

- Credit snapshots have unique `loan_id` values within each reporting snapshot.
- Sales Details has 20,691 unique `loan_id` values from 20,696 populated loan IDs, indicating 5 duplicate loan rows.
- Gender has 10,497 unique loan IDs from 14,896 populated loan IDs, indicating repeated customer attributes.
- DOB has 11,217 unique loan IDs from 13,562 populated loan IDs.
- Income Level has 10,609 unique loan IDs from 11,885 populated loan IDs.
- NPS has 3,532 unique loan IDs from 4,129 responses, meaning customers can submit multiple responses.

## Relationship Analysis

`loan_id` is the strongest common join key across the three source datasets.

| Relationship | Cardinality / integrity finding | Treatment |
|:--|:--|:--|
| Credit snapshots by `loan_id` and reporting date | One account record per loan per snapshot. | Use `loan_id` + `reporting_date` as credit snapshot grain. |
| Sales Details to credit | 20,689 of 20,691 Sales Details loan IDs matched credit records; 2 orphan loan IDs found. | Keep credit as the left side for portfolio analysis and flag orphan sales rows. |
| Gender, DOB, Income to Sales Details | All unique populated loan IDs matched Sales Details, but repeated rows exist. | Deduplicate or aggregate by sheet-specific rules before enrichment. |
| NPS to credit | All 3,532 unique NPS loan IDs matched credit records, but repeated survey responses exist. | Preserve repeated NPS responses and create latest-response or aggregated views as needed. |

## Assumptions

- `loan_id` is the primary analytical join key across credit, sales/customer, and NPS data.
- Credit filenames provide reliable reporting dates and are preserved as `reporting_date`.
- Missing values are not imputed during profiling; they are measured, documented, and handled later using explicit rules.
- Date parsing should use explicit conversion with invalid parses retained as null plus validation flags.
- DOB-derived age is preferred over `customer_age` because observed credit `customer_age` values do not consistently behave like age in years.
- NPS is optional enrichment because survey coverage is partial and repeated responses can be analytically meaningful.
- Negative monetary values are flagged for review, not dropped automatically.

## Cleaning Decisions and Justification

| Issue | Cleaning decision | Justification |
|:--|:--|:--|
| Inconsistent column names | Standardize all columns to snake_case. | Makes joins, validation, and downstream code reproducible. |
| Raw source files | Keep raw files immutable and write cleaned outputs separately. | Maintains auditability and enables replay. |
| Duplicate `loan_id` values in customer sheets | Apply deterministic rules per sheet: latest DOB record, aggregated income records, primary sales row, and preserved NPS responses. | Some duplicates represent legitimate repeated records, so blind row dropping would lose information. |
| High-null business fields | Retain fields and add missingness flags where analytically useful. | Sparse fields such as returns, adjustments, and survey feedback can still carry business meaning. |
| Date fields | Parse explicitly and normalize timezone handling. | Portfolio aging, reporting snapshots, and age calculation depend on reliable dates. |
| Currency and numeric fields | Strip formatting, convert to numeric, and flag invalid or negative values. | Analysts need numeric fields, but anomalies must remain visible for validation. |
| `unnamed_*` columns | Drop only when empty or not defined in the data dictionary. | These are likely spreadsheet artifacts with no business meaning. |
| Relationship mismatches | Keep portfolio credit records as the base and flag unmatched enrichment records. | Prevents customer or NPS sparsity from removing valid portfolio accounts. |

## Key Takeaway

The datasets are usable for portfolio analysis after controlled cleaning, but they require explicit handling of repeated customer records, sparse enrichment fields, mixed date formats, negative monetary values, and unclear status semantics. The strongest reliable grain is `loan_id` by `reporting_date` for credit snapshots, enriched with customer and NPS data only after deduplication, aggregation, and validation.
