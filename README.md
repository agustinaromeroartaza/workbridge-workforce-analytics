# WorkBridge Workforce Analytics

End-to-end data analytics project focused on automating monthly workforce executive reports for a fictitious professional services company.

## Business Problem

WorkBridge Solutions prepares monthly executive reports for its corporate clients using manual Excel-based processes. These reports include workforce turnover, regional costs, capacity utilization, billable utilization and goal achievement.

The current process takes approximately three days per client and presents risks related to manual errors, inconsistent data, duplicated work and limited traceability.

## Project Objective

The objective of this project is to design and implement an automated data pipeline that integrates multiple internal data sources, applies data cleaning and transformation processes, builds an analytical data model, and prepares curated datasets for Power BI reporting.

The final solution follows a Medallion Architecture approach:

```text
Raw data sources
→ Bronze layer
→ Silver layer
→ Gold analytical model
→ Power BI dashboard
→ PDF executive report
```

## Fictitious Company

WorkBridge Solutions is a fictitious professional services company that manages distributed workforce teams assigned to different corporate clients across multiple regions.

## Data Sources

The project uses synthetic datasets that simulate common workforce, client, hours, cost and target data.

| Source file | Description |
|---|---|
| `headcount.csv` | Employee and HR data. |
| `assignments.xlsx` | Employee assignments to clients and projects. |
| `hours.csv` | Monthly worked, available, billable, non-billable and overtime hours. |
| `costs.json` | Monthly workforce costs by employee and region. |
| `goals.csv` | Monthly business targets by client and region. |
| `clients.xlsx` | Client master data. |

## Tools and Technologies

- Python
- Pandas
- PySpark
- Databricks
- Delta Lake
- Databricks Jobs
- Git / GitHub
- CSV, Excel and JSON files
- Power BI

## Repository Structure

```text
workbridge-workforce-analytics/
├── data/
│   └── raw/
├── databricks/
│   └── workbridge_job_config.yml
├── docs/
│   ├── data_model.md
│   ├── databricks_job_orchestration.md
│   └── images/
│       ├── databricks_job_run_success.png
│       └── gold_data_model.png
├── notebooks/
│   ├── 01_ingest_bronze.ipynb
│   ├── 02_validate_bronze.ipynb
│   ├── 03_transform_silver.ipynb
│   ├── 04_validate_silver.ipynb
│   ├── 05_build_gold.ipynb
│   └── 06_validate_gold.ipynb
├── scripts/
└── README.md
```

## Pipeline Overview

### 01 — Ingest Bronze

The Bronze ingestion notebook reads raw files directly from GitHub and saves them as managed Delta tables in Databricks.

Main actions:

- Reads CSV, Excel and JSON files.
- Uses Pandas for simple file loading from GitHub raw URLs.
- Converts Pandas DataFrames into Spark DataFrames.
- Adds Bronze metadata columns:
  - `source_file`
  - `ingestion_timestamp`
  - `bronze_load_id`
- Saves the following Bronze Delta tables:
  - `bronze_headcount`
  - `bronze_assignments`
  - `bronze_hours`
  - `bronze_costs`
  - `bronze_goals`
  - `bronze_clients`

### 02 — Validate Bronze

The Bronze validation notebook audits the raw ingested tables before transformation.

Main checks:

- Table existence.
- Row counts.
- Expected business columns.
- Required Bronze metadata columns.

Output table:

- `bronze_quality_log`

### 03 — Transform Silver

The Silver transformation notebook cleans, standardizes and validates the Bronze data.

Main actions:

- Normalizes business values such as gender, employment status, regions, contract types and periods.
- Converts dates and numeric fields into analytical types.
- Validates primary identifiers and logical keys.
- Validates foreign key relationships across cleaned Silver entities.
- Separates critical rejected records and warning-level issues.
- Saves cleaned Silver Delta tables.

Silver tables created:

- `silver_employees`
- `silver_clients`
- `silver_assignments`
- `silver_hours`
- `silver_costs`
- `silver_goals`
- `silver_rejected_records`

### 04 — Validate Silver

The Silver validation notebook audits the cleaned Silver layer and stores validation evidence.

Main checks:

- Table existence and row counts.
- Non-null and unique identifiers.
- Logical composite keys.
- Referential integrity between Silver tables.
- Business metric validity.
- Warning-level monitoring for non-critical issues.

Output table:

- `silver_quality_log`

### 05 — Build Gold

The Gold build notebook creates the analytical model for reporting.

Gold dimensions:

- `dim_region`
- `dim_date`
- `dim_employee`
- `dim_client`

Gold fact tables:

- `fact_workforce_monthly`
- `fact_goals_monthly`

Gold design decisions:

