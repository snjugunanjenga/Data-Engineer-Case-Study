# Data Quality Report

## Scope

This report profiles all credit snapshots, all sheets in the sales/customer workbook, and the NPS survey workbook using pandas.

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

- Rows: 1,048,575
- Columns: 16
- Full duplicate rows: 1,027,827

### Column Profile

| column                   | dtype          |   non_null_count |   null_count |   null_percent |   unique_count |
|:-------------------------|:---------------|-----------------:|-------------:|---------------:|---------------:|
| return_date              | datetime64[us] |             1744 |      1046831 |          99.83 |            530 |
| return_policy_compliance | str            |             1744 |      1046831 |          99.83 |              2 |
| seller_type              | str            |            15776 |      1032799 |          98.5  |              5 |
| loan_id                  | str            |            20696 |      1027879 |          98.03 |          20691 |
| seller                   | str            |            20670 |      1027905 |          98.03 |            519 |
| business_model           | str            |            20747 |      1027828 |          98.02 |              7 |
| cash_price               | float64        |            20745 |      1027830 |          98.02 |            259 |
| client_model             | str            |            20722 |      1027853 |          98.02 |              3 |
| loan_price               | float64        |            20745 |      1027830 |          98.02 |            930 |
| loan_term                | str            |            20743 |      1027832 |          98.02 |              3 |
| model                    | str            |            20745 |      1027830 |          98.02 |             82 |
| product_name             | str            |            20745 |      1027830 |          98.02 |            132 |
| returned                 | float64        |            20747 |      1027828 |          98.02 |              2 |
| sale_date                | datetime64[us] |            20747 |      1027828 |          98.02 |            939 |
| sale_id                  | str            |            20747 |      1027828 |          98.02 |          20747 |
| sale_type                | str            |            20745 |      1027830 |          98.02 |              3 |

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

### Currency and Numeric Inconsistency Checks

| money_column   |   non_null_count |   formatted_value_count |   non_numeric_after_cleaning |   negative_count |   min_value |   max_value |
|:---------------|-----------------:|------------------------:|-----------------------------:|-----------------:|------------:|------------:|
| cash_price     |            20745 |                       0 |                            0 |                0 |        7999 |      215499 |
| loan_price     |            20745 |                       0 |                            0 |                0 |       15159 |      334219 |

### Suspicious Values

| issue                        |   count | details                                                                                                                                                                                   |
|:-----------------------------|--------:|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| unnamed_columns              |       0 | none                                                                                                                                                                                      |
| all_null_columns             |       0 | none                                                                                                                                                                                      |
| columns_over_50_percent_null |      16 | sale_id, sale_date, returned, return_date, sale_type, seller, seller_type, return_policy_compliance, cash_price, loan_price, client_model, business_model, loan_term, product_name, model |

## Dataset: sales_customer__Gender

- Rows: 1,048,575
- Columns: 3
- Full duplicate rows: 1,038,065

### Column Profile

| column      | dtype   |   non_null_count |   null_count |   null_percent |   unique_count |
|:------------|:--------|-----------------:|-------------:|---------------:|---------------:|
| loan_id     | str     |            14896 |      1033679 |          98.58 |          10497 |
| citizenship | str     |            49788 |       998787 |          95.25 |              3 |
| gender      | str     |            49783 |       998792 |          95.25 |              5 |

### Duplicate Identifier Checks

| identifier_column   |   non_null_count |   unique_count |   duplicate_value_count |
|:--------------------|-----------------:|---------------:|------------------------:|
| loan_id             |            14896 |          10497 |                    4399 |

### Date Inconsistency Checks

_No applicable columns found._

### Currency and Numeric Inconsistency Checks

_No applicable columns found._

### Suspicious Values

| issue                        |   count | details                      |
|:-----------------------------|--------:|:-----------------------------|
| unnamed_columns              |       0 | none                         |
| all_null_columns             |       0 | none                         |
| columns_over_50_percent_null |       3 | loan_id, citizenship, gender |

## Dataset: sales_customer__DOB

- Rows: 1,048,575
- Columns: 5
- Full duplicate rows: 991,444

