"""Portfolio analysis queries for the ABC Phones case study."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"


def main() -> None:
    path = OUTPUT_DIR / "cleaned_summary.csv"
    if not path.exists():
        raise FileNotFoundError("Run cleaning and feature engineering before analysis.")

    frame = pd.read_csv(path)
    metrics = (
        frame.assign(
            is_delinquent=lambda data: data.get("days_past_due", 0).fillna(0).astype(float) > 0
            if "days_past_due" in data
            else False
        )
        .groupby("reporting_date", dropna=False)
        .agg(
            account_count=("reporting_date", "size"),
            delinquency_rate=("is_delinquent", "mean"),
        )
        .reset_index()
    )
    metrics["delinquency_rate"] = metrics["delinquency_rate"].round(4)
    metrics.to_csv(OUTPUT_DIR / "portfolio_metrics.csv", index=False)


if __name__ == "__main__":
    main()
