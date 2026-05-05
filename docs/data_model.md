# Data Model — WorkBridge Workforce Analytics

This document describes the planned analytical data model for the WorkBridge Workforce Analytics project.

The model is designed to support executive reporting in Power BI using a simple dimensional structure.

## Modeling Approach

The project will use a dimensional model with:

- Dimension tables for descriptive business entities.
- One main fact table containing monthly workforce metrics.
- A monthly reporting grain by period, client and region.

The goal is to keep the model simple, clear and suitable for executive KPI analysis.

---

## Model Grain

The main analytical table will be built at the following level of detail:

| Grain Component | Description |
|---|---|
| `period` | Monthly reporting period |
| `client_id` | Client receiving the service |
| `region_id` | Region associated with the workforce activity |

This means that each row in the main fact table represents workforce performance for one client, in one region, during one month.

Example:

| period | client_id | region_id |
|---|---|---|
| 2026-01 | C001 | LATAM |
| 2026-01 | C002 | EMEA |
| 2026-02 | C001 | LATAM |

---

## Dimension Tables

### `dim_employee`

Contains employee descriptive information.

| Column | Description |
|---|---|
| `employee_id` | Unique employee identifier |
| `employee_name` | Employee full name |
| `gender` | Employee gender |
| `country` | Employee country |
| `region_id` | Employee region |
| `department` | Department or business area |
| `role` | Employee job role |
| `seniority` | Employee seniority level |
| `hire_date` | Employee hire date |
| `termination_date` | Employee termination date, if applicable |
| `employment_status` | Current employee status |

Main usage:

- Analyze workforce distribution.
- Filter KPIs by employee attributes.
- Support headcount and turnover calculations.

---

### `dim_client`

Contains client descriptive information.

| Column | Description |
|---|---|
| `client_id` | Unique client identifier |
| `client_name` | Client company name |
| `industry` | Client industry |
| `client_region` | Main client region |
| `account_manager` | Account manager responsible for the client |
| `contract_type` | Type of commercial contract |

Main usage:

- Analyze KPIs by client.
- Filter dashboards by industry, region and contract type.
- Support executive reporting by client.

---

### `dim_region`

Contains standardized region information used to validate and describe regional values across the analytical model.

| Column | Description |
|---|---|
| `region_id` | Unique region identifier |
| `region_name` | Standardized region name |

Main usage:

- Normalize regional values from different sources.
- Validate region identifiers used in Silver and Gold tables.
- Analyze cost, headcount and utilization by region.

---

### `dim_date`

Contains calendar information for reporting periods.

| Column | Description |
|---|---|
| `date_id` | Date identifier |
| `period` | Reporting period in YYYY-MM format |
| `year` | Reporting year |
| `month` | Reporting month number |
| `month_name` | Reporting month name |
| `quarter` | Reporting quarter |

Main usage:

- Analyze KPI trends over time.
- Filter dashboard visuals by month, quarter and year.

---

## Fact Table

### `fact_workforce_monthly`

This is the main analytical fact table for the project.

Each row represents workforce performance for one client, in one region, during one month.

| Column | Description |
|---|---|
| `period` | Monthly reporting period |
| `client_id` | Client identifier |
| `region_id` | Region identifier |
| `headcount` | Number of active employees |
| `new_hires` | Number of employees hired during the period |
| `terminations` | Number of employees terminated during the period |
| `available_hours` | Total available hours |
| `worked_hours` | Total worked hours |
| `billable_hours` | Total billable hours |
| `non_billable_hours` | Total non-billable hours |
| `overtime_hours` | Total overtime hours |
| `total_cost` | Total workforce cost |
| `target_turnover_rate` | Target turnover rate |
| `target_utilization_rate` | Target capacity utilization rate |
| `target_cost` | Target maximum cost |
| `target_billable_hours` | Target billable hours |
| `turnover_rate` | Actual turnover rate |
| `capacity_utilization` | Actual capacity utilization |
| `billable_utilization` | Actual billable utilization |
| `cost_goal_achievement` | Cost performance against target |
| `utilization_goal_achievement` | Utilization performance against target |
| `billable_hours_goal_achievement` | Billable hours performance against target |

---

## KPI Definitions

### Headcount

Number of active employees during the reporting period.

### New Hires

Number of employees with a hire date within the reporting period.

### Terminations

Number of employees with a termination date within the reporting period.

### Turnover Rate

`turnover_rate = terminations / average_headcount`

### Capacity Utilization

`capacity_utilization = worked_hours / available_hours`

### Billable Utilization

`billable_utilization = billable_hours / available_hours`

### Cost by Region

`cost_by_region = sum(total_cost) grouped by region`

### Cost Goal Achievement

`cost_goal_achievement = target_cost / total_cost`

For cost, a value greater than or equal to 1 means that the actual cost is within or below the target.

### Utilization Goal Achievement

`utilization_goal_achievement = capacity_utilization / target_utilization_rate`

### Billable Hours Goal Achievement

`billable_hours_goal_achievement = billable_hours / target_billable_hours`

---

## Model Notes

- The model is intentionally simple for the first version of the project.
- Only one main fact table will be created to avoid unnecessary complexity.
- The model can be expanded in future versions with additional fact tables if needed.
- The main focus is to support executive reporting and dashboard analysis