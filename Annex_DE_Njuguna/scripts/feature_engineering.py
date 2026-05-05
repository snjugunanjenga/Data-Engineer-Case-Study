"""Feature engineering logic for the ABC Phones case study."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"


def assign_age_band(age_years: pd.Series) -> pd.Series:
    return pd.cut(
        age_years,
        bins=[17, 25, 35, 45, 55, np.inf],
        labels=["18-25", "26-35", "36-45", "46-55", "55+"],
    )


def assign_income_band(avg_monthly_income: pd.Series) -> pd.Series:
    return pd.cut(
        avg_monthly_income,
        bins=[-np.inf, 4999, 9999, 19999, 29999, 49999, 99999, 149999, np.inf],
        labels=[
            "Below 5,000",
            "5,000-9,999",
            "10,000-19,999",
            "20,000-29,999",
            "30,000-49,999",
            "50,000-99,999",
            "100,000-149,999",
            "150,000+",
        ],
    )


def assign_risk_category(frame: pd.DataFrame) -> pd.Series:
    arrears = frame.get("arrears_amount", pd.Series(0, index=frame.index)).fillna(0)
    days_past_due = frame.get("days_past_due", pd.Series(0, index=frame.index)).fillna(0)
    status = frame.get("account_status", pd.Series("", index=frame.index)).astype(str).str.lower()

    conditions = [
        status.str.contains("write|default|closed_bad", regex=True) | (days_past_due >= 90),
        (arrears > 0) | days_past_due.between(31, 89),
        days_past_due.between(1, 30),
    ]
    choices = ["Critical", "High", "Medium"]
    return pd.Series(np.select(conditions, choices, default="Low"), index=frame.index)


def main() -> None:
    cleaned_path = OUTPUT_DIR / "cleaned_summary.csv"
    if not cleaned_path.exists():
        raise FileNotFoundError("Run scripts/data_cleaning.py before feature engineering.")

    frame = pd.read_csv(cleaned_path)
    if {"date_of_birth", "reporting_date"}.issubset(frame.columns):
        dob = pd.to_datetime(frame["date_of_birth"], errors="coerce")
        reporting_date = pd.to_datetime(frame["reporting_date"], errors="coerce")
        frame["age_years"] = ((reporting_date - dob).dt.days / 365.25).round(1)
        frame["age_band"] = assign_age_band(frame["age_years"])

    frame["risk_category"] = assign_risk_category(frame)
    frame.to_csv(cleaned_path, index=False)


if __name__ == "__main__":
    main()
