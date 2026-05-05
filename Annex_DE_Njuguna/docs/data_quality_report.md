# Data Quality Report

## Scope

This report profiles all credit snapshots, all sheets in the sales/customer workbook, and the NPS survey workbook using pandas.

- Raw data directory: `/workspaces/Data-Engineer-Case-Study/Annex_DE_Njuguna/data/raw`

## Work Performed

- Loaded five credit portfolio CSV snapshots and captured reporting dates from filenames.
- Loaded every sheet from the sales/customer workbook: Sales Details, Gender, DOB, and Income Level.
- Loaded the NPS workbook survey sheet.
- Standardized column names to snake_case for profiling and relationship checks.
- Calculated row counts, column data types, null counts, null percentages, and unique counts.
- Checked duplicate full rows and duplicate identifier values.
- Parsed date-like columns with UTC normalization to detect invalid dates and mixed timezone issues.
- Profiled date source formats and sample values before cleaning.
- Profiled numeric and currency-like columns for formatting, non-numeric values, negative values, and ranges.
- Analyzed `loan_id` join coverage, cardinality, and foreign-key integrity across source datasets.
- Generated cleaning decisions and justifications for discovered inconsistencies.

## Source Dataset Summary

| source_dataset   |   tables_or_sheets_profiled |   total_rows_profiled |   distinct_columns_observed | profiled_objects                                                                                                                                                         |
|:-----------------|----------------------------:|----------------------:|----------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| credit           |                           5 |                 71456 |                          36 | credit__Credit Data - 01-01-2025, credit__Credit Data - 30-03-2025, credit__Credit Data - 30-06-2025, credit__Credit Data - 30-09-2025, credit__Credit Data - 30-12-2025 |
| sales_customer   |                           4 |                150520 |                          27 | sales_customer__Sales Details, sales_customer__Gender, sales_customer__DOB, sales_customer__Income Level                                                                 |
| nps              |                           1 |                  4129 |                          17 | nps__Sheet1                                                                                                                                                              |

## Likely Join Keys and Relationship Coverage

| dataset                          | join_key          |   non_null_count |   unique_count |   duplicate_value_count |
|:---------------------------------|:------------------|-----------------:|---------------:|------------------------:|
| credit__Credit Data - 01-01-2025 | loan_id           |             8935 |           8935 |                       0 |
| credit__Credit Data - 30-03-2025 | loan_id           |            11024 |          11024 |                       0 |
| credit__Credit Data - 30-06-2025 | loan_id           |            13891 |          13891 |                       0 |
| credit__Credit Data - 30-09-2025 | loan_id           |            16864 |          16864 |                       0 |
| credit__Credit Data - 30-12-2025 | loan_id           |            20742 |          20742 |                       0 |
| sales_customer__Sales Details    | loan_id           |            20696 |          20691 |                       5 |
| sales_customer__Gender           | loan_id           |            14896 |          10497 |                    4399 |
| sales_customer__DOB              | loan_id           |            13562 |          11217 |                    2345 |
| sales_customer__Income Level     | loan_id           |            11885 |          10609 |                    1276 |
| nps__Sheet1                      | loan_id           |             4129 |           3532 |                     597 |
| sales_customer__Sales Details    | loan_id_to_credit |            20691 |          20689 |                       2 |
| sales_customer__Gender           | loan_id_to_credit |            10497 |          10497 |                       0 |
| sales_customer__DOB              | loan_id_to_credit |            11217 |          11217 |                       0 |
| sales_customer__Income Level     | loan_id_to_credit |            10609 |          10609 |                       0 |
| nps__Sheet1                      | loan_id_to_credit |             3532 |           3532 |                       0 |

## Relationship Analysis: Cardinality and Foreign-Key Integrity

| child_dataset                    | parent_dataset                | join_key   |   child_rows_with_key |   child_unique_keys |   child_duplicate_key_rows |   matched_parent_keys |   orphan_child_keys |   foreign_key_integrity_percent | cardinality_assessment                     |
|:---------------------------------|:------------------------------|:-----------|----------------------:|--------------------:|---------------------------:|----------------------:|--------------------:|--------------------------------:|:-------------------------------------------|
| credit__Credit Data - 01-01-2025 | credit_union                  | loan_id    |                  8935 |                8935 |                          0 |                  8935 |                   0 |                          100    | one-to-one candidate                       |
| credit__Credit Data - 30-03-2025 | credit_union                  | loan_id    |                 11024 |               11024 |                          0 |                 11024 |                   0 |                          100    | one-to-one candidate                       |
| credit__Credit Data - 30-06-2025 | credit_union                  | loan_id    |                 13891 |               13891 |                          0 |                 13891 |                   0 |                          100    | one-to-one candidate                       |
| credit__Credit Data - 30-09-2025 | credit_union                  | loan_id    |                 16864 |               16864 |                          0 |                 16864 |                   0 |                          100    | one-to-one candidate                       |
| credit__Credit Data - 30-12-2025 | credit_union                  | loan_id    |                 20742 |               20742 |                          0 |                 20742 |                   0 |                          100    | one-to-one candidate                       |
| sales_customer__Sales Details    | credit_union                  | loan_id    |                 20696 |               20691 |                          5 |                 20689 |                   2 |                           99.99 | many-to-one or repeated-event relationship |
| sales_customer__Gender           | sales_customer__Sales Details | loan_id    |                 14896 |               10497 |                       4399 |                 10497 |                   0 |                          100    | many-to-one or repeated-event relationship |
| sales_customer__DOB              | sales_customer__Sales Details | loan_id    |                 13562 |               11217 |                       2345 |                 11217 |                   0 |                          100    | many-to-one or repeated-event relationship |
| sales_customer__Income Level     | sales_customer__Sales Details | loan_id    |                 11885 |               10609 |                       1276 |                 10609 |                   0 |                          100    | many-to-one or repeated-event relationship |
| nps__Sheet1                      | credit_union                  | loan_id    |                  4129 |                3532 |                        597 |                  3532 |                   0 |                          100    | many-to-one or repeated-event relationship |

## Inconsistency Summary and Cleaning Decision Log

