# Portfolio, NPS, and Data Gaps Analysis

## Question 3A: Portfolio Health

Selected metrics:

| reporting_date   |   account_count |   total_records |   delinquency_rate |   write_off_rate |   average_collection_rate |   critical_risk_rate |   average_days_past_due |   total_arrears |   total_balance |
|:-----------------|----------------:|----------------:|-------------------:|-----------------:|--------------------------:|---------------------:|------------------------:|----------------:|----------------:|
| 2025-01-01       |            8935 |            8935 |             0.4214 |           0.1361 |                    0.2247 |               0.3149 |                 71.8009 |     9.84162e+07 |     3.42087e+08 |
| 2025-03-30       |           11024 |           11024 |             0.4413 |           0.1616 |                    0.213  |               0.3439 |                 90.3478 |     1.48889e+08 |     3.99987e+08 |
| 2025-06-30       |           13891 |           13891 |             0.4342 |           0.1728 |                    0.2178 |               0.355  |                104.337  |     2.04016e+08 |     4.78068e+08 |
| 2025-09-30       |           16864 |           16864 |             0.4395 |           0.1832 |                    0.2126 |               0.3582 |                119.1    |     2.54933e+08 |     5.46662e+08 |
| 2025-12-30       |           20742 |           20742 |             0.4527 |           0.1804 |                    0.0012 |               0.3561 |                128.103  |     3.04509e+08 |     6.68548e+08 |

Key trend findings:

- Account count increased from 8,935 to 20,742 across the available reporting snapshots.
- Delinquency rate moved from 42.1% to 45.3%.
- Write-off rate moved from 13.6% to 18.0%.
- Critical-risk share moved from 31.5% to 35.6%.
- Average collection rate moved from 22.5% to 0.1%.

Meaningful risk segment:

- `age_band` = `55+` has an average critical-risk rate of 12.8%, 22.1% below the portfolio average.

## Question 3B: Credit Outcomes x Customer Experience

NPS match coverage: 3,985 of 3,985 valid NPS responses matched to a credit account (100.0%).

Average NPS by risk category:

| risk_category   |   responses |   avg_nps |   detractor_rate |   avg_days_past_due |
|:----------------|------------:|----------:|-----------------:|--------------------:|
| Low             |        2531 |    7.0344 |           0.3441 |              0      |
| Medium          |         607 |    7.0181 |           0.3394 |              4.117  |
| High            |         392 |    6.5842 |           0.3776 |             24.5408 |
| Critical        |         455 |    5.2088 |           0.5363 |            201.609  |

Delinquency and customer experience:

| is_delinquent   |   responses |   avg_nps |   detractor_rate |   payment_delay_rate |   phone_lock_rate |   support_difficulty_rate |
|:----------------|------------:|----------:|-----------------:|---------------------:|------------------:|--------------------------:|
| False           |        3065 |    7.0186 |           0.3432 |             0.297722 |          0.27352  |                  0.282716 |
| True            |         920 |    5.9815 |           0.4533 |             0.327586 |          0.291765 |                  0.352941 |

Experience issues by NPS group:

| nps_group   |   responses |   delinquency_rate |   avg_days_past_due |   payment_delay_rate |   phone_lock_rate |   support_difficulty_rate |
|:------------|------------:|-------------------:|--------------------:|---------------------:|------------------:|--------------------------:|
| Detractor   |        1469 |           0.283867 |             41.7338 |             0.406863 |          0.380544 |                  0.531507 |
| Passive     |         811 |           0.187423 |             15.6745 |             0.289941 |          0.265589 |                  0.2277   |
| Promoter    |        1705 |           0.205865 |             17.4968 |             0.231064 |          0.202673 |                  0.146262 |

Interpretation:

- Lower-quality credit outcomes are proxied by higher risk category, delinquency, write-off status, and higher days past due because no explicit credit score is present.
- Low-risk customers average NPS of 7.03; critical-risk customers average NPS of 5.21.
- Customer-reported payment delays, payment-related phone locks, and support difficulty are the strongest operational signals to inspect for tension between collections effectiveness and satisfaction.

Recommendation:

- Create a targeted "payment reflection and unlock assurance" workflow for delinquent or recently paid customers: reconcile payments daily, proactively confirm reflected payments, suppress avoidable locks, and route unresolved cases to a collections-support queue. This directly targets repayment behavior and the experience issues visible in NPS.

## Question 3C: Data Gaps and Future Improvements

Missing:

- Employment type, location, device usage/lock event logs, transaction-level payment records, collection contact history, and explicit credit score are not available.
- NPS does not cover every credit customer and therefore should remain optional enrichment rather than a filtering join.

Inconsistent:

- Customer attributes are split across workbook sheets with repeated `loan_id` values.
- Income calculation fields and duration require business definition before they can be treated as a production credit-affordability feature.
- Some credit fields show negative balances/payments and high-null return/payment-adjustment fields.

Ambiguous:

- `account_status_l1` and `account_status_l2` encode several lifecycle and risk concepts but lack a formal hierarchy.
- `customer_age` in credit snapshots does not behave like age in years, so DOB-derived age is preferred.
- Payment due date is not explicitly available; days past due is inferred from source aging and arrears.

Future improvements:

1. Capture transaction-level payments with due date, payment timestamp, reflection timestamp, lock/unlock timestamp, and channel.
2. Create a governed customer/account dimension with one stable `loan_id`, customer ID, DOB, gender, employment type, location, and effective dates.
3. Publish a controlled account-status mapping table that defines lifecycle status, delinquency bucket, write-off flag, and risk severity.
