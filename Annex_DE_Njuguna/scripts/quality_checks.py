"""Data quality checks for the ABC Phones case study."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str
    severity: str
    details: str


def check_not_empty(frame: pd.DataFrame) -> CheckResult:
    status = "pass" if len(frame) > 0 else "fail"
    return CheckResult("freshness_not_empty", status, "critical", f"rows={len(frame)}")


def check_duplicate_rows(frame: pd.DataFrame) -> CheckResult:
    duplicate_count = int(frame.duplicated().sum())
    status = "pass" if duplicate_count == 0 else "fail"
    return CheckResult("duplicate_rows", status, "high", f"duplicates={duplicate_count}")


def check_null_threshold(frame: pd.DataFrame, threshold: float = 0.5) -> CheckResult:
    null_rates = frame.isna().mean()
    failing_columns = null_rates[null_rates > threshold].index.tolist()
    status = "pass" if not failing_columns else "fail"
    return CheckResult("null_threshold", status, "medium", f"columns={failing_columns}")


def check_reporting_date(frame: pd.DataFrame) -> CheckResult:
    if "reporting_date" not in frame.columns:
        return CheckResult("reporting_date_exists", "fail", "critical", "missing reporting_date")
    missing_count = int(pd.to_datetime(frame["reporting_date"], errors="coerce").isna().sum())
    status = "pass" if missing_count == 0 else "fail"
    return CheckResult("reporting_date_valid", status, "high", f"invalid_dates={missing_count}")


def check_risk_category(frame: pd.DataFrame) -> CheckResult:
    if "risk_category" not in frame.columns:
        return CheckResult("risk_category_exists", "fail", "medium", "missing risk_category")
    allowed = {"Low", "Medium", "High", "Critical"}
    invalid_count = int((~frame["risk_category"].isin(allowed)).sum())
    status = "pass" if invalid_count == 0 else "fail"
    return CheckResult("risk_category_allowed", status, "medium", f"invalid={invalid_count}")


def main() -> None:
    path = OUTPUT_DIR / "cleaned_summary.csv"
    if not path.exists():
        raise FileNotFoundError("Run cleaning and feature engineering before quality checks.")

    frame = pd.read_csv(path)
    checks = [
        check_not_empty(frame),
        check_duplicate_rows(frame),
        check_null_threshold(frame),
        check_reporting_date(frame),
        check_risk_category(frame),
    ]
    results = pd.DataFrame([check.__dict__ for check in checks])
    results.to_csv(OUTPUT_DIR / "quality_check_results.csv", index=False)
    print(results.to_string(index=False))


if __name__ == "__main__":
    main()