| dataset                          | issue_type                   | field_or_rule                                                                                                                                                                                                                                                                                                                                                                                                                                                      |   affected_count | cleaning_decision                                                                                                           | justification                                                                                                    |
|:---------------------------------|:-----------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------:|:----------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------|
| credit__Credit Data - 01-01-2025 | columns_over_50_percent_null | return_date, payment_amount, adjustment_amount                                                                                                                                                                                                                                                                                                                                                                                                                     |                3 | Retain high-null business fields but add missingness flags before analysis.                                                 | High-null fields such as return or adjustment amounts can be sparse by design and still analytically meaningful. |
| credit__Credit Data - 01-01-2025 | customer_age_outside_18_120  | customer_age                                                                                                                                                                                                                                                                                                                                                                                                                                                       |             6572 | Do not use `customer_age` as age in years until its unit is confirmed; derive age from DOB where available.                 | Observed values exceed normal human age ranges, suggesting a different unit or source-system defect.             |
| credit__Credit Data - 01-01-2025 | numeric_currency_anomaly     | total_paid                                                                                                                                                                                                                                                                                                                                                                                                                                                         |                1 | Parse numeric/currency fields after stripping formatting, then flag negative or non-numeric values for business validation. | Negative balances or payments may be refunds/adjustments, but they should not be silently coerced or dropped.    |
| credit__Credit Data - 01-01-2025 | numeric_currency_anomaly     | balance                                                                                                                                                                                                                                                                                                                                                                                                                                                            |                7 | Parse numeric/currency fields after stripping formatting, then flag negative or non-numeric values for business validation. | Negative balances or payments may be refunds/adjustments, but they should not be silently coerced or dropped.    |
| credit__Credit Data - 01-01-2025 | numeric_currency_anomaly     | closing_balance                                                                                                                                                                                                                                                                                                                                                                                                                                                    |                3 | Parse numeric/currency fields after stripping formatting, then flag negative or non-numeric values for business validation. | Negative balances or payments may be refunds/adjustments, but they should not be silently coerced or dropped.    |
| credit__Credit Data - 01-01-2025 | numeric_currency_anomaly     | deposit                                                                                                                                                                                                                                                                                                                                                                                                                                                            |                1 | Parse numeric/currency fields after stripping formatting, then flag negative or non-numeric values for business validation. | Negative balances or payments may be refunds/adjustments, but they should not be silently coerced or dropped.    |
| credit__Credit Data - 01-01-2025 | numeric_currency_anomaly     | total_paid_with_adjustments_15d                                                                                                                                                                                                                                                                                                                                                                                                                                    |                1 | Parse numeric/currency fields after stripping formatting, then flag negative or non-numeric values for business validation. | Negative balances or payments may be refunds/adjustments, but they should not be silently coerced or dropped.    |
| credit__Credit Data - 30-03-2025 | columns_over_50_percent_null | return_date, payment_amount, adjustment_amount                                                                                                                                                                                                                                                                                                                                                                                                                     |                3 | Retain high-null business fields but add missingness flags before analysis.                                                 | High-null fields such as return or adjustment amounts can be sparse by design and still analytically meaningful. |
| credit__Credit Data - 30-03-2025 | customer_age_outside_18_120  | customer_age                                                                                                                                                                                                                                                                                                                                                                                                                                                       |             8547 | Do not use `customer_age` as age in years until its unit is confirmed; derive age from DOB where available.                 | Observed values exceed normal human age ranges, suggesting a different unit or source-system defect.             |
| credit__Credit Data - 30-03-2025 | numeric_currency_anomaly     | total_paid                                                                                                                                                                                                                                                                                                                                                                                                                                                         |                1 | Parse numeric/currency fields after stripping formatting, then flag negative or non-numeric values for business validation. | Negative balances or payments may be refunds/adjustments, but they should not be silently coerced or dropped.    |
| credit__Credit Data - 30-03-2025 | numeric_currency_anomaly     | balance                                                                                                                                                                                                                                                                                                                                                                                                                                                            |                9 | Parse numeric/currency fields after stripping formatting, then flag negative or non-numeric values for business validation. | Negative balances or payments may be refunds/adjustments, but they should not be silently coerced or dropped.    |
| credit__Credit Data - 30-03-2025 | numeric_currency_anomaly     | closing_balance                                                                                                                                                                                                                                                                                                                                                                                                                                                    |                3 | Parse numeric/currency fields after stripping formatting, then flag negative or non-numeric values for business validation. | Negative balances or payments may be refunds/adjustments, but they should not be silently coerced or dropped.    |
| credit__Credit Data - 30-03-2025 | numeric_currency_anomaly     | deposit                                                                                                                                                                                                                                                                                                                                                                                                                                                            |                1 | Parse numeric/currency fields after stripping formatting, then flag negative or non-numeric values for business validation. | Negative balances or payments may be refunds/adjustments, but they should not be silently coerced or dropped.    |
| credit__Credit Data - 30-03-2025 | numeric_currency_anomaly     | total_paid_with_adjustments_15d                                                                                                                                                                                                                                                                                                                                                                                                                                    |                1 | Parse numeric/currency fields after stripping formatting, then flag negative or non-numeric values for business validation. | Negative balances or payments may be refunds/adjustments, but they should not be silently coerced or dropped.    |
| credit__Credit Data - 30-06-2025 | unnamed_columns              | unnamed_28                                                                                                                                                                                                                                                                                                                                                                                                                                                         |                1 | Drop unnamed columns when they are empty or have no data dictionary definition.                                             | Unnamed columns are usually spreadsheet artifacts and cannot be interpreted reliably.                            |
| credit__Credit Data - 30-06-2025 | all_null_columns             | unnamed_28                                                                                                                                                                                                                                                                                                                                                                                                                                                         |                1 | Quarantine or flag affected records for review before downstream use.                                                       | Suspicious values need traceability so analysts can include or exclude them deliberately.                        |
| credit__Credit Data - 30-06-2025 | columns_over_50_percent_null | return_date, payment_amount, adjustment_amount, unnamed_28                                                                                                                                                                                                                                                                                                                                                                                                         |                4 | Retain high-null business fields but add missingness flags before analysis.                                                 | High-null fields such as return or adjustment amounts can be sparse by design and still analytically meaningful. |
| credit__Credit Data - 30-06-2025 | customer_age_outside_18_120  | customer_age                                                                                                                                                                                                                                                                                                                                                                                                                                                       |            10732 | Do not use `customer_age` as age in years until its unit is confirmed; derive age from DOB where available.                 | Observed values exceed normal human age ranges, suggesting a different unit or source-system defect.             |
| credit__Credit Data - 30-06-2025 | numeric_currency_anomaly     | total_paid                                                                                                                                                                                                                                                                                                                                                                                                                                                         |                1 | Parse numeric/currency fields after stripping formatting, then flag negative or non-numeric values for business validation. | Negative balances or payments may be refunds/adjustments, but they should not be silently coerced or dropped.    |
| credit__Credit Data - 30-06-2025 | numeric_currency_anomaly     | balance                                                                                                                                                                                                                                                                                                                                                                                                                                                            |               34 | Parse numeric/currency fields after stripping formatting, then flag negative or non-numeric values for business validation. | Negative balances or payments may be refunds/adjustments, but they should not be silently coerced or dropped.    |
| credit__Credit Data - 30-06-2025 | numeric_currency_anomaly     | closing_balance                                                                                                                                                                                                                                                                                                                                                                                                                                                    |                3 | Parse numeric/currency fields after stripping formatting, then flag negative or non-numeric values for business validation. | Negative balances or payments may be refunds/adjustments, but they should not be silently coerced or dropped.    |
| credit__Credit Data - 30-06-2025 | numeric_currency_anomaly     | deposit                                                                                                                                                                                                                                                                                                                                                                                                                                                            |                1 | Parse numeric/currency fields after stripping formatting, then flag negative or non-numeric values for business validation. | Negative balances or payments may be refunds/adjustments, but they should not be silently coerced or dropped.    |
| credit__Credit Data - 30-06-2025 | numeric_currency_anomaly     | total_paid_with_adjustments_15d                                                                                                                                                                                                                                                                                                                                                                                                                                    |                1 | Parse numeric/currency fields after stripping formatting, then flag negative or non-numeric values for business validation. | Negative balances or payments may be refunds/adjustments, but they should not be silently coerced or dropped.    |
| credit__Credit Data - 30-09-2025 | unnamed_columns              | unnamed_28                                                                                                                                                                                                                                                                                                                                                                                                                                                         |                1 | Drop unnamed columns when they are empty or have no data dictionary definition.                                             | Unnamed columns are usually spreadsheet artifacts and cannot be interpreted reliably.                            |
| credit__Credit Data - 30-09-2025 | all_null_columns             | unnamed_28                                                                                                                                                                                                                                                                                                                                                                                                                                                         |                1 | Quarantine or flag affected records for review before downstream use.                                                       | Suspicious values need traceability so analysts can include or exclude them deliberately.                        |
| credit__Credit Data - 30-09-2025 | columns_over_50_percent_null | return_date, payment_amount, adjustment_amount, unnamed_28                                                                                                                                                                                                                                                                                                                                                                                                         |                4 | Retain high-null business fields but add missingness flags before analysis.                                                 | High-null fields such as return or adjustment amounts can be sparse by design and still analytically meaningful. |
| credit__Credit Data - 30-09-2025 | customer_age_outside_18_120  | customer_age                                                                                                                                                                                                                                                                                                                                                                                                                                                       |            13479 | Do not use `customer_age` as age in years until its unit is confirmed; derive age from DOB where available.                 | Observed values exceed normal human age ranges, suggesting a different unit or source-system defect.             |
| credit__Credit Data - 30-09-2025 | numeric_currency_anomaly     | total_paid                                                                                                                                                                                                                                                                                                                                                                                                                                                         |                1 | Parse numeric/currency fields after stripping formatting, then flag negative or non-numeric values for business validation. | Negative balances or payments may be refunds/adjustments, but they should not be silently coerced or dropped.    |
| credit__Credit Data - 30-09-2025 | numeric_currency_anomaly     | balance                                                                                                                                                                                                                                                                                                                                                                                                                                                            |               21 | Parse numeric/currency fields after stripping formatting, then flag negative or non-numeric values for business validation. | Negative balances or payments may be refunds/adjustments, but they should not be silently coerced or dropped.    |
| credit__Credit Data - 30-09-2025 | numeric_currency_anomaly     | closing_balance                                                                                                                                                                                                                                                                                                                                                                                                                                                    |                3 | Parse numeric/currency fields after stripping formatting, then flag negative or non-numeric values for business validation. | Negative balances or payments may be refunds/adjustments, but they should not be silently coerced or dropped.    |
| credit__Credit Data - 30-09-2025 | numeric_currency_anomaly     | deposit                                                                                                                                                                                                                                                                                                                                                                                                                                                            |                1 | Parse numeric/currency fields after stripping formatting, then flag negative or non-numeric values for business validation. | Negative balances or payments may be refunds/adjustments, but they should not be silently coerced or dropped.    |
| credit__Credit Data - 30-09-2025 | numeric_currency_anomaly     | total_paid_with_adjustments_15d                                                                                                                                                                                                                                                                                                                                                                                                                                    |                1 | Parse numeric/currency fields after stripping formatting, then flag negative or non-numeric values for business validation. | Negative balances or payments may be refunds/adjustments, but they should not be silently coerced or dropped.    |
| credit__Credit Data - 30-12-2025 | unnamed_columns              | unnamed_28                                                                                                                                                                                                                                                                                                                                                                                                                                                         |                1 | Drop unnamed columns when they are empty or have no data dictionary definition.                                             | Unnamed columns are usually spreadsheet artifacts and cannot be interpreted reliably.                            |
| credit__Credit Data - 30-12-2025 | all_null_columns             | unnamed_28                                                                                                                                                                                                                                                                                                                                                                                                                                                         |                1 | Quarantine or flag affected records for review before downstream use.                                                       | Suspicious values need traceability so analysts can include or exclude them deliberately.                        |
| credit__Credit Data - 30-12-2025 | columns_over_50_percent_null | return_date, payment_amount, adjustment_amount, unnamed_28                                                                                                                                                                                                                                                                                                                                                                                                         |                4 | Retain high-null business fields but add missingness flags before analysis.                                                 | High-null fields such as return or adjustment amounts can be sparse by design and still analytically meaningful. |
| credit__Credit Data - 30-12-2025 | customer_age_outside_18_120  | customer_age                                                                                                                                                                                                                                                                                                                                                                                                                                                       |            16647 | Do not use `customer_age` as age in years until its unit is confirmed; derive age from DOB where available.                 | Observed values exceed normal human age ranges, suggesting a different unit or source-system defect.             |
| credit__Credit Data - 30-12-2025 | numeric_currency_anomaly     | total_paid                                                                                                                                                                                                                                                                                                                                                                                                                                                         |                1 | Parse numeric/currency fields after stripping formatting, then flag negative or non-numeric values for business validation. | Negative balances or payments may be refunds/adjustments, but they should not be silently coerced or dropped.    |
| credit__Credit Data - 30-12-2025 | numeric_currency_anomaly     | balance                                                                                                                                                                                                                                                                                                                                                                                                                                                            |                5 | Parse numeric/currency fields after stripping formatting, then flag negative or non-numeric values for business validation. | Negative balances or payments may be refunds/adjustments, but they should not be silently coerced or dropped.    |
| credit__Credit Data - 30-12-2025 | numeric_currency_anomaly     | closing_balance                                                                                                                                                                                                                                                                                                                                                                                                                                                    |                3 | Parse numeric/currency fields after stripping formatting, then flag negative or non-numeric values for business validation. | Negative balances or payments may be refunds/adjustments, but they should not be silently coerced or dropped.    |
| credit__Credit Data - 30-12-2025 | numeric_currency_anomaly     | deposit                                                                                                                                                                                                                                                                                                                                                                                                                                                            |                1 | Parse numeric/currency fields after stripping formatting, then flag negative or non-numeric values for business validation. | Negative balances or payments may be refunds/adjustments, but they should not be silently coerced or dropped.    |
| credit__Credit Data - 30-12-2025 | numeric_currency_anomaly     | total_paid_with_adjustments_15d                                                                                                                                                                                                                                                                                                                                                                                                                                    |                1 | Parse numeric/currency fields after stripping formatting, then flag negative or non-numeric values for business validation. | Negative balances or payments may be refunds/adjustments, but they should not be silently coerced or dropped.    |
| sales_customer__Sales Details    | duplicate_identifier         | loan_id                                                                                                                                                                                                                                                                                                                                                                                                                                                            |                5 | Deduplicate only after selecting a deterministic business rule, such as latest timestamp or most complete record.           | Blind row dropping can remove legitimate one-to-many events or survey responses.                                 |
| sales_customer__Sales Details    | columns_over_50_percent_null | return_date, return_policy_compliance                                                                                                                                                                                                                                                                                                                                                                                                                              |                2 | Retain high-null business fields but add missingness flags before analysis.                                                 | High-null fields such as return or adjustment amounts can be sparse by design and still analytically meaningful. |
| sales_customer__Gender           | duplicate_identifier         | loan_id                                                                                                                                                                                                                                                                                                                                                                                                                                                            |             4399 | Deduplicate only after selecting a deterministic business rule, such as latest timestamp or most complete record.           | Blind row dropping can remove legitimate one-to-many events or survey responses.                                 |
| sales_customer__Gender           | columns_over_50_percent_null | loan_id                                                                                                                                                                                                                                                                                                                                                                                                                                                            |                1 | Retain high-null business fields but add missingness flags before analysis.                                                 | High-null fields such as return or adjustment amounts can be sparse by design and still analytically meaningful. |
| sales_customer__DOB              | duplicate_identifier         | loan_id                                                                                                                                                                                                                                                                                                                                                                                                                                                            |             2345 | Deduplicate only after selecting a deterministic business rule, such as latest timestamp or most complete record.           | Blind row dropping can remove legitimate one-to-many events or survey responses.                                 |
| sales_customer__DOB              | columns_over_50_percent_null | loan_id                                                                                                                                                                                                                                                                                                                                                                                                                                                            |                1 | Retain high-null business fields but add missingness flags before analysis.                                                 | High-null fields such as return or adjustment amounts can be sparse by design and still analytically meaningful. |
| sales_customer__Income Level     | duplicate_identifier         | loan_id                                                                                                                                                                                                                                                                                                                                                                                                                                                            |             1276 | Deduplicate only after selecting a deterministic business rule, such as latest timestamp or most complete record.           | Blind row dropping can remove legitimate one-to-many events or survey responses.                                 |
| sales_customer__Income Level     | numeric_currency_anomaly     | paybills_received_others                                                                                                                                                                                                                                                                                                                                                                                                                                           |               35 | Parse numeric/currency fields after stripping formatting, then flag negative or non-numeric values for business validation. | Negative balances or payments may be refunds/adjustments, but they should not be silently coerced or dropped.    |
| nps__Sheet1                      | duplicate_identifier         | respondent_id                                                                                                                                                                                                                                                                                                                                                                                                                                                      |              373 | Deduplicate only after selecting a deterministic business rule, such as latest timestamp or most complete record.           | Blind row dropping can remove legitimate one-to-many events or survey responses.                                 |
| nps__Sheet1                      | duplicate_identifier         | loan_id                                                                                                                                                                                                                                                                                                                                                                                                                                                            |              597 | Deduplicate only after selecting a deterministic business rule, such as latest timestamp or most complete record.           | Blind row dropping can remove legitimate one-to-many events or survey responses.                                 |
| nps__Sheet1                      | columns_over_50_percent_null | what_is_the_main_reason_for_your_score, what_is_one_thing_we_could_do_to_improve_your_experience_with_us, if_yes_please_describe_the_challenge_you_faced_and_how_we_can_improve_your_experience, have_you_used_the_mophones_app_moapp_to_manage_your_account_or_make_payments, which_communication_channel_do_you_prefer_when_contacting_mophones_for_inquiries_or_support, have_you_ever_had_your_phone_lock_despite_making_a_payment_on_time, any_other_feedback |                7 | Retain high-null business fields but add missingness flags before analysis.                                                 | High-null fields such as return or adjustment amounts can be sparse by design and still analytically meaningful. |

