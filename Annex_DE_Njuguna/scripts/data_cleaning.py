"""Clean and standardize source data for the ABC Phones case study."""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR.parent / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "outputs"


def clean_column_name(column: str) -> str:
    column = re.sub(r"[^0-9a-zA-Z]+", "_", str(column).strip().lower())
    return re.sub(r"_+", "_", column).strip("_")


def standardize_columns(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.rename(columns={column: clean_column_name(column) for column in frame.columns})


def clean_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(
        series.astype(str).str.replace(r"[^0-9.\-]", "", regex=True),
        errors="coerce",
    )


def load_credit_snapshots() -> pd.DataFrame:
    frames = []
    for path in sorted((RAW_DIR / "credit" / "Credit Data").glob("*.csv")):
        reporting_date = pd.to_datetime(
            path.stem.split(" - ")[-1],
            format="%d-%m-%Y",
            errors="coerce",
        )
        frame = standardize_columns(pd.read_csv(path))
        frame["reporting_date"] = reporting_date
        frame["source_file"] = path.name
        frames.append(frame)
    return pd.concat(frames, ignore_index=True)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    credit = load_credit_snapshots()
    credit = credit.drop_duplicates()
    credit.head(1000).to_csv(OUTPUT_DIR / "cleaned_summary.csv", index=False)


if __name__ == "__main__":
    main()
