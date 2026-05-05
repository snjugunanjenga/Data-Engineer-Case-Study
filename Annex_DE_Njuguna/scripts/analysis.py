"""Portfolio health, NPS, and data-gap analysis for ABC Phones.

This script uses the feature-engineered portfolio output and the raw NPS
workbook to answer Part 3 of the case study. It writes analysis CSVs, chart
PNGs, a markdown report, and a final slide deck.
"""

from __future__ import annotations

import os
import re
import textwrap
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "outputs"
DOCS_DIR = BASE_DIR / "docs"
CHART_DIR = OUTPUT_DIR / "charts"
SLIDES_DIR = BASE_DIR / "slides"

NPS_SCORE_COLUMN = (
    "Using a scale from 0 (not likely) to 10 (very likely), how likely are you "
    "to recommend ABC Phones to friends or family?"
)
NPS_RENAME = {
    "Submission ID": "submission_id",
    "Respondent ID": "respondent_id",
    "Submitted at": "submitted_at",
    "Loan Id": "loan_id",
    NPS_SCORE_COLUMN: "nps_score",
    "Have you ever experienced a delay in your payment reflecting in your ABC account?": "payment_delay_reported",
    "Have you ever had difficulty getting assistance from ABC Phones customer support when needed?": "support_difficulty_reported",
    "Have you ever had your phone lock despite making a payment on time?": "phone_lock_after_payment",
}
RISK_ORDER = ["Low", "Medium", "High", "Critical"]
RISK_SCORE = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}


def clean_column_name(column: object) -> str:
    normalized = re.sub(r"[^0-9a-zA-Z]+", "_", str(column).strip().lower())
    return re.sub(r"_+", "_", normalized).strip("_")


def normalize_loan_id(series: pd.Series) -> pd.Series:
    return series.astype("string").str.strip()


def yes_no_to_bool(series: pd.Series) -> pd.Series:
    values = series.astype("string").str.strip().str.lower()
    return values.map({"yes": True, "no": False})


def load_portfolio() -> pd.DataFrame:
    path = OUTPUT_DIR / "feature_engineered_summary.csv"
    if not path.exists():
        raise FileNotFoundError("Run scripts/feature_engineering.py before analysis.")

    frame = pd.read_csv(path)
    frame["loan_id"] = normalize_loan_id(frame["loan_id"])
    frame["reporting_date"] = pd.to_datetime(frame["reporting_date"], errors="coerce")
    numeric_columns = [
        "days_past_due",
        "arrears",
        "payment",
        "expected_payment",
        "total_paid",
        "total_due_today",
        "balance",
        "closing_balance",
    ]
    for column in numeric_columns:
        if column in frame.columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")

    frame["is_delinquent"] = frame["days_past_due"].fillna(0).gt(0)
    status_text = (
        frame["account_status_l1"].fillna("").astype(str).str.lower()
        + " "
        + frame["account_status_l2"].fillna("").astype(str).str.lower()
    )
    frame["is_write_off"] = status_text.str.contains("write off", regex=False)
    frame["is_critical"] = frame["risk_category"].eq("Critical")
    frame["risk_score"] = frame["risk_category"].map(RISK_SCORE)
    valid_expected = frame["expected_payment"].gt(0)
    frame["collection_rate"] = np.where(
        valid_expected,
        (frame["payment"] / frame["expected_payment"]).clip(lower=0, upper=2),
        np.nan,
    )
    return frame


def load_nps() -> pd.DataFrame:
    nps_path = RAW_DIR / "nps" / "NPS Data (1).xlsx"
    nps = pd.read_excel(nps_path).rename(columns=NPS_RENAME)
    nps["loan_id"] = normalize_loan_id(nps["loan_id"])
    nps["submitted_at"] = pd.to_datetime(nps["submitted_at"], errors="coerce")
    nps["nps_score"] = pd.to_numeric(nps["nps_score"], errors="coerce")
    nps = nps[nps["loan_id"].notna() & nps["nps_score"].between(0, 10)].copy()
    nps["nps_group"] = pd.cut(
        nps["nps_score"],
        bins=[-np.inf, 6, 8, np.inf],
        labels=["Detractor", "Passive", "Promoter"],
    )
    for column in ["payment_delay_reported", "support_difficulty_reported", "phone_lock_after_payment"]:
        if column in nps.columns:
            nps[column] = yes_no_to_bool(nps[column])
    return nps