## Dataset: credit__Credit Data - 01-01-2025

- Rows: 8,935
- Columns: 35
- Full duplicate rows: 0

### Column Profile

| column                          | dtype          |   non_null_count |   null_count |   null_percent |   unique_count |
|:--------------------------------|:---------------|-----------------:|-------------:|---------------:|---------------:|
| adjustment_amount               | float64        |              570 |         8365 |          93.62 |              2 |
| payment_amount                  | float64        |              570 |         8365 |          93.62 |            193 |
| return_date                     | str            |              986 |         7949 |          88.96 |            380 |
| max_payment_date                | str            |             8906 |           29 |           0.32 |            908 |
| balance_due_to_date             | float64        |             8930 |            5 |           0.06 |           3379 |
| total_due_today                 | float64        |             8930 |            5 |           0.06 |           1515 |
| balance                         | float64        |             8934 |            1 |           0.01 |           4026 |
| closing_balance                 | float64        |             8934 |            1 |           0.01 |           2831 |
| deposit                         | float64        |             8934 |            1 |           0.01 |            172 |
| expected_payment                | float64        |             8934 |            1 |           0.01 |            146 |
| weekly_rate                     | float64        |             8934 |            1 |           0.01 |            218 |
| account_status_l1               | str            |             8935 |            0 |           0    |             20 |
| account_status_l2               | str            |             8935 |            0 |           0    |              9 |
| advance                         | int64          |             8935 |            0 |           0    |            678 |
| arrears                         | int64          |             8935 |            0 |           0    |           2702 |
| balance_due_status              | str            |             8935 |            0 |           0    |              3 |
| credit_check_done               | str            |             8935 |            0 |           0    |              4 |
| credit_expiry                   | str            |             8935 |            0 |           0    |            645 |
| customer_age                    | int64          |             8935 |            0 |           0    |            581 |
| date                            | str            |             8935 |            0 |           0    |              1 |
| days_past_due                   | int64          |             8935 |            0 |           0    |            516 |
| discount                        | int64          |             8935 |            0 |           0    |            113 |
| first_expected_payment          | int64          |             8935 |            0 |           0    |              1 |
| first_payment                   | int64          |             8935 |            0 |           0    |              1 |
| initial_pay                     | int64          |             8935 |            0 |           0    |            629 |
| loan_id                         | str            |             8935 |            0 |           0    |           8935 |
| next_invoice_date               | str            |             8935 |            0 |           0    |              7 |
| overpayment_amount              | int64          |             8935 |            0 |           0    |             98 |
| payment                         | int64          |             8935 |            0 |           0    |            194 |
| prepayment_amount               | int64          |             8935 |            0 |           0    |             14 |
| reporting_date_from_file        | datetime64[us] |             8935 |            0 |           0    |              1 |
| sale_date                       | str            |             8935 |            0 |           0    |            581 |
| source_file                     | str            |             8935 |            0 |           0    |              1 |
| total_paid                      | int64          |             8935 |            0 |           0    |           4193 |
| total_paid_with_adjustments_15d | int64          |             8935 |            0 |           0    |           4135 |

### Duplicate Identifier Checks

| identifier_column   |   non_null_count |   unique_count |   duplicate_value_count |
|:--------------------|-----------------:|---------------:|------------------------:|
| loan_id             |             8935 |           8935 |                       0 |

### Date Inconsistency Checks

| date_column              |   non_null_count |   invalid_date_count |   invalid_date_percent | min_date                  | max_date                  |
|:-------------------------|-----------------:|---------------------:|-----------------------:|:--------------------------|:--------------------------|
| date                     |             8935 |                    0 |                      0 | 2025-01-01 00:00:00+00:00 | 2025-01-01 00:00:00+00:00 |
| return_date              |              986 |                    0 |                      0 | 2023-03-16 00:00:00+00:00 | 2025-12-24 00:00:00+00:00 |
| sale_date                |             8935 |                    0 |                      0 | 2023-02-08 00:00:00+00:00 | 2024-12-31 00:00:00+00:00 |
| credit_expiry            |             8935 |                    0 |                      0 | 2023-02-15 00:00:00+00:00 | 2025-09-30 00:00:00+00:00 |
| next_invoice_date        |             8935 |                    0 |                      0 | 2025-01-02 00:00:00+00:00 | 2025-01-08 00:00:00+00:00 |
| max_payment_date         |             8906 |                    0 |                      0 | 2023-02-08 00:00:00+00:00 | 2025-12-29 00:00:00+00:00 |
| reporting_date_from_file |             8935 |                    0 |                      0 | 2025-01-01 00:00:00+00:00 | 2025-01-01 00:00:00+00:00 |

### Date Source Format Checks

| column                   |   non_null_count |   iso_like_count |   slash_date_count |   dash_date_count |   timestamp_count | sample_values                      |
|:-------------------------|-----------------:|-----------------:|-------------------:|------------------:|------------------:|:-----------------------------------|
| date                     |             8935 |                0 |               8935 |                 0 |                 0 | 1/1/2025                           |
| return_date              |              986 |                0 |                986 |                 0 |                 0 | 1/22/2025, 11/20/2024, 7/22/2023   |
| sale_date                |             8935 |                0 |               8935 |                 0 |                 0 | 9/21/2024, 6/4/2024, 12/10/2024    |
| credit_expiry            |             8935 |                0 |               8935 |                 0 |                 0 | 12/28/2024, 12/31/2024, 12/17/2024 |
| next_invoice_date        |             8935 |                0 |               8935 |                 0 |                 0 | 1/4/2025, 1/7/2025, 1/3/2025       |
| max_payment_date         |             8906 |                0 |               8906 |                 0 |                 0 | 1/7/2025, 10/10/2025, 12/10/2024   |
| reporting_date_from_file |             8935 |             8935 |                  0 |                 0 |                 0 | 2025-01-01                         |

### Currency and Numeric Inconsistency Checks

