# Feature Engineering Report

## Work Completed

- Loaded all five credit snapshots.
- Loaded DOB and Income Level sheets from the sales/customer workbook.
- Joined DOB and income attributes to credit snapshots by normalized `loan_id`.
- Derived `age_band`, `avg_monthly_income_band`, `days_past_due`, and `risk_category` programmatically.
- Saved full feature output to `outputs/feature_engineered_summary.csv`.
- Saved a compact sample output to `outputs/cleaned_summary.csv` for downstream scripts.

## Feature Logic

| Feature | Logic | Bands / Values |
|:--|:--|:--|
| `age_band` | `age_years = (reporting_date - date_of_birth) / 365.25`; binned after joining DOB by `loan_id`. | 18-25, 26-35, 36-45, 46-55, 55+ |
| `avg_monthly_income_band` | Sum `received`, `persons_received_from_total`, `banks_received`, and `paybills_received_others`; divide by `duration`. | Below 5,000; 5,000-9,999; 10,000-19,999; 20,000-29,999; 30,000-49,999; 50,000-99,999; 100,000-149,999; 150,000+ |
| `days_past_due` | Infer `payment_due_date = reporting_date - source_days_past_due`; recalculate DPD as date difference; force 0 where arrears are 0. | Integer |
| `risk_category` | Combine status text, arrears, DPD, and missed expected payment indicators. | Low, Medium, High, Critical |

## Risk Category Rules

- Critical: write-off/default/FPD/FMD status, DPD >= 90, or arrears >= 50,000.
- High: DPD 31-89, arrears 10,000-49,999, or arrears plus missed expected payment.
- Medium: DPD 1-30, any arrears, or missed expected payment.
- Low: no risk trigger above.

## Assumptions

- `loan_id` is the stable join key across credit, DOB, and income records.
- DOB duplicates are resolved by keeping the latest `createdat_utc` record per `loan_id`.
- Income duplicates are aggregated by `loan_id`; `duration` uses the maximum observed duration and income columns are summed.
- The Income Level sheet does not explicitly define employment duration units; `duration` is treated as months for the required average monthly income calculation.
- The credit source does not provide an original overdue due date. `payment_due_date` is inferred from source aging so `days_past_due` remains reproducible, and records with no arrears are set to 0.
- Missing DOB or income records are left null and reported; they are not imputed.

## Feature Coverage

| feature                 |   non_null_count |   null_count |   null_percent |
|:------------------------|-----------------:|-------------:|---------------:|
| age_band                |            27770 |        43686 |          61.14 |
| avg_monthly_income_band |            26162 |        45294 |          63.39 |
| days_past_due           |            71456 |            0 |           0    |
| risk_category           |            71456 |            0 |           0    |

## Age Band Distribution

| age_band   |   record_count |
|:-----------|---------------:|
| Missing    |          43686 |
| 26-35      |          15635 |
| 36-45      |           5313 |
| 18-25      |           4908 |
| 46-55      |           1503 |
| 55+        |            411 |

## Income Band Distribution

| avg_monthly_income_band   |   record_count |
|:--------------------------|---------------:|
| Missing                   |          45294 |
| 150,000+                  |          11502 |
| 50,000-99,999             |           5806 |
| 100,000-149,999           |           3736 |
| 30,000-49,999             |           3008 |
| 20,000-29,999             |           1188 |
| 10,000-19,999             |            649 |
| 5,000-9,999               |            186 |
| Below 5,000               |             87 |

## Risk Category Distribution

| risk_category   |   record_count |
|:----------------|---------------:|
| Low             |          28515 |
| Critical        |          24964 |
| Medium          |          11487 |
| High            |           6490 |
