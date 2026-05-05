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
OUTPUT_DIR = BASE_DIR / "outputs"
DOCS_DIR = BASE_DIR / "docs"

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
            and (candidate / "nps" / "NPS Data (1).xlsx").exists()
        ):
            return candidate

    expected_paths = "\n".join(str(path) for path in candidates)
    raise FileNotFoundError(
        "Raw data folder was not found. Expected one of these layouts:\n"
        f"{expected_paths}\n\n"
        "Required files:\n"
        "- credit/Credit Data/*.csv\n"
        "- sales_customer/Sales and Customer Data.xlsx\n"
        "- nps/NPS Data (1).xlsx"
    )


def clean_column_name(column: object) -> str:
    """Normalize source column names for consistent profiling."""
    normalized = re.sub(r"[^0-9a-zA-Z]+", "_", str(column).strip().lower())
    return re.sub(r"_+", "_", normalized).strip("_")


def normalize_columns(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.rename(columns={column: clean_column_name(column) for column in frame.columns})


def normalize_identifier(series: pd.Series) -> pd.Series:
    return series.astype("string").str.strip().str.upper()


def read_credit_snapshots(raw_dir: Path) -> dict[str, pd.DataFrame]:
    snapshots = {}
    for path in sorted((raw_dir / "credit" / "Credit Data").glob("*.csv")):
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
    return {
        sheet_name: normalize_columns(frame.dropna(how="all"))
        for sheet_name, frame in sheets.items()
    }


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
        and not column.startswith(("have_", "what_", "are_", "if_", "which_", "any_"))
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


def source_dataset_summary(datasets: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Summarize the three provided source datasets at case-study level."""
    groups = {
        "credit": [name for name in datasets if name.startswith("credit__")],
        "sales_customer": [name for name in datasets if name.startswith("sales_customer__")],
        "nps": [name for name in datasets if name.startswith("nps__")],
    }
    records = []
    for source_dataset, names in groups.items():
        row_count = sum(len(datasets[name]) for name in names)
        all_columns = sorted({column for name in names for column in datasets[name].columns})
        records.append(
            {
                "source_dataset": source_dataset,
                "tables_or_sheets_profiled": len(names),
                "total_rows_profiled": row_count,
                "distinct_columns_observed": len(all_columns),
                "profiled_objects": ", ".join(names),
            }
        )
    return pd.DataFrame(records)


def value_format_profile(frame: pd.DataFrame) -> pd.DataFrame:
    """Profile date-like source value formats before cleaning."""
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
        values = frame[column].dropna().astype("string").str.strip()
        iso_count = int(values.str.match(r"^\d{4}-\d{2}-\d{2}", na=False).sum())
        slash_date_count = int(values.str.match(r"^\d{1,2}/\d{1,2}/\d{2,4}", na=False).sum())
        dash_date_count = int(values.str.match(r"^\d{1,2}-\d{1,2}-\d{2,4}", na=False).sum())
        timestamp_count = int(values.str.contains(r"\d{2}:\d{2}", regex=True, na=False).sum())
        records.append(
            {
                "column": column,
                "non_null_count": int(values.size),
                "iso_like_count": iso_count,
                "slash_date_count": slash_date_count,
                "dash_date_count": dash_date_count,
                "timestamp_count": timestamp_count,
                "sample_values": ", ".join(values.drop_duplicates().head(3).astype(str)),
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


def summarize_dataset_issues(name: str, frame: pd.DataFrame) -> list[dict[str, object]]:
    issues = []

    duplicate_ids = duplicate_identifier_profile(frame)
    for _, row in duplicate_ids.iterrows():
        if row["duplicate_value_count"] > 0:
            issues.append(
                {
                    "dataset": name,
                    "issue_type": "duplicate_identifier",
                    "field_or_rule": row["identifier_column"],
                    "affected_count": int(row["duplicate_value_count"]),
                    "cleaning_decision": "Deduplicate only after selecting a deterministic business rule, such as latest timestamp or most complete record.",
                    "justification": "Blind row dropping can remove legitimate one-to-many events or survey responses.",
                }
            )

    for _, row in suspicious_value_profile(frame).iterrows():
        if row["count"] > 0:
            issue = row["issue"]
            if issue == "unnamed_columns":
                decision = "Drop unnamed columns when they are empty or have no data dictionary definition."
                justification = "Unnamed columns are usually spreadsheet artifacts and cannot be interpreted reliably."
            elif issue == "columns_over_50_percent_null":
                decision = "Retain high-null business fields but add missingness flags before analysis."
                justification = "High-null fields such as return or adjustment amounts can be sparse by design and still analytically meaningful."
            elif issue == "customer_age_outside_18_120":
                decision = "Do not use `customer_age` as age in years until its unit is confirmed; derive age from DOB where available."
                justification = "Observed values exceed normal human age ranges, suggesting a different unit or source-system defect."
            else:
                decision = "Quarantine or flag affected records for review before downstream use."
                justification = "Suspicious values need traceability so analysts can include or exclude them deliberately."
            issues.append(
                {
                    "dataset": name,
                    "issue_type": issue,
                    "field_or_rule": row["details"],
                    "affected_count": int(row["count"]),
                    "cleaning_decision": decision,
                    "justification": justification,
                }
            )

    for _, row in currency_inconsistency_profile(frame).iterrows():
        if row["non_numeric_after_cleaning"] > 0 or row["negative_count"] > 0:
            issues.append(
                {
                    "dataset": name,
                    "issue_type": "numeric_currency_anomaly",
                    "field_or_rule": row["money_column"],
                    "affected_count": int(row["non_numeric_after_cleaning"] + row["negative_count"]),
                    "cleaning_decision": "Parse numeric/currency fields after stripping formatting, then flag negative or non-numeric values for business validation.",
                    "justification": "Negative balances or payments may be refunds/adjustments, but they should not be silently coerced or dropped.",
                }
            )

    for _, row in date_inconsistency_profile(frame).iterrows():
        if row["invalid_date_count"] > 0:
            issues.append(
                {
                    "dataset": name,
                    "issue_type": "invalid_date",
                    "field_or_rule": row["date_column"],
                    "affected_count": int(row["invalid_date_count"]),
                    "cleaning_decision": "Parse dates with explicit UTC normalization and preserve invalid parses as null plus an error flag.",
                    "justification": "Date assumptions affect snapshot aging, arrears, and time-series trend analysis.",
                }
            )

    return issues


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


def relationship_analysis(datasets: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Analyze join keys, cardinality, and foreign-key integrity."""
    loan_id_sets = {}
    row_counts = {}
    duplicate_counts = {}
    for name, frame in datasets.items():
        if "loan_id" not in frame.columns:
            continue
        values = normalize_identifier(frame["loan_id"]).dropna()
        loan_id_sets[name] = set(values)
        row_counts[name] = len(values)
        duplicate_counts[name] = int(values.duplicated().sum())

    credit_dataset_names = [name for name in loan_id_sets if name.startswith("credit__")]
    credit_keys = set().union(*(loan_id_sets[name] for name in credit_dataset_names))
    sales_keys = loan_id_sets.get("sales_customer__Sales Details", set())

    records = []
    for name, keys in loan_id_sets.items():
        if name.startswith("credit__"):
            parent_name = "credit_union"
            parent_keys = credit_keys
        elif name == "sales_customer__Sales Details":
            parent_name = "credit_union"
            parent_keys = credit_keys
        elif name.startswith("sales_customer__"):
            parent_name = "sales_customer__Sales Details"
            parent_keys = sales_keys
        else:
            parent_name = "credit_union"
            parent_keys = credit_keys

        matched_keys = keys & parent_keys
        orphan_keys = keys - parent_keys
        if duplicate_counts[name] == 0 and len(orphan_keys) == 0:
            cardinality = "one-to-one candidate"
        elif duplicate_counts[name] == 0:
            cardinality = "one-to-zero-or-one candidate with orphan keys"
        else:
            cardinality = "many-to-one or repeated-event relationship"

        records.append(
            {
                "child_dataset": name,
                "parent_dataset": parent_name,
                "join_key": "loan_id",
                "child_rows_with_key": row_counts[name],
                "child_unique_keys": len(keys),
                "child_duplicate_key_rows": duplicate_counts[name],
                "matched_parent_keys": len(matched_keys),
                "orphan_child_keys": len(orphan_keys),
                "foreign_key_integrity_percent": round(
                    (len(matched_keys) / len(keys)) * 100, 2
                )
                if keys
                else 0.0,
                "cardinality_assessment": cardinality,
            }
        )
    return pd.DataFrame(records)


def issue_summary(datasets: dict[str, pd.DataFrame]) -> pd.DataFrame:
    records = []
    for name, frame in datasets.items():
        records.extend(summarize_dataset_issues(name, frame))
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
            "### Date Source Format Checks",
            "",
            markdown_table(value_format_profile(frame)),
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
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    raw_dir = resolve_raw_dir()

    credit_snapshots = read_credit_snapshots(raw_dir)
    sales_sheets = read_excel_sheets(raw_dir / "sales_customer" / "Sales and Customer Data.xlsx")
    nps_sheets = read_excel_sheets(raw_dir / "nps" / "NPS Data (1).xlsx")

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
        f"- Raw data directory: `{raw_dir}`",
        "",
        "## Work Performed",
        "",
        "- Loaded five credit portfolio CSV snapshots and captured reporting dates from filenames.",
        "- Loaded every sheet from the sales/customer workbook: Sales Details, Gender, DOB, and Income Level.",
        "- Loaded the NPS workbook survey sheet.",
        "- Standardized column names to snake_case for profiling and relationship checks.",
        "- Calculated row counts, column data types, null counts, null percentages, and unique counts.",
        "- Checked duplicate full rows and duplicate identifier values.",
        "- Parsed date-like columns with UTC normalization to detect invalid dates and mixed timezone issues.",
        "- Profiled date source formats and sample values before cleaning.",
        "- Profiled numeric and currency-like columns for formatting, non-numeric values, negative values, and ranges.",
        "- Analyzed `loan_id` join coverage, cardinality, and foreign-key integrity across source datasets.",
        "- Generated cleaning decisions and justifications for discovered inconsistencies.",
        "",
        "## Source Dataset Summary",
        "",
        markdown_table(source_dataset_summary(datasets)),
        "",
        "## Likely Join Keys and Relationship Coverage",
        "",
        markdown_table(likely_join_key_profile(datasets)),
        "",
        "## Relationship Analysis: Cardinality and Foreign-Key Integrity",
        "",
        markdown_table(relationship_analysis(datasets)),
        "",
        "## Inconsistency Summary and Cleaning Decision Log",
        "",
        markdown_table(issue_summary(datasets)),
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
            "- Missing values are not imputed during profiling; nulls are measured and documented so cleaning rules remain auditable.",
            "- Date parsing uses `errors='coerce'` and `utc=True` only for quality assessment; invalid parses should be retained as null plus a validation flag during cleaning.",
            "- Currency and numeric cleaning should strip display formatting but preserve original raw columns or source files for auditability.",
            "- Negative monetary values are flagged, not automatically removed, because they may represent adjustments, refunds, reversals, or source defects.",
            "- `customer_age` is treated as suspicious where values fall outside 18-120; final age bands should be derived from DOB as of reporting date where possible.",
            "",
            "## Cleaning Decision Principles",
            "",
            "| Decision area | Rule | Justification |",
            "|:--|:--|:--|",
            "| Column names | Standardize to snake_case. | Consistent names make joins, validation, and downstream SQL/Python code reproducible. |",
            "| Raw data | Keep raw files immutable. | Auditability requires the ability to reproduce every cleaned value from source. |",
            "| Duplicate IDs | Resolve with deterministic business rules per table. | Some duplicates are legitimate repeated events or survey responses; blind deduplication can lose information. |",
            "| Missing values | Flag and document before imputation or exclusion. | Missingness may carry business meaning, especially sparse returns, payments, adjustments, and survey fields. |",
            "| Dates | Parse explicitly and normalize timezone handling. | Portfolio snapshots, aging, and days-past-due metrics depend on reliable dates. |",
            "| Currency/numeric values | Strip formatting, convert to numeric, and flag invalid or negative values. | Analysts need numeric fields, but anomalies should remain visible for validation. |",
            "| Relationships | Treat `loan_id` as the primary analytical join key. | It appears across credit, sales/customer, and NPS sources and gives the strongest cross-dataset coverage. |",
            "",
        ]
    )

    report_path = DOCS_DIR / "data_quality_report.md"
    report_path.write_text("\n".join(report_sections), encoding="utf-8")
    print(f"Wrote {report_path}")


if __name__ == "__main__":
    main()