def calculate_portfolio_metrics(portfolio: pd.DataFrame) -> pd.DataFrame:
    metrics = (
        portfolio.groupby("reporting_date", as_index=False)
        .agg(
            account_count=("loan_id", "nunique"),
            total_records=("loan_id", "size"),
            delinquency_rate=("is_delinquent", "mean"),
            write_off_rate=("is_write_off", "mean"),
            average_collection_rate=("collection_rate", "mean"),
            critical_risk_rate=("is_critical", "mean"),
            average_days_past_due=("days_past_due", "mean"),
            total_arrears=("arrears", "sum"),
            total_balance=("balance", "sum"),
        )
        .sort_values("reporting_date")
    )
    rate_columns = [
        "delinquency_rate",
        "write_off_rate",
        "average_collection_rate",
        "critical_risk_rate",
        "average_days_past_due",
    ]
    metrics[rate_columns] = metrics[rate_columns].round(4)
    metrics["reporting_date"] = metrics["reporting_date"].dt.date.astype(str)
    return metrics


def calculate_segment_metrics(portfolio: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    portfolio_avg = portfolio["is_critical"].mean()
    segment_frames = []
    for segment_column in ["age_band", "avg_monthly_income_band"]:
        segment = (
            portfolio.assign(segment_value=portfolio[segment_column].fillna("Missing"))
            .groupby(["reporting_date", "segment_value"], as_index=False)
            .agg(
                segment_records=("loan_id", "size"),
                delinquency_rate=("is_delinquent", "mean"),
                critical_risk_rate=("is_critical", "mean"),
                write_off_rate=("is_write_off", "mean"),
            )
        )
        segment["segment_type"] = segment_column
        segment_frames.append(segment)

    segments = pd.concat(segment_frames, ignore_index=True)
    summary = (
        segments.groupby(["segment_type", "segment_value"], as_index=False)
        .agg(
            segment_records=("segment_records", "sum"),
            avg_delinquency_rate=("delinquency_rate", "mean"),
            avg_critical_risk_rate=("critical_risk_rate", "mean"),
            avg_write_off_rate=("write_off_rate", "mean"),
        )
        .query("segment_value != 'Missing' and segment_records >= 100")
    )
    summary["critical_risk_lift_vs_portfolio"] = (
        summary["avg_critical_risk_rate"] - portfolio_avg
    )
    summary["absolute_critical_risk_lift"] = summary["critical_risk_lift_vs_portfolio"].abs()
    best_segment = summary.sort_values(
        ["absolute_critical_risk_lift", "segment_records"], ascending=[False, False]
    ).iloc[0]

    segments["reporting_date"] = pd.to_datetime(segments["reporting_date"]).dt.date.astype(str)
    for column in ["delinquency_rate", "critical_risk_rate", "write_off_rate"]:
        segments[column] = segments[column].round(4)
    return segments, best_segment


def join_credit_to_nps(portfolio: pd.DataFrame, nps: pd.DataFrame) -> pd.DataFrame:
    credit_columns = [
        "loan_id",
        "reporting_date",
        "risk_category",
        "risk_score",
        "days_past_due",
        "is_delinquent",
        "is_write_off",
        "collection_rate",
        "age_band",
        "avg_monthly_income_band",
    ]
    credit = portfolio[credit_columns].sort_values(["loan_id", "reporting_date"])
    latest_credit = credit.drop_duplicates("loan_id", keep="last")

    joined_parts = []
    for loan_id, nps_group in nps.sort_values("submitted_at").groupby("loan_id", dropna=False):
        credit_group = credit[credit["loan_id"].eq(loan_id)]
        if credit_group.empty:
            joined_parts.append(nps_group.assign(_merge="left_only"))
            continue

        asof_joined = pd.merge_asof(
            nps_group.sort_values("submitted_at"),
            credit_group.sort_values("reporting_date"),
            left_on="submitted_at",
            right_on="reporting_date",
            direction="backward",
        )
        missing_credit = asof_joined["reporting_date"].isna()
        if missing_credit.any():
            fallback = latest_credit[latest_credit["loan_id"].eq(loan_id)].iloc[0]
            for column in credit_columns:
                if column == "loan_id":
                    continue
                asof_joined.loc[missing_credit, column] = fallback[column]
        asof_joined["loan_id"] = loan_id
        asof_joined["_merge"] = "both"
        joined_parts.append(asof_joined)

    return pd.concat(joined_parts, ignore_index=True)


def calculate_nps_metrics(credit_nps: pd.DataFrame) -> dict[str, pd.DataFrame]:
    by_risk = (
        credit_nps.dropna(subset=["risk_category"])
        .groupby("risk_category", as_index=False)
        .agg(
            responses=("submission_id", "nunique"),
            avg_nps=("nps_score", "mean"),
            detractor_rate=("nps_group", lambda s: s.eq("Detractor").mean()),
            avg_days_past_due=("days_past_due", "mean"),
        )
    )
    by_risk["risk_category"] = pd.Categorical(by_risk["risk_category"], RISK_ORDER, ordered=True)
    by_risk = by_risk.sort_values("risk_category")

    by_delinquency = (
        credit_nps.dropna(subset=["is_delinquent"])
        .groupby("is_delinquent", as_index=False)
        .agg(
            responses=("submission_id", "nunique"),
            avg_nps=("nps_score", "mean"),
            detractor_rate=("nps_group", lambda s: s.eq("Detractor").mean()),
            payment_delay_rate=("payment_delay_reported", "mean"),
            phone_lock_rate=("phone_lock_after_payment", "mean"),
            support_difficulty_rate=("support_difficulty_reported", "mean"),
        )
    )

    experience = (
        credit_nps.groupby("nps_group", as_index=False, observed=False)
        .agg(
            responses=("submission_id", "nunique"),
            delinquency_rate=("is_delinquent", "mean"),
            avg_days_past_due=("days_past_due", "mean"),
            payment_delay_rate=("payment_delay_reported", "mean"),
            phone_lock_rate=("phone_lock_after_payment", "mean"),
            support_difficulty_rate=("support_difficulty_reported", "mean"),
        )
    )

    for frame in [by_risk, by_delinquency, experience]:
        numeric = frame.select_dtypes(include="number").columns
        frame[numeric] = frame[numeric].round(4)

    return {
        "nps_by_risk": by_risk,
        "nps_by_delinquency": by_delinquency,
        "nps_experience": experience,
    }


def save_chart(fig: plt.Figure, filename: str) -> Path:
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    path = CHART_DIR / filename
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return path


def create_charts(
    portfolio_metrics: pd.DataFrame,
    segment_metrics: pd.DataFrame,
    nps_tables: dict[str, pd.DataFrame],
) -> dict[str, Path]:
    sns.set_theme(style="whitegrid")
    charts = {}
    metrics = portfolio_metrics.copy()
    metrics["reporting_date"] = pd.to_datetime(metrics["reporting_date"])

    fig, ax = plt.subplots(figsize=(10, 5))
    for column, label in [
        ("delinquency_rate", "Delinquency"),
        ("write_off_rate", "Write-off"),
        ("critical_risk_rate", "Critical risk"),
    ]:
        ax.plot(metrics["reporting_date"], metrics[column] * 100, marker="o", label=label)
    ax.set_title("Portfolio Risk Trends by Reporting Snapshot")
    ax.set_ylabel("Rate (%)")
    ax.set_xlabel("Reporting date")
    ax.legend()
    charts["portfolio_trends"] = save_chart(fig, "portfolio_trends.png")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(metrics["reporting_date"], metrics["average_collection_rate"] * 100, marker="o", color="#0f766e")
    ax.set_title("Average Payment Collection Rate")
    ax.set_ylabel("Payment / expected payment (%)")
    ax.set_xlabel("Reporting date")
    charts["collection_trend"] = save_chart(fig, "collection_trend.png")

    latest_segment = segment_metrics[
        (segment_metrics["segment_type"] == "avg_monthly_income_band")
        & (segment_metrics["segment_value"] != "Missing")
    ].copy()
    latest_segment = latest_segment.sort_values("critical_risk_rate", ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=latest_segment, x="critical_risk_rate", y="segment_value", ax=ax, color="#dc2626")
    ax.set_title("Critical Risk Rate by Income Band")
    ax.set_xlabel("Critical risk rate")
    ax.set_ylabel("Income band")
    charts["segment_risk"] = save_chart(fig, "segment_risk.png")

    by_risk = nps_tables["nps_by_risk"].copy()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=by_risk, x="risk_category", y="avg_nps", ax=ax, color="#2563eb")
    ax.set_title("Average NPS by Credit Risk Category")
    ax.set_xlabel("Risk category")
    ax.set_ylabel("Average NPS")
    ax.set_ylim(0, 10)
    charts["nps_by_risk"] = save_chart(fig, "nps_by_risk.png")

    experience = nps_tables["nps_experience"].copy()
    fig, ax = plt.subplots(figsize=(9, 5))
    plot_data = experience.melt(
        id_vars="nps_group",
        value_vars=["payment_delay_rate", "phone_lock_rate", "support_difficulty_rate"],
        var_name="experience_issue",
        value_name="rate",
    )
    sns.barplot(data=plot_data, x="nps_group", y="rate", hue="experience_issue", ax=ax)
    ax.set_title("Customer Experience Issues by NPS Group")
    ax.set_xlabel("NPS group")
    ax.set_ylabel("Reported issue rate")
    ax.legend(title="")
    charts["experience_by_nps"] = save_chart(fig, "experience_by_nps.png")
    return charts