| money_column                    |   non_null_count |   formatted_value_count |   non_numeric_after_cleaning |   negative_count |   min_value |   max_value |
|:--------------------------------|-----------------:|------------------------:|-----------------------------:|-----------------:|------------:|------------:|
| total_paid                      |             8935 |                       0 |                            0 |                1 |      -20499 |      222159 |
| total_due_today                 |             8930 |                       0 |                            0 |                0 |        3179 |      334219 |
| balance                         |             8934 |                       0 |                            0 |                7 |      -17870 |      205019 |
| days_past_due                   |             8935 |                       0 |                            0 |                0 |           0 |         685 |
| closing_balance                 |             8934 |                       0 |                            0 |                3 |          -1 |      205019 |
| arrears                         |             8935 |                       0 |                            0 |                0 |           0 |      168350 |
| payment                         |             8935 |                       0 |                            0 |                0 |           0 |       19385 |
| expected_payment                |             8934 |                       0 |                            0 |                0 |           0 |        3950 |
| first_payment                   |             8935 |                       0 |                            0 |                0 |           0 |           0 |
| first_expected_payment          |             8935 |                       0 |                            0 |                0 |           0 |           0 |
| payment_amount                  |              570 |                       0 |                            0 |                0 |           0 |       11200 |
| adjustment_amount               |              570 |                       0 |                            0 |                0 |           0 |       19385 |
| prepayment_amount               |             8935 |                       0 |                            0 |                0 |           0 |       67049 |
| deposit                         |             8934 |                       0 |                            0 |                1 |          -1 |       55499 |
| weekly_rate                     |             8934 |                       0 |                            0 |                0 |         370 |        5360 |
| discount                        |             8935 |                       0 |                            0 |                0 |           0 |       49240 |
| overpayment_amount              |             8935 |                       0 |                            0 |                0 |           0 |       40600 |
| total_paid_with_adjustments_15d |             8935 |                       0 |                            0 |                1 |      -20499 |      222159 |

### Suspicious Values

| issue                        |   count | details                                        |
|:-----------------------------|--------:|:-----------------------------------------------|
| unnamed_columns              |       0 | none                                           |
| all_null_columns             |       0 | none                                           |
| columns_over_50_percent_null |       3 | return_date, payment_amount, adjustment_amount |
| customer_age_outside_18_120  |    6572 | customer_age                                   |
| negative_days_past_due       |       0 | days_past_due                                  |

## Dataset: credit__Credit Data - 30-03-2025

- Rows: 11,024
- Columns: 35
- Full duplicate rows: 0

### Column Profile

| column                          | dtype          |   non_null_count |   null_count |   null_percent |   unique_count |
|:--------------------------------|:---------------|-----------------:|-------------:|---------------:|---------------:|
| adjustment_amount               | float64        |              647 |        10377 |          94.13 |              4 |
| payment_amount                  | float64        |              647 |        10377 |          94.13 |            216 |
| return_date                     | str            |             1185 |         9839 |          89.25 |            428 |
| max_payment_date                | str            |            10958 |           66 |           0.6  |            909 |
| balance_due_to_date             | float64        |            11019 |            5 |           0.05 |           4189 |
| total_due_today                 | float64        |            11019 |            5 |           0.05 |           1778 |
| balance                         | float64        |            11023 |            1 |           0.01 |           4641 |
| closing_balance                 | float64        |            11023 |            1 |           0.01 |           3558 |
| deposit                         | float64        |            11023 |            1 |           0.01 |            281 |
| weekly_rate                     | float64        |            11023 |            1 |           0.01 |            245 |
| account_status_l1               | str            |            11024 |            0 |           0    |             20 |
| account_status_l2               | str            |            11024 |            0 |           0    |              9 |
| advance                         | int64          |            11024 |            0 |           0    |            720 |
| arrears                         | int64          |            11024 |            0 |           0    |           3470 |
| balance_due_status              | str            |            11024 |            0 |           0    |              3 |
| credit_check_done               | str            |            11024 |            0 |           0    |              4 |
| credit_expiry                   | str            |            11024 |            0 |           0    |            743 |
| customer_age                    | int64          |            11024 |            0 |           0    |            670 |
| date                            | str            |            11024 |            0 |           0    |              1 |
| days_past_due                   | int64          |            11024 |            0 |           0    |            604 |
| discount                        | int64          |            11024 |            0 |           0    |            165 |
| expected_payment                | int64          |            11024 |            0 |           0    |            172 |
| first_expected_payment          | int64          |            11024 |            0 |           0    |              2 |
| first_payment                   | int64          |            11024 |            0 |           0    |              2 |
| initial_pay                     | int64          |            11024 |            0 |           0    |            742 |
| loan_id                         | str            |            11024 |            0 |           0    |          11024 |
| next_invoice_date               | str            |            11024 |            0 |           0    |              7 |
| overpayment_amount              | int64          |            11024 |            0 |           0    |            119 |
| payment                         | int64          |            11024 |            0 |           0    |            219 |
| prepayment_amount               | int64          |            11024 |            0 |           0    |             15 |
| reporting_date_from_file        | datetime64[us] |            11024 |            0 |           0    |              1 |
| sale_date                       | str            |            11024 |            0 |           0    |            670 |
| source_file                     | str            |            11024 |            0 |           0    |              1 |
| total_paid                      | int64          |            11024 |            0 |           0    |           4988 |
| total_paid_with_adjustments_15d | int64          |            11024 |            0 |           0    |           4935 |

### Duplicate Identifier Checks

| identifier_column   |   non_null_count |   unique_count |   duplicate_value_count |
|:--------------------|-----------------:|---------------:|------------------------:|
| loan_id             |            11024 |          11024 |                       0 |

### Date Inconsistency Checks

| date_column              |   non_null_count |   invalid_date_count |   invalid_date_percent | min_date                  | max_date                  |
|:-------------------------|-----------------:|---------------------:|-----------------------:|:--------------------------|:--------------------------|
| date                     |            11024 |                    0 |                      0 | 2025-03-31 00:00:00+00:00 | 2025-03-31 00:00:00+00:00 |
| return_date              |             1185 |                    0 |                      0 | 2023-03-16 00:00:00+00:00 | 2025-12-29 00:00:00+00:00 |
| sale_date                |            11024 |                    0 |                      0 | 2023-02-08 00:00:00+00:00 | 2025-03-31 00:00:00+00:00 |
| credit_expiry            |            11024 |                    0 |                      0 | 2023-02-15 00:00:00+00:00 | 2026-02-06 00:00:00+00:00 |
| next_invoice_date        |            11024 |                    0 |                      0 | 2025-04-01 00:00:00+00:00 | 2025-04-07 00:00:00+00:00 |
| max_payment_date         |            10958 |                    0 |                      0 | 2023-02-08 00:00:00+00:00 | 2025-12-30 00:00:00+00:00 |
| reporting_date_from_file |            11024 |                    0 |                      0 | 2025-03-30 00:00:00+00:00 | 2025-03-30 00:00:00+00:00 |

### Date Source Format Checks

| column                   |   non_null_count |   iso_like_count |   slash_date_count |   dash_date_count |   timestamp_count | sample_values                   |
|:-------------------------|-----------------:|-----------------:|-------------------:|------------------:|------------------:|:--------------------------------|
| date                     |            11024 |                0 |              11024 |                 0 |                 0 | 3/31/2025                       |
| return_date              |             1185 |                0 |               1185 |                 0 |                 0 | 2/13/2025, 6/27/2025, 7/30/2024 |
| sale_date                |            11024 |                0 |              11024 |                 0 |                 0 | 7/28/2024, 8/10/2024, 9/6/2023  |
| credit_expiry            |            11024 |                0 |              11024 |                 0 |                 0 | 8/4/2024, 11/2/2024, 9/4/2024   |
| next_invoice_date        |            11024 |                0 |              11024 |                 0 |                 0 | 4/6/2025, 4/5/2025, 4/2/2025    |
| max_payment_date         |            10958 |                0 |              10958 |                 0 |                 0 | 7/28/2024, 1/24/2025, 8/10/2024 |
| reporting_date_from_file |            11024 |            11024 |                  0 |                 0 |                 0 | 2025-03-30                      |

### Currency and Numeric Inconsistency Checks

| money_column                    |   non_null_count |   formatted_value_count |   non_numeric_after_cleaning |   negative_count |   min_value |   max_value |
|:--------------------------------|-----------------:|------------------------:|-----------------------------:|-----------------:|------------:|------------:|
| total_paid                      |            11024 |                       0 |                            0 |                1 |      -20499 |      222159 |
| total_due_today                 |            11019 |                       0 |                            0 |                0 |        3799 |      334219 |
| balance                         |            11023 |                       0 |                            0 |                9 |      -37844 |      205019 |
| days_past_due                   |            11024 |                       0 |                            0 |                0 |           0 |         774 |
| closing_balance                 |            11023 |                       0 |                            0 |                3 |          -1 |      205019 |
| arrears                         |            11024 |                       0 |                            0 |                0 |           0 |      179579 |
| payment                         |            11024 |                       0 |                            0 |                0 |           0 |       47499 |
| expected_payment                |            11024 |                       0 |                            0 |                0 |           0 |       47499 |
| first_payment                   |            11024 |                       0 |                            0 |                0 |           0 |           1 |
| first_expected_payment          |            11024 |                       0 |                            0 |                0 |           0 |           1 |
| payment_amount                  |              647 |                       0 |                            0 |                0 |           0 |       47499 |
| adjustment_amount               |              647 |                       0 |                            0 |                0 |           0 |       10130 |
| prepayment_amount               |            11024 |                       0 |                            0 |                0 |           0 |       67049 |
| deposit                         |            11023 |                       0 |                            0 |                1 |          -1 |       55499 |
| weekly_rate                     |            11023 |                       0 |                            0 |                0 |         370 |        8720 |
| discount                        |            11024 |                       0 |                            0 |                0 |           0 |       51080 |
| overpayment_amount              |            11024 |                       0 |                            0 |                0 |           0 |       40600 |
| total_paid_with_adjustments_15d |            11024 |                       0 |                            0 |                1 |      -20499 |      222159 |

### Suspicious Values

| issue                        |   count | details                                        |
|:-----------------------------|--------:|:-----------------------------------------------|
| unnamed_columns              |       0 | none                                           |
| all_null_columns             |       0 | none                                           |
| columns_over_50_percent_null |       3 | return_date, payment_amount, adjustment_amount |
| customer_age_outside_18_120  |    8547 | customer_age                                   |
| negative_days_past_due       |       0 | days_past_due                                  |

## Dataset: credit__Credit Data - 30-06-2025

- Rows: 13,891
- Columns: 36
- Full duplicate rows: 0

### Column Profile

