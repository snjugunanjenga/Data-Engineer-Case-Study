"""Engineer required analytical features for the ABC Phones case study.

Outputs:
    - outputs/feature_engineered_summary.csv
    - outputs/cleaned_summary.csv
    - docs/feature_engineering_report.md

The implementation keeps the logic explicit and auditable:
    - DOB and income are joined by normalized loan_id.
    - Age is calculated as at each credit reporting date.
    - Income bands use all income-related columns divided by duration.
    - Days past due is derived from source aging with a no-arrears override.
    - Risk category combines account status, arrears, days past due, and payment
      performance.
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"
DOCS_DIR = BASE_DIR / "docs"

AGE_LABELS = ["18-25", "26-35", "36-45", "46-55", "55+"]
INCOME_LABELS = [
    "Below 5,000",
    "5,000-9,999",
    "10,000-19,999",
    "20,000-29,999",
    "30,000-49,999",
    "50,000-99,999",
    "100,000-149,999",
    "150,000+",
]
INCOME_COLUMNS = [
    "received",
    "persons_received_from_total",
    "banks_received",
    "paybills_received_others",
]
FEATURE_COLUMNS = [
    "loan_id",
    "reporting_date",
    "date_of_birth",
    "age_years",
    "age_band",
    "duration",
    "total_income",
    "avg_monthly_income",
    "avg_monthly_income_band",
    "payment_due_date",
    "days_past_due",
    "risk_category",
]


def resolve_raw_dir() -> Path:
    """Find raw data whether it lives inside the submission or repo root."""
    candidates = [
        BASE_DIR / "data" / "raw",
        BASE_DIR.parent / "data" / "raw",
    ]
    for candidate in candidates:
        if (
            (candidate / "credit" / "Credit Data").exists()
            and (candidate / "sales_customer" / "Sales and Customer Data.xlsx").exists()
        ):
            return candidate

    raise FileNotFoundError(
        "Raw data folder was not found. Expected `data/raw` inside the submission "
        "folder or at the repository root."
    )


def clean_column_name(column: object) -> str:
    """Convert source column names to stable snake_case names."""
    normalized = re.sub(r"[^0-9a-zA-Z]+", "_", str(column).strip().lower())
    return re.sub(r"_+", "_", normalized).strip("_")


def standardize_columns(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.rename(columns={column: clean_column_name(column) for column in frame.columns})


def normalize_identifier(series: pd.Series) -> pd.Series:
    return series.astype("string").str.strip()


def clean_numeric(series: pd.Series) -> pd.Series:
    """Parse numbers while tolerating currency separators and symbols."""
    return pd.to_numeric(
        series.astype("string").str.replace(r"[^0-9.\-]", "", regex=True),
        errors="coerce",
    )


def load_credit_snapshots(raw_dir: Path) -> pd.DataFrame:
    """Load and standardize every credit snapshot."""
    frames = []
    for path in sorted((raw_dir / "credit" / "Credit Data").glob("*.csv")):
        reporting_date = pd.to_datetime(
            path.stem.split(" - ")[-1],
            format="%d-%m-%Y",
            errors="coerce",
        )
        frame = standardize_columns(pd.read_csv(path))
        frame["loan_id"] = normalize_identifier(frame["loan_id"])
        frame["reporting_date"] = reporting_date
        frame["snapshot_date_from_credit_file"] = reporting_date
        frame["source_file"] = path.name
        frames.append(frame)

    credit = pd.concat(frames, ignore_index=True)
    numeric_columns = [
        "arrears",
        "days_past_due",
        "payment",
        "expected_payment",
        "total_paid",
        "total_due_today",
        "balance",
        "closing_balance",
    ]
    for column in numeric_columns:
        if column in credit.columns:
            credit[column] = clean_numeric(credit[column])

    if "date" in credit.columns:
        credit["credit_snapshot_date"] = pd.to_datetime(credit["date"], errors="coerce")
    return credit


def load_dob_by_loan(raw_dir: Path) -> pd.DataFrame:
    """Select one DOB record per loan_id using the latest created timestamp."""
    dob = standardize_columns(
        pd.read_excel(raw_dir / "sales_customer" / "Sales and Customer Data.xlsx", sheet_name="DOB")
    ).dropna(how="all")
    dob = dob.dropna(subset=["loan_id"]).copy()
    dob["loan_id"] = normalize_identifier(dob["loan_id"])
    dob["date_of_birth"] = pd.to_datetime(dob["date_of_birth"], errors="coerce", utc=True)
    dob["createdat_utc"] = pd.to_datetime(dob["createdat_utc"], errors="coerce", utc=True)
    dob = (
        dob.sort_values(["loan_id", "createdat_utc"], ascending=[True, False])
        .drop_duplicates(subset=["loan_id"], keep="first")
        [["loan_id", "date_of_birth", "createdat_utc"]]
    )
    return dob


def load_income_by_loan(raw_dir: Path) -> pd.DataFrame:
    """Aggregate all income-related columns by loan_id."""
    income = standardize_columns(
        pd.read_excel(
            raw_dir / "sales_customer" / "Sales and Customer Data.xlsx",
            sheet_name="Income Level",
        )
    ).dropna(how="all")
    income = income.dropna(subset=["loan_id"]).copy()
    income["loan_id"] = normalize_identifier(income["loan_id"])

    for column in ["duration", *INCOME_COLUMNS]:
        income[column] = clean_numeric(income[column])

    income["total_income_record"] = income[INCOME_COLUMNS].sum(axis=1, min_count=1)
    income = (
        income.groupby("loan_id", as_index=False)
        .agg(
            duration=("duration", "max"),
            received=("received", "sum"),
            persons_received_from_total=("persons_received_from_total", "sum"),
            banks_received=("banks_received", "sum"),
            paybills_received_others=("paybills_received_others", "sum"),
            total_income=("total_income_record", "sum"),
            income_record_count=("loan_id", "size"),
        )
    )
    income["avg_monthly_income"] = np.where(
        income["duration"].gt(0),
        income["total_income"] / income["duration"],
        np.nan,
    )
    return income


def assign_age_band(age_years: pd.Series) -> pd.Series:
    """Band age in years using the required case-study buckets."""
    return pd.cut(
        age_years,
        bins=[17, 25, 35, 45, 55, np.inf],
        labels=AGE_LABELS,
        right=True,
    )


def assign_income_band(avg_monthly_income: pd.Series) -> pd.Series:
    """Band average monthly income using the required case-study buckets."""
    return pd.cut(
        avg_monthly_income,
        bins=[-np.inf, 4999, 9999, 19999, 29999, 49999, 99999, 149999, np.inf],
        labels=INCOME_LABELS,
        right=True,
    )


def derive_days_past_due(frame: pd.DataFrame) -> pd.Series:
    """Derive days past due with a no-arrears override.

    The credit source provides account aging but not the original overdue due
    date. To keep the derivation auditable, payment_due_date is inferred as
    reporting_date minus source aging days, then days_past_due is recalculated
    as the date difference. Records with no arrears are forced to zero.
    """
    source_dpd = frame["days_past_due"].fillna(0).clip(lower=0)
    inferred_due_date = frame["reporting_date"] - pd.to_timedelta(source_dpd, unit="D")
    frame["payment_due_date"] = inferred_due_date.where(frame["arrears"].fillna(0).gt(0))
    derived_dpd = (frame["reporting_date"] - frame["payment_due_date"]).dt.days
    return derived_dpd.where(frame["arrears"].fillna(0).gt(0), 0).fillna(0).astype("int64")


def assign_risk_category(frame: pd.DataFrame) -> pd.Series:
    """Classify credit risk using status, arrears, DPD, and payment pattern."""
    arrears = frame["arrears"].fillna(0)
    dpd = frame["days_past_due"].fillna(0)
    expected_payment = frame.get("expected_payment", pd.Series(0, index=frame.index)).fillna(0)
    payment = frame.get("payment", pd.Series(0, index=frame.index)).fillna(0)
    status_l1 = frame.get("account_status_l1", pd.Series("", index=frame.index)).astype(str).str.lower()
    status_l2 = frame.get("account_status_l2", pd.Series("", index=frame.index)).astype(str).str.lower()
    status_text = status_l1 + " " + status_l2
    missed_expected_payment = expected_payment.gt(0) & payment.lt(expected_payment)

    conditions = [
        status_text.str.contains("write off|default|fpd|fmd", regex=True)
        | dpd.ge(90)
        | arrears.ge(50_000),
        dpd.between(31, 89)
        | arrears.between(10_000, 49_999)
        | (arrears.gt(0) & missed_expected_payment),
        dpd.between(1, 30) | arrears.gt(0) | missed_expected_payment,
    ]
    choices = ["Critical", "High", "Medium"]
    return pd.Series(np.select(conditions, choices, default="Low"), index=frame.index)


def add_required_features(credit: pd.DataFrame, dob: pd.DataFrame, income: pd.DataFrame) -> pd.DataFrame:
    """Join supporting tables and create all required features."""
    features = credit.merge(dob, on="loan_id", how="left").merge(income, on="loan_id", how="left")

    dob_naive = features["date_of_birth"].dt.tz_convert(None)
    features["age_years"] = ((features["reporting_date"] - dob_naive).dt.days / 365.25).round(1)
    features["age_band"] = assign_age_band(features["age_years"])
    features["avg_monthly_income_band"] = assign_income_band(features["avg_monthly_income"])
    features["days_past_due"] = derive_days_past_due(features)
    features["risk_category"] = assign_risk_category(features)
    return features


def summarize_features(features: pd.DataFrame) -> str:
    """Create a markdown report documenting logic, assumptions, and output coverage."""
    required = ["age_band", "avg_monthly_income_band", "days_past_due", "risk_category"]
    coverage = pd.DataFrame(
        {
            "feature": required,
            "non_null_count": [int(features[column].notna().sum()) for column in required],
            "null_count": [int(features[column].isna().sum()) for column in required],
            "null_percent": [
                round(float(features[column].isna().mean() * 100), 2) for column in required
            ],
        }
    )
    risk_distribution = (
        features["risk_category"]
        .value_counts(dropna=False)
        .rename_axis("risk_category")
        .reset_index(name="record_count")
    )
    age_distribution = (
        features["age_band"].astype("string").fillna("Missing")
        .value_counts()
        .rename_axis("age_band")
        .reset_index(name="record_count")
    )
    income_distribution = (
        features["avg_monthly_income_band"].astype("string").fillna("Missing")
        .value_counts()
        .rename_axis("avg_monthly_income_band")
        .reset_index(name="record_count")
    )

    return "\n".join(
        [
            "# Feature Engineering Report",
            "",
            "## Work Completed",
            "",
            "- Loaded all five credit snapshots.",
            "- Loaded DOB and Income Level sheets from the sales/customer workbook.",
            "- Joined DOB and income attributes to credit snapshots by normalized `loan_id`.",
            "- Derived `age_band`, `avg_monthly_income_band`, `days_past_due`, and `risk_category` programmatically.",
            "- Saved full feature output to `outputs/feature_engineered_summary.csv`.",
            "- Saved a compact sample output to `outputs/cleaned_summary.csv` for downstream scripts.",
            "",
            "## Feature Logic",
            "",
            "| Feature | Logic | Bands / Values |",
            "|:--|:--|:--|",
            "| `age_band` | `age_years = (reporting_date - date_of_birth) / 365.25`; binned after joining DOB by `loan_id`. | 18-25, 26-35, 36-45, 46-55, 55+ |",
            "| `avg_monthly_income_band` | Sum `received`, `persons_received_from_total`, `banks_received`, and `paybills_received_others`; divide by `duration`. | Below 5,000; 5,000-9,999; 10,000-19,999; 20,000-29,999; 30,000-49,999; 50,000-99,999; 100,000-149,999; 150,000+ |",
            "| `days_past_due` | Infer `payment_due_date = reporting_date - source_days_past_due`; recalculate DPD as date difference; force 0 where arrears are 0. | Integer |",
            "| `risk_category` | Combine status text, arrears, DPD, and missed expected payment indicators. | Low, Medium, High, Critical |",
            "",
            "## Risk Category Rules",
            "",
            "- Critical: write-off/default/FPD/FMD status, DPD >= 90, or arrears >= 50,000.",
            "- High: DPD 31-89, arrears 10,000-49,999, or arrears plus missed expected payment.",
            "- Medium: DPD 1-30, any arrears, or missed expected payment.",
            "- Low: no risk trigger above.",
            "",
            "## Assumptions",
            "",
            "- `loan_id` is the stable join key across credit, DOB, and income records.",
            "- DOB duplicates are resolved by keeping the latest `createdat_utc` record per `loan_id`.",
            "- Income duplicates are aggregated by `loan_id`; `duration` uses the maximum observed duration and income columns are summed.",
            "- The Income Level sheet does not explicitly define employment duration units; `duration` is treated as months for the required average monthly income calculation.",
            "- The credit source does not provide an original overdue due date. `payment_due_date` is inferred from source aging so `days_past_due` remains reproducible, and records with no arrears are set to 0.",
            "- Missing DOB or income records are left null and reported; they are not imputed.",
            "",
            "## Feature Coverage",
            "",
            coverage.to_markdown(index=False),
            "",
            "## Age Band Distribution",
            "",
            age_distribution.to_markdown(index=False),
            "",
            "## Income Band Distribution",
            "",
            income_distribution.to_markdown(index=False),
            "",
            "## Risk Category Distribution",
            "",
            risk_distribution.to_markdown(index=False),
            "",
        ]
    )


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    raw_dir = resolve_raw_dir()
    credit = load_credit_snapshots(raw_dir)
    dob = load_dob_by_loan(raw_dir)
    income = load_income_by_loan(raw_dir)
    features = add_required_features(credit, dob, income)

    feature_path = OUTPUT_DIR / "feature_engineered_summary.csv"
    sample_path = OUTPUT_DIR / "cleaned_summary.csv"
    report_path = DOCS_DIR / "feature_engineering_report.md"

    output_columns = [column for column in [*FEATURE_COLUMNS, *features.columns] if column in features.columns]
    output_columns = list(dict.fromkeys(output_columns))
    features[output_columns].to_csv(feature_path, index=False)
    features[output_columns].head(5_000).to_csv(sample_path, index=False)
    report_path.write_text(summarize_features(features), encoding="utf-8")

    print(f"Wrote {feature_path}")
    print(f"Wrote {sample_path}")
    print(f"Wrote {report_path}")


if __name__ == "__main__":
    main()
