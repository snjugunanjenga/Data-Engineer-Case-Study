# Annex Data Engineer Case Study

## Project

ABC Phones credit portfolio analysis for the Annex Technologies Limited Data Engineer Case Study.

This submission is organized to support repeatable profiling, cleaning, feature engineering, data quality checks, portfolio analysis, and presentation packaging.

## Source Data

Raw source files are kept outside this submission folder under:

```text
../data/raw/
├── credit/Credit Data/
├── sales_customer/
└── nps/
```

Expected source files:

- `../data/raw/credit/Credit Data/Credit Data - 01-01-2025.csv`
- `../data/raw/credit/Credit Data/Credit Data - 30-03-2025.csv`
- `../data/raw/credit/Credit Data/Credit Data - 30-06-2025.csv`
- `../data/raw/credit/Credit Data/Credit Data - 30-09-2025.csv`
- `../data/raw/credit/Credit Data/Credit Data - 30-12-2025.csv`
- `../data/raw/credit/Credit Data/Credit Data Definitions.xlsx`
- `../data/raw/sales_customer/Sales and Customer Data.xlsx`
- `../data/raw/nps/NPS Data (1).xlsx`

## Environment

Recommended Python version: 3.10 or newer.

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Install dependencies from the locked project list:

```bash
python -m pip install -r requirements.txt
```

## How to Run

Run scripts from this folder:

```bash
cd Annex_DE_Njuguna
python scripts/data_profiling.py
python scripts/data_cleaning.py
python scripts/feature_engineering.py
python scripts/quality_checks.py
python scripts/analysis.py
```

## Outputs

- `outputs/data_quality_report.md`: Profiling findings, assumptions, and quality issues.
- `outputs/cleaned_summary.csv`: Sample cleaned and feature-enriched output.
- `outputs/portfolio_metrics.csv`: Portfolio health metrics for analysis and slides.
- `pipeline_design/architecture.png`: Batch ETL architecture diagram.
- `slides/Annex_DE_Presentation.pdf`: Final presentation placeholder.

## Assumptions

- Customer identifiers are the primary join keys across credit, sales/customer, and NPS data.
- Credit CSV filenames contain reporting dates and can be used to derive snapshot dates.
- NPS enrichment is optional because not all customers may have survey responses.
- Income columns should be standardized to numeric values before aggregation.
- Date parsing decisions and missing-value handling must be documented in `outputs/data_quality_report.md`.

## Submission Notes

The scripts are intentionally organized by workflow stage:

1. Profile source data.
2. Clean and standardize records.
3. Engineer required case-study features.
4. Run data quality checks.
5. Produce portfolio and NPS analysis outputs.

## Dependencies

- pandas: data loading, profiling, cleaning, joins, and aggregation.
- numpy: vectorized feature engineering and numeric operations.
- matplotlib: low-level charting for portfolio trend outputs.
- seaborn: statistical charts with accessible defaults.
- jupyter: exploratory notebook development and reproducible analysis narratives.
- scikit-learn: optional modeling or segmentation extensions.
- openpyxl: Excel workbook ingestion.
- tabulate: markdown table rendering in profiling reports.