| column                          | dtype          |   non_null_count |   null_count |   null_percent |   unique_count |
|:--------------------------------|:---------------|-----------------:|-------------:|---------------:|---------------:|
| unnamed_28                      | float64        |                0 |        13891 |         100    |              0 |
| adjustment_amount               | float64        |              901 |        12990 |          93.51 |              9 |
| payment_amount                  | float64        |              901 |        12990 |          93.51 |            253 |
| return_date                     | str            |             1402 |        12489 |          89.91 |            479 |
| max_payment_date                | str            |            13748 |          143 |           1.03 |            909 |
| balance_due_to_date             | float64        |            13885 |            6 |           0.04 |           4965 |
| total_due_today                 | float64        |            13885 |            6 |           0.04 |           1974 |
| balance                         | float64        |            13889 |            2 |           0.01 |           5209 |
| closing_balance                 | float64        |            13889 |            2 |           0.01 |           4404 |
| deposit                         | float64        |            13889 |            2 |           0.01 |            388 |
| weekly_rate                     | float64        |            13889 |            2 |           0.01 |            278 |
| account_status_l1               | str            |            13891 |            0 |           0    |             20 |
| account_status_l2               | str            |            13891 |            0 |           0    |              9 |
| advance                         | float64        |            13891 |            0 |           0    |            827 |
| arrears                         | float64        |            13891 |            0 |           0    |           4139 |
| balance_due_status              | str            |            13891 |            0 |           0    |              3 |
| credit_check_done               | str            |            13891 |            0 |           0    |              4 |
| credit_expiry                   | str            |            13891 |            0 |           0    |            834 |
| customer_age                    | int64          |            13891 |            0 |           0    |            761 |
| date                            | str            |            13891 |            0 |           0    |              1 |
| days_past_due                   | int64          |            13891 |            0 |           0    |            697 |
| discount                        | float64        |            13891 |            0 |           0    |            275 |
| expected_payment                | int64          |            13891 |            0 |           0    |            196 |
| first_expected_payment          | int64          |            13891 |            0 |           0    |              2 |
| first_payment                   | int64          |            13891 |            0 |           0    |              2 |
| initial_pay                     | int64          |            13891 |            0 |           0    |            840 |
| loan_id                         | str            |            13891 |            0 |           0    |          13891 |
| next_invoice_date               | str            |            13891 |            0 |           0    |              7 |
| overpayment_amount              | float64        |            13891 |            0 |           0    |            159 |
| payment                         | int64          |            13891 |            0 |           0    |            259 |
| prepayment_amount               | int64          |            13891 |            0 |           0    |             21 |
| reporting_date_from_file        | datetime64[us] |            13891 |            0 |           0    |              1 |
| sale_date                       | str            |            13891 |            0 |           0    |            761 |
| source_file                     | str            |            13891 |            0 |           0    |              1 |
| total_paid                      | int64          |            13891 |            0 |           0    |           5747 |
| total_paid_with_adjustments_15d | int64          |            13891 |            0 |           0    |           5684 |

### Duplicate Identifier Checks

| identifier_column   |   non_null_count |   unique_count |   duplicate_value_count |
|:--------------------|-----------------:|---------------:|------------------------:|
| loan_id             |            13891 |          13891 |                       0 |

### Date Inconsistency Checks

| date_column              |   non_null_count |   invalid_date_count |   invalid_date_percent | min_date                  | max_date                  |
|:-------------------------|-----------------:|---------------------:|-----------------------:|:--------------------------|:--------------------------|
| date                     |            13891 |                    0 |                      0 | 2025-06-30 00:00:00+00:00 | 2025-06-30 00:00:00+00:00 |
| return_date              |             1402 |                    0 |                      0 | 2023-03-16 00:00:00+00:00 | 2025-12-29 00:00:00+00:00 |
| sale_date                |            13891 |                    0 |                      0 | 2023-02-08 00:00:00+00:00 | 2025-06-30 00:00:00+00:00 |
| credit_expiry            |            13891 |                    0 |                      0 | 2023-02-15 00:00:00+00:00 | 2026-04-25 00:00:00+00:00 |
| next_invoice_date        |            13891 |                    0 |                      0 | 2025-07-01 00:00:00+00:00 | 2025-07-07 00:00:00+00:00 |
| max_payment_date         |            13748 |                    0 |                      0 | 2023-02-08 00:00:00+00:00 | 2025-12-30 00:00:00+00:00 |
| reporting_date_from_file |            13891 |                    0 |                      0 | 2025-06-30 00:00:00+00:00 | 2025-06-30 00:00:00+00:00 |

### Date Source Format Checks

| column                   |   non_null_count |   iso_like_count |   slash_date_count |   dash_date_count |   timestamp_count | sample_values                    |
|:-------------------------|-----------------:|-----------------:|-------------------:|------------------:|------------------:|:---------------------------------|
| date                     |            13891 |                0 |              13891 |                 0 |                 0 | 6/30/2025                        |
| return_date              |             1402 |                0 |               1402 |                 0 |                 0 | 8/5/2024, 12/17/2024, 8/13/2025  |
| sale_date                |            13891 |                0 |              13891 |                 0 |                 0 | 12/27/2024, 5/30/2025, 2/26/2024 |
| credit_expiry            |            13891 |                0 |              13891 |                 0 |                 0 | 1/3/2025, 6/20/2025, 3/3/2025    |
| next_invoice_date        |            13891 |                0 |              13891 |                 0 |                 0 | 7/4/2025, 7/7/2025, 7/1/2025     |
| max_payment_date         |            13748 |                0 |              13748 |                 0 |                 0 | 12/27/2024, 6/6/2025, 3/31/2025  |
| reporting_date_from_file |            13891 |            13891 |                  0 |                 0 |                 0 | 2025-06-30                       |

### Currency and Numeric Inconsistency Checks

| money_column                    |   non_null_count |   formatted_value_count |   non_numeric_after_cleaning |   negative_count |   min_value |   max_value |
|:--------------------------------|-----------------:|------------------------:|-----------------------------:|-----------------:|------------:|------------:|
| total_paid                      |            13891 |                       0 |                            0 |                1 |      -20499 |      222159 |
| total_due_today                 |            13885 |                       0 |                            0 |                0 |        3499 |      334219 |
| balance                         |            13889 |                       0 |                            0 |               34 |      -59524 |      205019 |
| days_past_due                   |            13891 |                       0 |                            0 |                0 |           0 |         865 |
| closing_balance                 |            13889 |                       0 |                            0 |                3 |          -1 |      205019 |
| arrears                         |            13891 |                       0 |                            0 |                0 |           0 |      205019 |
| payment                         |            13891 |                       0 |                            0 |                0 |           0 |       37999 |
| expected_payment                |            13891 |                       0 |                            0 |                0 |           0 |       42699 |
| first_payment                   |            13891 |                       0 |                            0 |                0 |           0 |           1 |
| first_expected_payment          |            13891 |                       0 |                            0 |                0 |           0 |           1 |
| payment_amount                  |              901 |                       0 |                            0 |                0 |           0 |       37999 |
| adjustment_amount               |              901 |                       0 |                            0 |                0 |           0 |       22020 |
| prepayment_amount               |            13891 |                       0 |                            0 |                0 |           0 |       67049 |
| deposit                         |            13889 |                       0 |                            0 |                1 |          -1 |       55499 |
| weekly_rate                     |            13889 |                       0 |                            0 |                0 |         240 |        9060 |
| discount                        |            13891 |                       0 |                            0 |                0 |           0 |       75135 |
| overpayment_amount              |            13891 |                       0 |                            0 |                0 |           0 |       40600 |
| total_paid_with_adjustments_15d |            13891 |                       0 |                            0 |                1 |      -20499 |      222159 |

### Suspicious Values

| issue                        |   count | details                                                    |
|:-----------------------------|--------:|:-----------------------------------------------------------|
| unnamed_columns              |       1 | unnamed_28                                                 |
| all_null_columns             |       1 | unnamed_28                                                 |
| columns_over_50_percent_null |       4 | return_date, payment_amount, adjustment_amount, unnamed_28 |
| customer_age_outside_18_120  |   10732 | customer_age                                               |
| negative_days_past_due       |       0 | days_past_due                                              |

## Dataset: credit__Credit Data - 30-09-2025

- Rows: 16,864
- Columns: 36
- Full duplicate rows: 0

### Column Profile

| column                          | dtype          |   non_null_count |   null_count |   null_percent |   unique_count |
|:--------------------------------|:---------------|-----------------:|-------------:|---------------:|---------------:|
| unnamed_28                      | float64        |                0 |        16864 |         100    |              0 |
| adjustment_amount               | float64        |             1015 |        15849 |          93.98 |              5 |
| payment_amount                  | float64        |             1015 |        15849 |          93.98 |            269 |
| return_date                     | str            |             1569 |        15295 |          90.7  |            504 |
| max_payment_date                | str            |            16658 |          206 |           1.22 |            909 |
| balance_due_to_date             | float64        |            16858 |            6 |           0.04 |           5579 |
| total_due_today                 | float64        |            16858 |            6 |           0.04 |           2188 |
| balance                         | float64        |            16862 |            2 |           0.01 |           5691 |
| closing_balance                 | float64        |            16862 |            2 |           0.01 |           5227 |
| deposit                         | float64        |            16862 |            2 |           0.01 |            477 |
| weekly_rate                     | float64        |            16862 |            2 |           0.01 |            284 |
| account_status_l1               | str            |            16864 |            0 |           0    |             20 |
| account_status_l2               | str            |            16864 |            0 |           0    |              9 |
| advance                         | float64        |            16864 |            0 |           0    |            894 |
| arrears                         | float64        |            16864 |            0 |           0    |           4686 |
| balance_due_status              | str            |            16864 |            0 |           0    |              3 |
| credit_check_done               | str            |            16864 |            0 |           0    |              4 |
| credit_expiry                   | str            |            16864 |            0 |           0    |            943 |
| customer_age                    | int64          |            16864 |            0 |           0    |            852 |
| date                            | str            |            16864 |            0 |           0    |              1 |
| days_past_due                   | int64          |            16864 |            0 |           0    |            789 |
| discount                        | float64        |            16864 |            0 |           0    |            412 |
| expected_payment                | int64          |            16864 |            0 |           0    |            200 |
| first_expected_payment          | int64          |            16864 |            0 |           0    |              2 |
| first_payment                   | int64          |            16864 |            0 |           0    |              2 |
| initial_pay                     | int64          |            16864 |            0 |           0    |            899 |
| loan_id                         | str            |            16864 |            0 |           0    |          16864 |
| next_invoice_date               | str            |            16864 |            0 |           0    |              7 |
| overpayment_amount              | float64        |            16864 |            0 |           0    |            192 |
| payment                         | int64          |            16864 |            0 |           0    |            272 |
| prepayment_amount               | int64          |            16864 |            0 |           0    |             22 |
| reporting_date_from_file        | datetime64[us] |            16864 |            0 |           0    |              1 |
| sale_date                       | str            |            16864 |            0 |           0    |            852 |
| source_file                     | str            |            16864 |            0 |           0    |              1 |
| total_paid                      | int64          |            16864 |            0 |           0    |           6367 |
| total_paid_with_adjustments_15d | int64          |            16864 |            0 |           0    |           6305 |

