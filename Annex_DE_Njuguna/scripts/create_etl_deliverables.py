"""Generate ETL architecture diagram and design slides."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


BASE_DIR = Path(__file__).resolve().parents[1]
PIPELINE_DIR = BASE_DIR / "pipeline_design"
SLIDES_DIR = BASE_DIR / "slides"


def add_box(ax, xy, width, height, title, body, color):
    box = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.02",
        linewidth=1.3,
        edgecolor="#1f2937",
        facecolor=color,
    )
    ax.add_patch(box)
    ax.text(xy[0] + width / 2, xy[1] + height - 0.08, title, ha="center", va="top", fontsize=11, weight="bold")
    ax.text(xy[0] + 0.04, xy[1] + height - 0.22, body, ha="left", va="top", fontsize=8.5, linespacing=1.25)


def add_arrow(ax, start, end, color="#334155"):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=14,
            linewidth=1.4,
            color=color,
        )
    )


def create_architecture_png() -> None:
    PIPELINE_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(16, 8.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor("#f8fafc")

    ax.text(0.5, 0.96, "ABC Phones Batch ETL Architecture", ha="center", va="top", fontsize=20, weight="bold", color="#0f172a")
    ax.text(0.5, 0.92, "Source files -> raw ingestion -> cleaning and enrichment -> quality gate -> analytics-ready gold tables", ha="center", va="top", fontsize=11, color="#475569")

    boxes = [
        ((0.03, 0.64), 0.15, 0.2, "Sources", "Credit CSV snapshots\nSales/customer workbook\nNPS workbook", "#dbeafe"),
        ((0.23, 0.64), 0.15, 0.2, "Ingestion", "Python + pandas\nFile manifest\nSchema checks\nChecksums", "#dcfce7"),
        ((0.43, 0.64), 0.15, 0.2, "Bronze", "Raw append-only tables\nSource row lineage\nIngestion versions", "#fef9c3"),
        ((0.63, 0.64), 0.15, 0.2, "Silver", "Clean types\nNormalize IDs\nDeduplicate\nValidation flags", "#ffedd5"),
        ((0.83, 0.64), 0.15, 0.2, "Gold", "Account snapshots\nPortfolio metrics\nCredit x NPS views", "#ede9fe"),
    ]
    for xy, width, height, title, body, color in boxes:
        add_box(ax, xy, width, height, title, body, color)

    for x0, x1 in [(0.18, 0.23), (0.38, 0.43), (0.58, 0.63), (0.78, 0.83)]:
        add_arrow(ax, (x0, 0.74), (x1, 0.74))

    add_box(ax, (0.23, 0.33), 0.23, 0.18, "Transformation Orchestration", "Daily scheduled batch\nFull refresh dimensions\nIncremental credit snapshots\nLate-arrival replay", "#e0f2fe")
    add_box(ax, (0.52, 0.33), 0.23, 0.18, "Feature Engineering", "age_band\navg_monthly_income_band\ndays_past_due\nrisk_category", "#fce7f3")
    add_box(ax, (0.30, 0.08), 0.18, 0.15, "Error Handling", "Quarantine bad files\nBlock gold publish\nReplay corrected files", "#fee2e2")
    add_box(ax, (0.52, 0.08), 0.18, 0.15, "Logging + Alerts", "DQ results table\nSlack/email alerts\nRun manifest", "#f1f5f9")
    add_box(ax, (0.74, 0.08), 0.18, 0.15, "Analyst Access", "SQL / BI dashboards\nPartition by date\nSegment by risk bands", "#ecfccb")

    add_arrow(ax, (0.705, 0.64), (0.63, 0.51))
    add_arrow(ax, (0.635, 0.33), (0.71, 0.64))
    add_arrow(ax, (0.705, 0.64), (0.61, 0.23), "#dc2626")
    add_arrow(ax, (0.60, 0.23), (0.52, 0.16), "#dc2626")
    add_arrow(ax, (0.98, 0.70), (0.84, 0.23))

    ax.text(0.03, 0.02, "Tools: Python, pandas, SQL/dbt-compatible marts, object storage or warehouse partitions, scheduler such as cron/Airflow/Prefect.", fontsize=9, color="#475569")
    fig.savefig(PIPELINE_DIR / "architecture.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def slide(title, bullets):
    fig, ax = plt.subplots(figsize=(13.33, 7.5))
    fig.patch.set_facecolor("#ffffff")
    ax.axis("off")
    ax.text(0.06, 0.90, title, fontsize=24, weight="bold", color="#0f172a", transform=ax.transAxes)
    y = 0.76
    for heading, body in bullets:
        ax.text(0.08, y, heading, fontsize=15, weight="bold", color="#1f2937", transform=ax.transAxes)
        ax.text(0.10, y - 0.07, body, fontsize=12, color="#334155", linespacing=1.35, transform=ax.transAxes)
        y -= 0.22
    return fig


def create_slides_pdf() -> None:
    SLIDES_DIR.mkdir(parents=True, exist_ok=True)
    slides = [
        slide(
            "ETL Architecture and Tooling",
            [
                ("Pattern", "Bronze/silver/gold batch pipeline from source files to analytics-ready tables."),
                ("Tools", "Python + pandas for ingestion/profiling, SQL/dbt-style marts for warehouse outputs, scheduler for daily orchestration."),
                ("Controls", "File manifest, source lineage, schema validation, data quality gates, and partitioned gold publication."),
            ],
        ),
        slide(
            "Ingestion and Transformation Decisions",
            [
                ("Credit snapshots", "Append incrementally by reporting_date parsed from filenames; replay late files by replacing affected partitions."),
                ("Customer and NPS workbooks", "Full refresh dimensions where source is workbook-based; preserve NPS repeated responses and dedupe by submission_id."),
                ("Feature automation", "Normalize loan_id, join DOB/income/NPS, then derive age_band, income band, days_past_due, and risk_category."),
            ],
        ),
        slide(
            "Storage, Quality, and Recovery",
            [
                ("Gold outputs", "gold_credit_account_snapshot, gold_portfolio_metrics_daily, gold_risk_segment_metrics, gold_credit_nps_customer_view."),
                ("Partitioning", "Partition by reporting_date; cluster/index by loan_id, risk_category, age_band, and avg_monthly_income_band."),
                ("Failure handling", "Quarantine malformed files, block gold publication on critical DQ failures, alert stakeholders, and replay corrected files."),
            ],
        ),
    ]
    with PdfPages(SLIDES_DIR / "etl_pipeline_design_slides.pdf") as pdf:
        for fig in slides:
            pdf.savefig(fig, bbox_inches="tight")
            plt.close(fig)


def main() -> None:
    create_architecture_png()
    create_slides_pdf()
    print(f"Wrote {PIPELINE_DIR / 'architecture.png'}")
    print(f"Wrote {SLIDES_DIR / 'etl_pipeline_design_slides.pdf'}")


if __name__ == "__main__":
    main()