def percent(value: float) -> str:
    if pd.isna(value):
        return "n/a"
    return f"{value * 100:.1f}%"


def describe_lift(value: float) -> str:
    direction = "above" if value >= 0 else "below"
    return f"{abs(value) * 100:.1f}% {direction}"


def write_report(
    portfolio_metrics: pd.DataFrame,
    segment_metrics: pd.DataFrame,
    best_segment: pd.Series,
    credit_nps: pd.DataFrame,
    nps_tables: dict[str, pd.DataFrame],
) -> Path:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    latest = portfolio_metrics.iloc[-1]
    first = portfolio_metrics.iloc[0]
    by_risk = nps_tables["nps_by_risk"]
    nps_low = by_risk.loc[by_risk["risk_category"].astype(str).eq("Low"), "avg_nps"]
    nps_critical = by_risk.loc[by_risk["risk_category"].astype(str).eq("Critical"), "avg_nps"]
    low_text = f"{float(nps_low.iloc[0]):.2f}" if not nps_low.empty else "n/a"
    critical_text = f"{float(nps_critical.iloc[0]):.2f}" if not nps_critical.empty else "n/a"
    matched = int(credit_nps["_merge"].eq("both").sum())
    total = int(len(credit_nps))

    report = f"""# Portfolio, NPS, and Data Gaps Analysis

## Question 3A: Portfolio Health

Selected metrics:

{portfolio_metrics.to_markdown(index=False)}

Key trend findings:

- Account count increased from {int(first['account_count']):,} to {int(latest['account_count']):,} across the available reporting snapshots.
- Delinquency rate moved from {percent(first['delinquency_rate'])} to {percent(latest['delinquency_rate'])}.
- Write-off rate moved from {percent(first['write_off_rate'])} to {percent(latest['write_off_rate'])}.
- Critical-risk share moved from {percent(first['critical_risk_rate'])} to {percent(latest['critical_risk_rate'])}.
- Average collection rate moved from {percent(first['average_collection_rate'])} to {percent(latest['average_collection_rate'])}.

Meaningful risk segment:

- `{best_segment['segment_type']}` = `{best_segment['segment_value']}` has an average critical-risk rate of {percent(best_segment['avg_critical_risk_rate'])}, {describe_lift(best_segment['critical_risk_lift_vs_portfolio'])} the portfolio average.

## Question 3B: Credit Outcomes x Customer Experience

NPS match coverage: {matched:,} of {total:,} valid NPS responses matched to a credit account ({matched / total:.1%}).

Average NPS by risk category:

{by_risk.to_markdown(index=False)}

Delinquency and customer experience:

{nps_tables['nps_by_delinquency'].to_markdown(index=False)}

Experience issues by NPS group:

{nps_tables['nps_experience'].to_markdown(index=False)}

Interpretation:

- Lower-quality credit outcomes are proxied by higher risk category, delinquency, write-off status, and higher days past due because no explicit credit score is present.
- Low-risk customers average NPS of {low_text}; critical-risk customers average NPS of {critical_text}.
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
"""
    path = DOCS_DIR / "portfolio_nps_analysis_report.md"
    path.write_text(report, encoding="utf-8")
    return path