### Duplicate Identifier Checks

| identifier_column   |   non_null_count |   unique_count |   duplicate_value_count |
|:--------------------|-----------------:|---------------:|------------------------:|
| loan_id             |            16864 |          16864 |                       0 |

### Date Inconsistency Checks

| date_column              |   non_null_count |   invalid_date_count |   invalid_date_percent | min_date                  | max_date                  |
|:-------------------------|-----------------:|---------------------:|-----------------------:|:--------------------------|:--------------------------|
| date                     |            16864 |                    0 |                      0 | 2025-09-30 00:00:00+00:00 | 2025-09-30 00:00:00+00:00 |
| return_date              |             1569 |                    0 |                      0 | 2023-03-16 00:00:00+00:00 | 2025-12-29 00:00:00+00:00 |
| sale_date                |            16864 |                    0 |                      0 | 2023-02-08 00:00:00+00:00 | 2025-09-30 00:00:00+00:00 |
| credit_expiry            |            16864 |                    0 |                      0 | 2023-02-15 00:00:00+00:00 | 2026-05-25 00:00:00+00:00 |
| next_invoice_date        |            16864 |                    0 |                      0 | 2025-10-01 00:00:00+00:00 | 2025-10-07 00:00:00+00:00 |
| max_payment_date         |            16658 |                    0 |                      0 | 2023-02-08 00:00:00+00:00 | 2025-12-30 00:00:00+00:00 |
| reporting_date_from_file |            16864 |                    0 |                      0 | 2025-09-30 00:00:00+00:00 | 2025-09-30 00:00:00+00:00 |

### Date Source Format Checks

| column                   |   non_null_count |   iso_like_count |   slash_date_count |   dash_date_count |   timestamp_count | sample_values                    |
|:-------------------------|-----------------:|-----------------:|-------------------:|------------------:|------------------:|:---------------------------------|
| date                     |            16864 |                0 |              16864 |                 0 |                 0 | 9/30/2025                        |
| return_date              |             1569 |                0 |               1569 |                 0 |                 0 | 7/22/2025, 2/28/2025, 11/17/2023 |
| sale_date                |            16864 |                0 |              16864 |                 0 |                 0 | 7/27/2024, 10/31/2024, 4/19/2025 |
| credit_expiry            |            16864 |                0 |              16864 |                 0 |                 0 | 2/8/2025, 11/21/2024, 10/4/2025  |
| next_invoice_date        |            16864 |                0 |              16864 |                 0 |                 0 | 10/4/2025, 10/2/2025, 10/3/2025  |
| max_payment_date         |            16658 |                0 |              16658 |                 0 |                 0 | 3/3/2025, 11/16/2024, 12/20/2025 |
| reporting_date_from_file |            16864 |            16864 |                  0 |                 0 |                 0 | 2025-09-30                       |

### Currency and Numeric Inconsistency Checks

| money_column                    |   non_null_count |   formatted_value_count |   non_numeric_after_cleaning |   negative_count |   min_value |   max_value |
|:--------------------------------|-----------------:|------------------------:|-----------------------------:|-----------------:|------------:|------------:|
| total_paid                      |            16864 |                       0 |                            0 |                1 |      -20499 |      222159 |
| total_due_today                 |            16858 |                       0 |                            0 |                0 |        3299 |      334219 |
| balance                         |            16862 |                       0 |                            0 |               21 |      -81294 |      205019 |
| days_past_due                   |            16864 |                       0 |                            0 |                0 |           0 |         957 |
| closing_balance                 |            16862 |                       0 |                            0 |                3 |          -1 |      205019 |
| arrears                         |            16864 |                       0 |                            0 |                0 |           0 |      205019 |
| payment                         |            16864 |                       0 |                            0 |                0 |           0 |       44999 |
| expected_payment                |            16864 |                       0 |                            0 |                0 |           0 |       34999 |
| first_payment                   |            16864 |                       0 |                            0 |                0 |           0 |           1 |
| first_expected_payment          |            16864 |                       0 |                            0 |                0 |           0 |           1 |
| payment_amount                  |             1015 |                       0 |                            0 |                0 |           0 |       44999 |
| adjustment_amount               |             1015 |                       0 |                            0 |                0 |           0 |        4300 |
| prepayment_amount               |            16864 |                       0 |                            0 |                0 |           0 |       67049 |
| deposit                         |            16862 |                       0 |                            0 |                1 |          -1 |       55499 |
| weekly_rate                     |            16862 |                       0 |                            0 |                0 |         240 |        9060 |
| discount                        |            16864 |                       0 |                            0 |                0 |           0 |       75135 |
| overpayment_amount              |            16864 |                       0 |                            0 |                0 |           0 |       40600 |
| total_paid_with_adjustments_15d |            16864 |                       0 |                            0 |                1 |      -20499 |      222159 |

### Suspicious Values

| issue                        |   count | details                                                    |
|:-----------------------------|--------:|:-----------------------------------------------------------|
| unnamed_columns              |       1 | unnamed_28                                                 |
| all_null_columns             |       1 | unnamed_28                                                 |
| columns_over_50_percent_null |       4 | return_date, payment_amount, adjustment_amount, unnamed_28 |
| customer_age_outside_18_120  |   13479 | customer_age                                               |
| negative_days_past_due       |       0 | days_past_due                                              |

## Dataset: credit__Credit Data - 30-12-2025

- Rows: 20,742
- Columns: 36
- Full duplicate rows: 0

### Column Profile

| column                          | dtype          |   non_null_count |   null_count |   null_percent |   unique_count |
|:--------------------------------|:---------------|-----------------:|-------------:|---------------:|---------------:|
| unnamed_28                      | float64        |                0 |        20742 |         100    |              0 |
| adjustment_amount               | float64        |               30 |        20712 |          99.86 |              1 |
| payment_amount                  | float64        |               30 |        20712 |          99.86 |             24 |
| return_date                     | str            |             1744 |        18998 |          91.59 |              1 |
| max_payment_date                | str            |            20437 |          305 |           1.47 |            909 |
| balance_due_to_date             | float64        |            20736 |            6 |           0.03 |           6166 |
| total_due_today                 | float64        |            20736 |            6 |           0.03 |           2365 |
| balance                         | float64        |            20740 |            2 |           0.01 |           6140 |
| closing_balance                 | float64        |            20740 |            2 |           0.01 |           6138 |
| deposit                         | float64        |            20740 |            2 |           0.01 |            602 |
| weekly_rate                     | float64        |            20740 |            2 |           0.01 |            307 |
| account_status_l1               | str            |            20742 |            0 |           0    |             20 |
| account_status_l2               | str            |            20742 |            0 |           0    |              9 |
| advance                         | float64        |            20742 |            0 |           0    |            957 |
| arrears                         | float64        |            20742 |            0 |           0    |           5210 |
| balance_due_status              | str            |            20742 |            0 |           0    |              3 |
| credit_check_done               | str            |            20742 |            0 |           0    |              4 |
| credit_expiry                   | str            |            20742 |            0 |           0    |           1049 |
| customer_age                    | int64          |            20742 |            0 |           0    |            939 |
| date                            | str            |            20742 |            0 |           0    |              1 |
| days_past_due                   | int64          |            20742 |            0 |           0    |            881 |
| discount                        | float64        |            20742 |            0 |           0    |            584 |
| expected_payment                | int64          |            20742 |            0 |           0    |            201 |
| first_expected_payment          | int64          |            20742 |            0 |           0    |              1 |
| first_payment                   | int64          |            20742 |            0 |           0    |              1 |
| initial_pay                     | int64          |            20742 |            0 |           0    |            947 |
| loan_id                         | str            |            20742 |            0 |           0    |          20742 |
| next_invoice_date               | str            |            20742 |            0 |           0    |              7 |
| overpayment_amount              | float64        |            20742 |            0 |           0    |            231 |
| payment                         | int64          |            20742 |            0 |           0    |             25 |
| prepayment_amount               | int64          |            20742 |            0 |           0    |             22 |
| reporting_date_from_file        | datetime64[us] |            20742 |            0 |           0    |              1 |
| sale_date                       | str            |            20742 |            0 |           0    |            939 |
| source_file                     | str            |            20742 |            0 |           0    |              1 |
| total_paid                      | int64          |            20742 |            0 |           0    |           7098 |
| total_paid_with_adjustments_15d | int64          |            20742 |            0 |           0    |           6988 |

### Duplicate Identifier Checks

| identifier_column   |   non_null_count |   unique_count |   duplicate_value_count |
|:--------------------|-----------------:|---------------:|------------------------:|
| loan_id             |            20742 |          20742 |                       0 |

### Date Inconsistency Checks