- Source identifiers from Silver are preserved for traceability.
- Model-owned numeric surrogate keys are generated in Gold.
- Facts use Gold keys such as:
  - `date_key`
  - `employee_key`
  - `client_key`
  - `region_key`
- `fact_workforce_monthly` keeps `hours_record_id`, `employee_id`, `client_id`, `project_id` and `period` for traceability.
- `fact_goals_monthly` keeps `goal_record_id`, `client_id`, `region_id` and `period` for traceability.

### 06 — Validate Gold

The Gold validation notebook audits the analytical model and stores validation evidence.

Main checks:

- Gold table existence.
- Row counts.
- Surrogate key uniqueness and non-null checks.
- Fact-to-dimension foreign key checks.
- Business metric ranges.
- Goal target validity.

Output table:

- `gold_quality_log`

## Databricks Job Orchestration

The full Bronze, Silver and Gold pipeline is orchestrated using a Databricks Job.

The Job runs the notebooks sequentially, from raw ingestion to Gold validation, and can be executed manually or through a monthly schedule.

The Job configuration is versioned in the repository as YAML:

- `databricks/workbridge_job_config.yml`

For more details, see [`docs/databricks_job_orchestration.md`](docs/databricks_job_orchestration.md).

## Data Quality Strategy

The project separates data quality issues into two levels:

### Critical issues

Critical issues exclude records from the corresponding Silver business table because they would compromise model integrity or downstream reporting.

Examples:

- Missing primary identifiers.
- Invalid employment status.
- Termination date earlier than hire date.
- Invalid client region.
- Foreign keys that do not exist in cleaned Silver dimensions.
- Invalid hours, costs or goals.
- Conflicting duplicated records.

### Warning-level issues

Warning-level issues are preserved for traceability and review when they do not block core KPI computation.

Examples:

- Invalid employee email format.
- Missing account manager.
- Potential duplicate client names.
- Exact duplicated records that can be deduplicated.
- Employees with non-normalizable region values.

Invalid emails are not rejected because they do not prevent workforce KPI calculation. Instead, they are preserved in Silver with an `email_is_valid` flag.

Employees with missing or non-normalizable regions are monitored as warning-level issues, while invalid client regions are treated as critical because client region is used for regional reporting and downstream fact relationships.

Rejecting clients with invalid or non-normalizable regions also causes related assignments, hours and goals to be rejected in Silver. This is intentional because the Silver layer prioritizes model integrity and reliable regional reporting.

## Gold Analytical Model

The Gold layer is modeled as a dimensional analytical model for reporting.

It includes four dimensions:

- `dim_date`
- `dim_region`
- `dim_employee`
- `dim_client`

And two fact tables:

- `fact_workforce_monthly`
- `fact_goals_monthly`

The implemented model follows a fact constellation schema, with a controlled snowflake-style normalization through the shared `dim_region` dimension.

For more details, see [`docs/data_model.md`](docs/data_model.md).

## Surrogate Keys

Gold uses model-owned numeric surrogate keys instead of relying only on source identifiers.

Examples:

- `employee_key`
- `client_key`
- `region_key`
- `date_key`
- `workforce_fact_key`
- `goals_fact_key`

Original identifiers such as `employee_id`, `client_id`, `region_id`, `hours_record_id` and `goal_record_id` are preserved for traceability.

## SCD Type 2 Readiness

`dim_employee` includes basic SCD Type 2 columns:

- `valid_from`
- `valid_to`
- `is_current`

Since the current synthetic dataset contains a single cleaned employee snapshot, the project does not perform historical versioning yet. All employee records are loaded as current records.

In a future incremental load, SCD Type 2 logic could compare incoming employee records against existing current records and create a new version when tracked attributes such as department, role, seniority, region or employment status change.

## Main KPIs

The model supports executive reporting for KPIs such as:

- Headcount
- New hires
- Terminations
- Turnover rate
- Cost by region
- Capacity utilization
- Billable utilization
- Goal achievement
- Worked hours by client
- Billable hours by month
- Workforce cost by client and region
- Target vs actual utilization
- Target vs actual cost

## Current Project Status

Implemented:

- Synthetic source datasets.
- Bronze ingestion notebook.
- Bronze quality validation notebook.
- Silver transformation notebook.
- Silver quality validation notebook.
- Gold analytical model notebook.
- Gold quality validation notebook.
- Databricks Job orchestration with monthly schedule.
- Delta tables for Bronze, Silver and Gold layers.
- Rejected records table.
- Bronze, Silver and Gold quality logs.
- Gold dimensional data model documentation.
- Job orchestration documentation and execution evidence.

Pending / next steps:

- Connect Gold tables to Power BI.
- Build the executive dashboard.
- Create a sample exportable PDF executive report.
- Expand final user-facing dashboard documentation.