### Column Profile

| column        | dtype   |   non_null_count |   null_count |   null_percent |   unique_count |
|:--------------|:--------|-----------------:|-------------:|---------------:|---------------:|
| loan_id       | str     |            13562 |      1035013 |          98.71 |          11217 |
| date_of_birth | object  |            56921 |       991654 |          94.57 |          17087 |
| createdat_utc | str     |            57130 |       991445 |          94.55 |          57130 |
| id            | str     |            57130 |       991445 |          94.55 |          57130 |
| provider      | str     |            57130 |       991445 |          94.55 |              3 |

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

### Currency and Numeric Inconsistency Checks

_No applicable columns found._

### Suspicious Values

| issue                        |   count | details                                             |
|:-----------------------------|--------:|:----------------------------------------------------|
| unnamed_columns              |       0 | none                                                |
| all_null_columns             |       0 | none                                                |
| columns_over_50_percent_null |       5 | id, provider, date_of_birth, loan_id, createdat_utc |

## Dataset: sales_customer__Income Level

- Rows: 1,048,575
- Columns: 6
- Full duplicate rows: 1,027,254

### Column Profile

| column                      | dtype   |   non_null_count |   null_count |   null_percent |   unique_count |
|:----------------------------|:--------|-----------------:|-------------:|---------------:|---------------:|
| loan_id                     | str     |            11885 |      1036690 |          98.87 |          10609 |
| banks_received              | float64 |            22839 |      1025736 |          97.82 |          16632 |
| duration                    | float64 |            22839 |      1025736 |          97.82 |             23 |
| paybills_received_others    | float64 |            22839 |      1025736 |          97.82 |          12560 |
| persons_received_from_total | float64 |            22839 |      1025736 |          97.82 |          20993 |
| received                    | float64 |            22839 |      1025736 |          97.82 |          21191 |

### Duplicate Identifier Checks

| identifier_column   |   non_null_count |   unique_count |   duplicate_value_count |
|:--------------------|-----------------:|---------------:|------------------------:|
| loan_id             |            11885 |          10609 |                    1276 |

### Date Inconsistency Checks

_No applicable columns found._

### Currency and Numeric Inconsistency Checks

| money_column                |   non_null_count |   formatted_value_count |   non_numeric_after_cleaning |   negative_count |   min_value |   max_value |
|:----------------------------|-----------------:|------------------------:|-----------------------------:|-----------------:|------------:|------------:|
| received                    |            22839 |                       0 |                            0 |                0 |  0          | 3.82711e+07 |
| persons_received_from_total |            22839 |                       0 |                            0 |                0 |  0          | 3.78957e+07 |
| banks_received              |            22839 |                       0 |                            0 |                0 |  0          | 2.60762e+07 |
| paybills_received_others    |            22839 |                       0 |                            0 |               35 | -1.9756e+06 | 2.20073e+07 |

### Suspicious Values

| issue                        |   count | details                                                                                            |
|:-----------------------------|--------:|:---------------------------------------------------------------------------------------------------|
| unnamed_columns              |       0 | none                                                                                               |
| all_null_columns             |       0 | none                                                                                               |
| columns_over_50_percent_null |       6 | loan_id, duration, received, persons_received_from_total, banks_received, paybills_received_others |

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

### Currency and Numeric Inconsistency Checks

| money_column                                                                     |   non_null_count |   formatted_value_count |   non_numeric_after_cleaning |   negative_count | min_value   | max_value   |
|:---------------------------------------------------------------------------------|-----------------:|------------------------:|-----------------------------:|-----------------:|:------------|:------------|
| have_you_ever_experienced_a_delay_in_your_payment_reflecting_in_your_abc_account |             2369 |                    2369 |                         2369 |                0 | <NA>        | <NA>        |
| have_you_used_the_mophones_app_moapp_to_manage_your_account_or_make_payments     |             2060 |                    2060 |                         2060 |                0 | <NA>        | <NA>        |
| have_you_ever_had_your_phone_lock_despite_making_a_payment_on_time               |             2030 |                    2030 |                         2030 |                0 | <NA>        | <NA>        |

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