| date_column              |   non_null_count |   invalid_date_count |   invalid_date_percent | min_date                  | max_date                  |
|:-------------------------|-----------------:|---------------------:|-----------------------:|:--------------------------|:--------------------------|
| date                     |            20742 |                    0 |                      0 | 2025-12-30 00:00:00+00:00 | 2025-12-30 00:00:00+00:00 |
| return_date              |             1744 |                    0 |                      0 | 2026-05-05 00:00:00+00:00 | 2026-05-05 00:00:00+00:00 |
| sale_date                |            20742 |                    0 |                      0 | 2023-02-08 00:00:00+00:00 | 2025-12-29 00:00:00+00:00 |
| credit_expiry            |            20742 |                    0 |                      0 | 2023-02-15 00:00:00+00:00 | 2026-09-05 00:00:00+00:00 |
| next_invoice_date        |            20742 |                    0 |                      0 | 2025-12-31 00:00:00+00:00 | 2026-01-06 00:00:00+00:00 |
| max_payment_date         |            20437 |                    0 |                      0 | 2023-02-08 00:00:00+00:00 | 2025-12-30 00:00:00+00:00 |
| reporting_date_from_file |            20742 |                    0 |                      0 | 2025-12-30 00:00:00+00:00 | 2025-12-30 00:00:00+00:00 |

### Date Source Format Checks

| column                   |   non_null_count |   iso_like_count |   slash_date_count |   dash_date_count |   timestamp_count | sample_values                     |
|:-------------------------|-----------------:|-----------------:|-------------------:|------------------:|------------------:|:----------------------------------|
| date                     |            20742 |                0 |              20742 |                 0 |                 0 | 12/30/2025                        |
| return_date              |             1744 |                0 |                  0 |                 0 |              1744 | 00:00.0                           |
| sale_date                |            20742 |                0 |              20742 |                 0 |                 0 | 10/15/2024, 8/22/2025, 7/31/2023  |
| credit_expiry            |            20742 |                0 |              20742 |                 0 |                 0 | 10/14/2025, 1/2/2026, 6/10/2024   |
| next_invoice_date        |            20742 |                0 |              20742 |                 0 |                 0 | 1/6/2026, 1/2/2026, 1/5/2026      |
| max_payment_date         |            20437 |                0 |              20437 |                 0 |                 0 | 12/23/2025, 12/25/2025, 1/28/2024 |
| reporting_date_from_file |            20742 |            20742 |                  0 |                 0 |                 0 | 2025-12-30                        |

### Currency and Numeric Inconsistency Checks

| money_column                    |   non_null_count |   formatted_value_count |   non_numeric_after_cleaning |   negative_count |   min_value |   max_value |
|:--------------------------------|-----------------:|------------------------:|-----------------------------:|-----------------:|------------:|------------:|
| total_paid                      |            20742 |                       0 |                            0 |                1 |      -20499 |      222159 |
| total_due_today                 |            20736 |                       0 |                            0 |                0 |        3099 |      334219 |
| balance                         |            20740 |                       0 |                            0 |                5 |       -1000 |      187939 |
| days_past_due                   |            20742 |                       0 |                            0 |                0 |           0 |        1048 |
| closing_balance                 |            20740 |                       0 |                            0 |                3 |          -1 |      187939 |
| arrears                         |            20742 |                       0 |                            0 |                0 |           0 |      187939 |
| payment                         |            20742 |                       0 |                            0 |                0 |           0 |        3550 |
| expected_payment                |            20742 |                       0 |                            0 |                0 |           0 |        4130 |
| first_payment                   |            20742 |                       0 |                            0 |                0 |           0 |           0 |
| first_expected_payment          |            20742 |                       0 |                            0 |                0 |           0 |           0 |
| payment_amount                  |               30 |                       0 |                            0 |                0 |         200 |        3550 |
| adjustment_amount               |               30 |                       0 |                            0 |                0 |           0 |           0 |
| prepayment_amount               |            20742 |                       0 |                            0 |                0 |           0 |       67049 |
| deposit                         |            20740 |                       0 |                            0 |                1 |          -1 |       55499 |
| weekly_rate                     |            20740 |                       0 |                            0 |                0 |         240 |        9060 |
| discount                        |            20742 |                       0 |                            0 |                0 |           0 |       86870 |
| overpayment_amount              |            20742 |                       0 |                            0 |                0 |           0 |       91254 |
| total_paid_with_adjustments_15d |            20742 |                       0 |                            0 |                1 |      -20499 |      222159 |

### Suspicious Values

| issue                        |   count | details                                                    |
|:-----------------------------|--------:|:-----------------------------------------------------------|
| unnamed_columns              |       1 | unnamed_28                                                 |
| all_null_columns             |       1 | unnamed_28                                                 |
| columns_over_50_percent_null |       4 | return_date, payment_amount, adjustment_amount, unnamed_28 |
| customer_age_outside_18_120  |   16647 | customer_age                                               |
| negative_days_past_due       |       0 | days_past_due                                              |

## Dataset: sales_customer__Sales Details

- Rows: 20,747
- Columns: 16
- Full duplicate rows: 0

### Column Profile

| column                   | dtype          |   non_null_count |   null_count |   null_percent |   unique_count |
|:-------------------------|:---------------|-----------------:|-------------:|---------------:|---------------:|
| return_date              | datetime64[us] |             1744 |        19003 |          91.59 |            530 |
| return_policy_compliance | str            |             1744 |        19003 |          91.59 |              2 |
| seller_type              | str            |            15776 |         4971 |          23.96 |              5 |
| seller                   | str            |            20670 |           77 |           0.37 |            519 |
| loan_id                  | str            |            20696 |           51 |           0.25 |          20691 |
| client_model             | str            |            20722 |           25 |           0.12 |              3 |
| loan_term                | str            |            20743 |            4 |           0.02 |              3 |
| cash_price               | float64        |            20745 |            2 |           0.01 |            259 |
| loan_price               | float64        |            20745 |            2 |           0.01 |            930 |
| model                    | str            |            20745 |            2 |           0.01 |             82 |
| product_name             | str            |            20745 |            2 |           0.01 |            132 |
| sale_type                | str            |            20745 |            2 |           0.01 |              3 |
| business_model           | str            |            20747 |            0 |           0    |              7 |
| returned                 | float64        |            20747 |            0 |           0    |              2 |
| sale_date                | datetime64[us] |            20747 |            0 |           0    |            939 |
| sale_id                  | str            |            20747 |            0 |           0    |          20747 |

### Duplicate Identifier Checks

| identifier_column   |   non_null_count |   unique_count |   duplicate_value_count |
|:--------------------|-----------------:|---------------:|------------------------:|
| sale_id             |            20747 |          20747 |                       0 |
| loan_id             |            20696 |          20691 |                       5 |

### Date Inconsistency Checks

| date_column   |   non_null_count |   invalid_date_count |   invalid_date_percent | min_date                  | max_date                  |
|:--------------|-----------------:|---------------------:|-----------------------:|:--------------------------|:--------------------------|
| sale_date     |            20747 |                    0 |                      0 | 2023-02-08 00:00:00+00:00 | 2025-12-29 00:00:00+00:00 |
| return_date   |             1744 |                    0 |                      0 | 2023-03-16 00:00:00+00:00 | 2025-12-29 00:00:00+00:00 |

### Date Source Format Checks

| column      |   non_null_count |   iso_like_count |   slash_date_count |   dash_date_count |   timestamp_count | sample_values                      |
|:------------|-----------------:|-----------------:|-------------------:|------------------:|------------------:|:-----------------------------------|
| sale_date   |            20747 |            20747 |                  0 |                 0 |                 0 | 2025-06-26, 2024-07-15, 2024-08-15 |
| return_date |             1744 |             1744 |                  0 |                 0 |                 0 | 2025-06-09, 2024-09-02, 2024-10-09 |

### Currency and Numeric Inconsistency Checks

| money_column   |   non_null_count |   formatted_value_count |   non_numeric_after_cleaning |   negative_count |   min_value |   max_value |
|:---------------|-----------------:|------------------------:|-----------------------------:|-----------------:|------------:|------------:|
| cash_price     |            20745 |                       0 |                            0 |                0 |        7999 |      215499 |
| loan_price     |            20745 |                       0 |                            0 |                0 |       15159 |      334219 |

### Suspicious Values

| issue                        |   count | details                               |
|:-----------------------------|--------:|:--------------------------------------|
| unnamed_columns              |       0 | none                                  |
| all_null_columns             |       0 | none                                  |
| columns_over_50_percent_null |       2 | return_date, return_policy_compliance |

## Dataset: sales_customer__Gender

- Rows: 49,804
- Columns: 3
- Full duplicate rows: 39,295

### Column Profile

| column      | dtype   |   non_null_count |   null_count |   null_percent |   unique_count |
|:------------|:--------|-----------------:|-------------:|---------------:|---------------:|
| loan_id     | str     |            14896 |        34908 |          70.09 |          10497 |
| gender      | str     |            49783 |           21 |           0.04 |              5 |
| citizenship | str     |            49788 |           16 |           0.03 |              3 |

### Duplicate Identifier Checks

| identifier_column   |   non_null_count |   unique_count |   duplicate_value_count |
|:--------------------|-----------------:|---------------:|------------------------:|
| loan_id             |            14896 |          10497 |                    4399 |

### Date Inconsistency Checks

_No applicable columns found._

### Date Source Format Checks

_No applicable columns found._

### Currency and Numeric Inconsistency Checks

_No applicable columns found._

### Suspicious Values

| issue                        |   count | details   |
|:-----------------------------|--------:|:----------|
| unnamed_columns              |       0 | none      |
| all_null_columns             |       0 | none      |
| columns_over_50_percent_null |       1 | loan_id   |

## Dataset: sales_customer__DOB

- Rows: 57,130
- Columns: 5
- Full duplicate rows: 0

### Column Profile

| column        | dtype   |   non_null_count |   null_count |   null_percent |   unique_count |
|:--------------|:--------|-----------------:|-------------:|---------------:|---------------:|
| loan_id       | str     |            13562 |        43568 |          76.26 |          11217 |
| date_of_birth | object  |            56921 |          209 |           0.37 |          17087 |
| createdat_utc | str     |            57130 |            0 |           0    |          57130 |
| id            | str     |            57130 |            0 |           0    |          57130 |
| provider      | str     |            57130 |            0 |           0    |              3 |

### Duplicate Identifier Checks

| identifier_column   |   non_null_count |   unique_count |   duplicate_value_count |
|:--------------------|-----------------:|---------------:|------------------------:|
| id                  |            57130 |          57130 |                       0 |
| loan_id             |            13562 |          11217 |                    2345 |

### Date Inconsistency Checks