def add_wrapped_text(ax, text: str, x: float, y: float, width: int = 95, size: int = 11) -> None:
    wrapped = "\n".join(textwrap.fill(line, width=width) for line in text.split("\n"))
    ax.text(x, y, wrapped, fontsize=size, color="#334155", va="top", transform=ax.transAxes)


def slide_title(ax, title: str, subtitle: str | None = None) -> None:
    ax.text(0.05, 0.92, title, fontsize=22, weight="bold", color="#0f172a", transform=ax.transAxes)
    if subtitle:
        ax.text(0.05, 0.86, subtitle, fontsize=11, color="#475569", transform=ax.transAxes)


def create_final_deck(
    portfolio_metrics: pd.DataFrame,
    best_segment: pd.Series,
    nps_tables: dict[str, pd.DataFrame],
    charts: dict[str, Path],
) -> Path:
    SLIDES_DIR.mkdir(parents=True, exist_ok=True)
    output = SLIDES_DIR / "Annex_DE_Presentation.pdf"
    latest = portfolio_metrics.iloc[-1]
    first = portfolio_metrics.iloc[0]

    with PdfPages(output) as pdf:
        fig, ax = plt.subplots(figsize=(13.33, 7.5))
        ax.axis("off")
        slide_title(ax, "ABC Phones Credit Portfolio Analysis", "Data engineering, portfolio health, NPS, and source-data improvement recommendations")
        add_wrapped_text(
            ax,
            "This deck summarizes a reproducible ETL and analytics workflow built from credit snapshots, sales/customer data, and NPS survey responses.",
            0.07,
            0.68,
            size=14,
        )
        add_wrapped_text(ax, "Prepared for Annex Technologies Limited Data Engineer Case Study", 0.07, 0.25, size=12)
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(13.33, 7.5))
        ax.axis("off")
        slide_title(ax, "Data Foundation and ETL", "Batch pipeline from raw files to analytics-ready gold tables")
        img = plt.imread(BASE_DIR / "pipeline_design" / "architecture.png")
        ax.imshow(img, extent=[0.05, 0.95, 0.08, 0.78], aspect="auto")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(13.33, 7.5))
        ax.axis("off")
        slide_title(ax, "Data Quality and Feature Engineering")
        add_wrapped_text(
            ax,
            "\n".join(
                [
                    "- `loan_id` is the primary join key across credit, customer, and NPS sources.",
                    "- DOB and income records are sparse, so missing values are flagged rather than imputed.",
                    "- Required features created: age_band, avg_monthly_income_band, days_past_due, and risk_category.",
                    "- Risk category combines account status, arrears, DPD, and missed expected payment indicators.",
                ]
            ),
            0.08,
            0.78,
            size=13,
        )
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(13.33, 7.5))
        ax.axis("off")
        slide_title(ax, "Portfolio Health Trends")
        img = plt.imread(charts["portfolio_trends"])
        ax.imshow(img, extent=[0.07, 0.92, 0.25, 0.78], aspect="auto")
        add_wrapped_text(
            ax,
            f"Accounts grew from {int(first['account_count']):,} to {int(latest['account_count']):,}. Latest delinquency is {percent(latest['delinquency_rate'])}, write-off rate is {percent(latest['write_off_rate'])}, and critical-risk share is {percent(latest['critical_risk_rate'])}.",
            0.08,
            0.18,
            width=110,
            size=11,
        )
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(13.33, 7.5))
        ax.axis("off")
        slide_title(ax, "Segment Risk Behavior")
        img = plt.imread(charts["segment_risk"])
        ax.imshow(img, extent=[0.08, 0.88, 0.25, 0.78], aspect="auto")
        add_wrapped_text(
            ax,
            f"The strongest segment signal is {best_segment['segment_type']} = {best_segment['segment_value']}, with critical-risk rate {percent(best_segment['avg_critical_risk_rate'])}, {describe_lift(best_segment['critical_risk_lift_vs_portfolio'])} the portfolio average.",
            0.08,
            0.18,
            width=110,
            size=11,
        )
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(13.33, 7.5))
        ax.axis("off")
        slide_title(ax, "Credit Outcomes x NPS")
        img = plt.imread(charts["nps_by_risk"])
        ax.imshow(img, extent=[0.10, 0.82, 0.25, 0.78], aspect="auto")
        add_wrapped_text(
            ax,
            "Risk category, delinquency, write-off status, and days past due are used as credit-outcome proxies because no explicit credit score is present.",
            0.08,
            0.18,
            width=110,
            size=11,
        )
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(13.33, 7.5))
        ax.axis("off")
        slide_title(ax, "Collections and Customer Experience Tension")
        img = plt.imread(charts["experience_by_nps"])
        ax.imshow(img, extent=[0.08, 0.90, 0.27, 0.80], aspect="auto")
        add_wrapped_text(
            ax,
            "Payment delays, payment-related phone locks, and support difficulty are operational levers where ABC Phones can improve repayment experience and customer satisfaction together.",
            0.08,
            0.18,
            width=110,
            size=11,
        )
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(13.33, 7.5))
        ax.axis("off")
        slide_title(ax, "Data Gaps and Improvements")
        add_wrapped_text(
            ax,
            "\n".join(
                [
                    "Missing: transaction-level payment detail, employment type, location, collection contact history, lock/unlock events, and explicit credit score.",
                    "Inconsistent: repeated customer workbook records, sparse DOB/income coverage, negative monetary values, and mixed status semantics.",
                    "Ambiguous: account status hierarchy, meaning of customer_age, and original payment due date.",
                    "Improvements: capture transaction events, govern customer/account dimensions, and publish a controlled account-status mapping table.",
                ]
            ),
            0.08,
            0.78,
            width=105,
            size=13,
        )
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(13.33, 7.5))
        ax.axis("off")
        slide_title(ax, "Recommendation")
        add_wrapped_text(
            ax,
            "Create a payment reflection and unlock assurance workflow for delinquent or recently paid customers. Reconcile payments daily, proactively confirm reflected payments, suppress avoidable locks, and route unresolved cases to a collections-support queue.",
            0.08,
            0.75,
            width=95,
            size=16,
        )
        add_wrapped_text(
            ax,
            "Why this matters: it targets both repayment outcomes and the NPS pain points tied to delayed payment reflection, phone locking, and support difficulty.",
            0.08,
            0.45,
            width=100,
            size=13,
        )
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

    return output


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    portfolio = load_portfolio()
    nps = load_nps()
    portfolio_metrics = calculate_portfolio_metrics(portfolio)
    segment_metrics, best_segment = calculate_segment_metrics(portfolio)
    credit_nps = join_credit_to_nps(portfolio, nps)
    nps_tables = calculate_nps_metrics(credit_nps)
    charts = create_charts(portfolio_metrics, segment_metrics, nps_tables)

    portfolio_metrics.to_csv(OUTPUT_DIR / "portfolio_metrics.csv", index=False)
    segment_metrics.to_csv(OUTPUT_DIR / "segment_risk_metrics.csv", index=False)
    credit_nps.to_csv(OUTPUT_DIR / "credit_nps_analysis.csv", index=False)
    for name, frame in nps_tables.items():
        frame.to_csv(OUTPUT_DIR / f"{name}.csv", index=False)

    report_path = write_report(portfolio_metrics, segment_metrics, best_segment, credit_nps, nps_tables)
    deck_path = create_final_deck(portfolio_metrics, best_segment, nps_tables, charts)

    print(f"Wrote {OUTPUT_DIR / 'portfolio_metrics.csv'}")
    print(f"Wrote {OUTPUT_DIR / 'segment_risk_metrics.csv'}")
    print(f"Wrote {OUTPUT_DIR / 'credit_nps_analysis.csv'}")
    print(f"Wrote {report_path}")
    print(f"Wrote {deck_path}")


if __name__ == "__main__":
    main()
