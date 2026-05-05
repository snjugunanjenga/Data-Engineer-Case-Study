"""Profile all ABC Phones source datasets with pandas.

The script writes a markdown report covering row counts, column types, null
rates, duplicate identifiers, suspicious values, date/currency inconsistencies,
and likely join-key coverage.
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR.parent / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "outputs"

MONEY_PATTERNS = (
    "amount",
    "arrears",
    "balance",
    "cash",
    "deposit",
    "discount",
    "due",
    "income",
    "loan_price",
    "overpayment",
    "paid",
    "payment",
    "price",
    "rate",
    "received",
)
DATE_PATTERNS = ("date", "dob", "birth", "created", "submitted", "expiry")
DATE_COLUMNS = {
    "date",
    "return_date",
    "sale_date",
    "credit_expiry",
    "next_invoice_date",
    "max_payment_date",
    "reporting_date_from_file",
    "date_of_birth",
    "created_at_utc",
    "submitted_at",
}


def clean_column_name(column: object) -> str:
    """Normalize source column names for consistent profiling."""
    normalized = re.sub(r"[^0-9a-zA-Z]+", "_", str(column).strip().lower())
    return re.sub(r"_+", "_", normalized).strip("_")


def normalize_columns(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.rename(columns={column: clean_column_name(column) for column in frame.columns})


def normalize_identifier(series: pd.Series) -> pd.Series:
    return series.astype("string").str.strip().str.upper()


def read_credit_snapshots() -> dict[str, pd.DataFrame]:
    snapshots = {}
    for path in sorted((RAW_DIR / "credit" / "Credit Data").glob("*.csv")):
        reporting_date = pd.to_datetime(
            path.stem.split(" - ")[-1],
            format="%d-%m-%Y",
            errors="coerce",
        )
        frame = normalize_columns(pd.read_csv(path))
        frame["reporting_date_from_file"] = reporting_date
        frame["source_file"] = path.name
        snapshots[path.stem] = frame
    return snapshots


def read_excel_sheets(path: Path) -> dict[str, pd.DataFrame]:
    sheets = pd.read_excel(path, sheet_name=None)
    return {sheet_name: normalize_columns(frame) for sheet_name, frame in sheets.items()}


def column_profile(frame: pd.DataFrame) -> pd.DataFrame:
    profile = pd.DataFrame(
        {
            "column": frame.columns,
            "dtype": frame.dtypes.astype(str).values,
            "non_null_count": frame.notna().sum().values,
            "null_count": frame.isna().sum().values,
            "null_percent": (frame.isna().mean() * 100).round(2).values,
            "unique_count": frame.nunique(dropna=True).values,
        }
    )
    return profile.sort_values(["null_percent", "column"], ascending=[False, True])


def duplicate_identifier_profile(frame: pd.DataFrame) -> pd.DataFrame:
    id_columns = [
        column
        for column in frame.columns
        if (
            column in {"id", "_id", "loan_id", "sale_id", "submission_id", "respondent_id"}
            or column.endswith("_id")
        )
        and not column.startswith("unnamed")
    ]
    records = []
    for column in id_columns:
        values = normalize_identifier(frame[column]).dropna()
        records.append(
            {
                "identifier_column": column,
                "non_null_count": int(values.size),
                "unique_count": int(values.nunique()),
                "duplicate_value_count": int(values.duplicated().sum()),
            }
        )
    return pd.DataFrame(records)


def date_inconsistency_profile(frame: pd.DataFrame) -> pd.DataFrame:
    date_columns = [
        column
        for column in frame.columns
        if column in DATE_COLUMNS
        or (
            any(pattern in column for pattern in DATE_PATTERNS)
            and not column.startswith("balance_due")
        )
    ]
    records = []
    for column in date_columns:
        values = frame[column].dropna()
        if values.empty:
            parseable = pd.Series(dtype="datetime64[ns]")
            invalid_count = 0
        else:
            parseable = pd.to_datetime(values, errors="coerce", utc=True)
            invalid_count = int(parseable.isna().sum())
        records.append(
            {
                "date_column": column,
                "non_null_count": int(values.size),
                "invalid_date_count": invalid_count,
                "invalid_date_percent": round((invalid_count / values.size) * 100, 2)
                if values.size
                else 0.0,
                "min_date": parseable.min() if not parseable.empty else pd.NaT,
                "max_date": parseable.max() if not parseable.empty else pd.NaT,
            }
        )
    return pd.DataFrame(records)


def currency_inconsistency_profile(frame: pd.DataFrame) -> pd.DataFrame:
    money_columns = [
        column
        for column in frame.columns
        if any(pattern in column for pattern in MONEY_PATTERNS)
        and column not in DATE_COLUMNS
        and not column.endswith("_date")
        and not any(
            excluded in column
            for excluded in ("status", "type", "model", "policy", "compliance", "question")
        )
    ]
    records = []
    for column in money_columns:
        values = frame[column].dropna()
        as_text = values.astype("string")
        cleaned = as_text.str.replace(r"[^0-9.\-]", "", regex=True)
        parsed = pd.to_numeric(cleaned, errors="coerce")
        non_numeric_count = int(parsed.isna().sum())
        formatted_count = int(as_text.str.contains(r"[,A-Za-z$KESShs]", regex=True, na=False).sum())
        negative_count = int((parsed < 0).sum())
        records.append(
            {
                "money_column": column,
                "non_null_count": int(values.size),
                "formatted_value_count": formatted_count,
                "non_numeric_after_cleaning": non_numeric_count,
                "negative_count": negative_count,
                "min_value": parsed.min(),
                "max_value": parsed.max(),
            }
        )
    return pd.DataFrame(records)


def suspicious_value_profile(frame: pd.DataFrame) -> pd.DataFrame:
    records = []
    unnamed_columns = [column for column in frame.columns if column.startswith("unnamed")]
    all_null_columns = frame.columns[frame.isna().all()].tolist()
    high_null_columns = frame.columns[frame.isna().mean().ge(0.5)].tolist()
    records.extend(
        [
            {
                "issue": "unnamed_columns",
                "count": len(unnamed_columns),
                "details": ", ".join(unnamed_columns) or "none",
            },
            {
                "issue": "all_null_columns",
                "count": len(all_null_columns),
                "details": ", ".join(all_null_columns) or "none",
            },
            {
                "issue": "columns_over_50_percent_null",
                "count": len(high_null_columns),
                "details": ", ".join(high_null_columns[:15]) or "none",
            },
        ]
    )

    if "customer_age" in frame.columns:
        age = pd.to_numeric(frame["customer_age"], errors="coerce")
        invalid_age = int(age.dropna().lt(18).sum() + age.dropna().gt(120).sum())
        records.append(
            {
                "issue": "customer_age_outside_18_120",
                "count": invalid_age,
                "details": "customer_age",
            }
        )

    if "days_past_due" in frame.columns:
        dpd = pd.to_numeric(frame["days_past_due"], errors="coerce")
        records.append(
            {
                "issue": "negative_days_past_due",
                "count": int(dpd.dropna().lt(0).sum()),
                "details": "days_past_due",
            }
        )

    return pd.DataFrame(records)


def likely_join_key_profile(datasets: dict[str, pd.DataFrame]) -> pd.DataFrame:
    records = []
    loan_id_sets = {}
    for name, frame in datasets.items():
        if "loan_id" in frame.columns:
            values = normalize_identifier(frame["loan_id"]).dropna()
            loan_id_sets[name] = set(values)
            records.append(
                {
                    "dataset": name,
                    "join_key": "loan_id",
                    "non_null_count": len(values),
                    "unique_count": len(loan_id_sets[name]),
                    "duplicate_value_count": int(values.duplicated().sum()),
                }
            )

    credit_keys = set().union(
        *[values for name, values in loan_id_sets.items() if name.startswith("credit__")]
    )
    for name, keys in loan_id_sets.items():
        if name.startswith("credit__"):
            continue
        matched = len(keys & credit_keys)
        records.append(
            {
                "dataset": name,
                "join_key": "loan_id_to_credit",
                "non_null_count": len(keys),
                "unique_count": matched,
                "duplicate_value_count": len(keys - credit_keys),
            }
        )
    return pd.DataFrame(records)


def markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No applicable columns found._"
    return frame.to_markdown(index=False)


def dataset_section(name: str, frame: pd.DataFrame) -> str:
    return "\n".join(
        [
            f"## Dataset: {name}",
            "",
            f"- Rows: {len(frame):,}",
            f"- Columns: {len(frame.columns):,}",
            f"- Full duplicate rows: {int(frame.duplicated().sum()):,}",
            "",
            "### Column Profile",
            "",
            markdown_table(column_profile(frame)),
            "",
            "### Duplicate Identifier Checks",
            "",
            markdown_table(duplicate_identifier_profile(frame)),
            "",
            "### Date Inconsistency Checks",
            "",
            markdown_table(date_inconsistency_profile(frame)),
            "",
            "### Currency and Numeric Inconsistency Checks",
            "",
            markdown_table(currency_inconsistency_profile(frame)),
            "",
            "### Suspicious Values",
            "",
            markdown_table(suspicious_value_profile(frame)),
            "",
        ]
    )


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    credit_snapshots = read_credit_snapshots()
    sales_sheets = read_excel_sheets(RAW_DIR / "sales_customer" / "Sales and Customer Data.xlsx")
    nps_sheets = read_excel_sheets(RAW_DIR / "nps" / "NPS Data (1).xlsx")

    datasets = {
        **{f"credit__{name}": frame for name, frame in credit_snapshots.items()},
        **{f"sales_customer__{name}": frame for name, frame in sales_sheets.items()},
        **{f"nps__{name}": frame for name, frame in nps_sheets.items()},
    }

    report_sections = [
        "# Data Quality Report",
        "",
        "## Scope",
        "",
        "This report profiles all credit snapshots, all sheets in the sales/customer workbook, "
        "and the NPS survey workbook using pandas.",
        "",
        "## Likely Join Keys and Relationship Coverage",
        "",
        markdown_table(likely_join_key_profile(datasets)),
        "",
    ]
    report_sections.extend(dataset_section(name, frame) for name, frame in datasets.items())
    report_sections.extend(
        [
            "## Initial Findings and Assumptions",
            "",
            "- `loan_id` is the strongest common join key across credit, sales/customer, and NPS data.",
            "- Credit CSV filenames provide reliable reporting snapshot dates and are captured as `reporting_date_from_file`.",
            "- Sheets with repeated `loan_id` values should be handled as one-to-many unless business rules confirm otherwise.",
            "- `unnamed_*` columns, high-null columns, invalid dates, and non-numeric money values require explicit cleaning rules.",
            "- NPS records should be treated as optional enrichment because survey coverage is expected to be partial.",
            "",
        ]
    )

    report_path = OUTPUT_DIR / "data_quality_report.md"
    report_path.write_text("\n".join(report_sections), encoding="utf-8")
    print(f"Wrote {report_path}")


if __name__ == "__main__":
    main()