| date_column   |   non_null_count |   invalid_date_count |   invalid_date_percent | min_date                         | max_date                         |
|:--------------|-----------------:|---------------------:|-----------------------:|:---------------------------------|:---------------------------------|
| date_of_birth |            56921 |                    0 |                      0 | 1899-11-15 21:00:00+00:00        | 2025-08-08 00:00:00+00:00        |
| createdat_utc |            57130 |                    0 |                      0 | 2024-11-19 06:20:57.157000+00:00 | 2025-12-31 09:39:38.340000+00:00 |

### Date Source Format Checks

| column        |   non_null_count |   iso_like_count |   slash_date_count |   dash_date_count |   timestamp_count | sample_values                                                                   |
|:--------------|-----------------:|-----------------:|-------------------:|------------------:|------------------:|:--------------------------------------------------------------------------------|
| date_of_birth |            56921 |            56921 |                  0 |                 0 |             56921 | 1992-01-15T00:00:00+03:00, 2002-04-13T00:00:00+03:00, 1991-05-17T00:00:00+03:00 |
| createdat_utc |            57130 |            57130 |                  0 |                 0 |             57130 | 2025-03-03T12:12:02.196Z, 2025-03-03T12:12:02.967Z, 2025-03-03T10:32:05.687Z    |

### Currency and Numeric Inconsistency Checks

_No applicable columns found._

### Suspicious Values

| issue                        |   count | details   |
|:-----------------------------|--------:|:----------|
| unnamed_columns              |       0 | none      |
| all_null_columns             |       0 | none      |
| columns_over_50_percent_null |       1 | loan_id   |

## Dataset: sales_customer__Income Level

- Rows: 22,839
- Columns: 6
- Full duplicate rows: 1,519

### Column Profile

| column                      | dtype   |   non_null_count |   null_count |   null_percent |   unique_count |
|:----------------------------|:--------|-----------------:|-------------:|---------------:|---------------:|
| loan_id                     | str     |            11885 |        10954 |          47.96 |          10609 |
| banks_received              | float64 |            22839 |            0 |           0    |          16632 |
| duration                    | float64 |            22839 |            0 |           0    |             23 |
| paybills_received_others    | float64 |            22839 |            0 |           0    |          12560 |
| persons_received_from_total | float64 |            22839 |            0 |           0    |          20993 |
| received                    | float64 |            22839 |            0 |           0    |          21191 |

### Duplicate Identifier Checks

| identifier_column   |   non_null_count |   unique_count |   duplicate_value_count |
|:--------------------|-----------------:|---------------:|------------------------:|
| loan_id             |            11885 |          10609 |                    1276 |

### Date Inconsistency Checks

_No applicable columns found._

### Date Source Format Checks

_No applicable columns found._

### Currency and Numeric Inconsistency Checks

| money_column                |   non_null_count |   formatted_value_count |   non_numeric_after_cleaning |   negative_count |   min_value |   max_value |
|:----------------------------|-----------------:|------------------------:|-----------------------------:|-----------------:|------------:|------------:|
| received                    |            22839 |                       0 |                            0 |                0 |  0          | 3.82711e+07 |
| persons_received_from_total |            22839 |                       0 |                            0 |                0 |  0          | 3.78957e+07 |
| banks_received              |            22839 |                       0 |                            0 |                0 |  0          | 2.60762e+07 |
| paybills_received_others    |            22839 |                       0 |                            0 |               35 | -1.9756e+06 | 2.20073e+07 |

### Suspicious Values

| issue                        |   count | details   |
|:-----------------------------|--------:|:----------|
| unnamed_columns              |       0 | none      |
| all_null_columns             |       0 | none      |
| columns_over_50_percent_null |       0 | none      |

## Dataset: nps__Sheet1

- Rows: 4,129
- Columns: 17
- Full duplicate rows: 0

### Column Profile

| column                                                                                                            | dtype          |   non_null_count |   null_count |   null_percent |   unique_count |
|:------------------------------------------------------------------------------------------------------------------|:---------------|-----------------:|-------------:|---------------:|---------------:|
| what_is_one_thing_we_could_do_to_improve_your_experience_with_us                                                  | object         |             1134 |         2995 |          72.54 |           1068 |
| what_is_the_main_reason_for_your_score                                                                            | object         |             1183 |         2946 |          71.35 |           1060 |
| any_other_feedback                                                                                                | object         |             1753 |         2376 |          57.54 |           1163 |
| if_yes_please_describe_the_challenge_you_faced_and_how_we_can_improve_your_experience                             | object         |             1960 |         2169 |          52.53 |           1339 |
| have_you_ever_had_your_phone_lock_despite_making_a_payment_on_time                                                | str            |             2030 |         2099 |          50.84 |              2 |
| which_communication_channel_do_you_prefer_when_contacting_mophones_for_inquiries_or_support                       | str            |             2037 |         2092 |          50.67 |              5 |
| have_you_used_the_mophones_app_moapp_to_manage_your_account_or_make_payments                                      | str            |             2060 |         2069 |          50.11 |              3 |
| have_you_experienced_any_battery_related_issues_with_your_mophones_device                                         | str            |             2081 |         2048 |          49.6  |              2 |
| have_you_ever_had_difficulty_getting_assistance_from_abc_phones_customer_support_when_needed                      | str            |             2352 |         1777 |          43.04 |              3 |
| have_you_ever_experienced_a_delay_in_your_payment_reflecting_in_your_abc_account                                  | str            |             2369 |         1760 |          42.63 |              2 |
| are_you_happy_with_the_service_and_support_provided_by_abc_phones                                                 | str            |             2608 |         1521 |          36.84 |              2 |
| are_you_happy_with_the_quality_and_performance_of_your_device                                                     | str            |             2627 |         1502 |          36.38 |              2 |
| using_a_scale_from_0_not_likely_to_10_very_likely_how_likely_are_you_to_recommend_abc_phones_to_friends_or_family | float64        |             3985 |          144 |           3.49 |             11 |
| loan_id                                                                                                           | str            |             4129 |            0 |           0    |           3532 |
| respondent_id                                                                                                     | str            |             4129 |            0 |           0    |           3756 |
| submission_id                                                                                                     | str            |             4129 |            0 |           0    |           4129 |
| submitted_at                                                                                                      | datetime64[us] |             4129 |            0 |           0    |           3087 |

### Duplicate Identifier Checks

| identifier_column   |   non_null_count |   unique_count |   duplicate_value_count |
|:--------------------|-----------------:|---------------:|------------------------:|
| submission_id       |             4129 |           4129 |                       0 |
| respondent_id       |             4129 |           3756 |                     373 |
| loan_id             |             4129 |           3532 |                     597 |

### Date Inconsistency Checks

| date_column   |   non_null_count |   invalid_date_count |   invalid_date_percent | min_date                  | max_date                  |
|:--------------|-----------------:|---------------------:|-----------------------:|:--------------------------|:--------------------------|
| submitted_at  |             4129 |                    0 |                      0 | 2025-04-22 15:15:00+00:00 | 2025-12-27 02:06:00+00:00 |

### Date Source Format Checks

| column       |   non_null_count |   iso_like_count |   slash_date_count |   dash_date_count |   timestamp_count | sample_values                                                 |
|:-------------|-----------------:|-----------------:|-------------------:|------------------:|------------------:|:--------------------------------------------------------------|
| submitted_at |             4129 |             4129 |                  0 |                 0 |              4129 | 2025-04-22 15:15:00, 2025-04-22 15:18:00, 2025-04-22 15:31:00 |

### Currency and Numeric Inconsistency Checks

_No applicable columns found._

### Suspicious Values

| issue                        |   count | details                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
|:-----------------------------|--------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| unnamed_columns              |       0 | none                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| all_null_columns             |       0 | none                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| columns_over_50_percent_null |       7 | what_is_the_main_reason_for_your_score, what_is_one_thing_we_could_do_to_improve_your_experience_with_us, if_yes_please_describe_the_challenge_you_faced_and_how_we_can_improve_your_experience, have_you_used_the_mophones_app_moapp_to_manage_your_account_or_make_payments, which_communication_channel_do_you_prefer_when_contacting_mophones_for_inquiries_or_support, have_you_ever_had_your_phone_lock_despite_making_a_payment_on_time, any_other_feedback |

## Initial Findings and Assumptions

- `loan_id` is the strongest common join key across credit, sales/customer, and NPS data.
- Credit CSV filenames provide reliable reporting snapshot dates and are captured as `reporting_date_from_file`.
- Sheets with repeated `loan_id` values should be handled as one-to-many unless business rules confirm otherwise.
- `unnamed_*` columns, high-null columns, invalid dates, and non-numeric money values require explicit cleaning rules.
- NPS records should be treated as optional enrichment because survey coverage is expected to be partial.
- Missing values are not imputed during profiling; nulls are measured and documented so cleaning rules remain auditable.
- Date parsing uses `errors='coerce'` and `utc=True` only for quality assessment; invalid parses should be retained as null plus a validation flag during cleaning.
- Currency and numeric cleaning should strip display formatting but preserve original raw columns or source files for auditability.
- Negative monetary values are flagged, not automatically removed, because they may represent adjustments, refunds, reversals, or source defects.
- `customer_age` is treated as suspicious where values fall outside 18-120; final age bands should be derived from DOB as of reporting date where possible.

## Cleaning Decision Principles

| Decision area | Rule | Justification |
|:--|:--|:--|
| Column names | Standardize to snake_case. | Consistent names make joins, validation, and downstream SQL/Python code reproducible. |
| Raw data | Keep raw files immutable. | Auditability requires the ability to reproduce every cleaned value from source. |
| Duplicate IDs | Resolve with deterministic business rules per table. | Some duplicates are legitimate repeated events or survey responses; blind deduplication can lose information. |
| Missing values | Flag and document before imputation or exclusion. | Missingness may carry business meaning, especially sparse returns, payments, adjustments, and survey fields. |
| Dates | Parse explicitly and normalize timezone handling. | Portfolio snapshots, aging, and days-past-due metrics depend on reliable dates. |
| Currency/numeric values | Strip formatting, convert to numeric, and flag invalid or negative values. | Analysts need numeric fields, but anomalies should remain visible for validation. |
| Relationships | Treat `loan_id` as the primary analytical join key. | It appears across credit, sales/customer, and NPS sources and gives the strongest cross-dataset coverage. |
