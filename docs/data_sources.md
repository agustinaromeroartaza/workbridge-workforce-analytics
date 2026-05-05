# Data Sources — WorkBridge Workforce Analytics

This document describes the synthetic data sources planned for the WorkBridge Workforce Analytics project.

The project simulates multiple internal systems used by WorkBridge Solutions to prepare monthly executive workforce reports.

## Source Overview

| Source File | Format | Simulated System | Purpose |
|---|---|---|---|
| `headcount.csv` | CSV | Human Resources System | Employee master data and employment status |
| `assignments.xlsx` | Excel | Project Management System | Employee assignments to clients and projects |
| `hours.csv` | CSV | Time Tracking System | Monthly available, worked and billable hours |
| `costs.json` | JSON | Finance System | Monthly workforce costs |
| `goals.csv` | CSV | Business Planning System | Monthly operational targets |
| `clients.xlsx` | Excel | CRM / Client Master Data | Client information |

---

## 1. `headcount.csv`

This file contains employee and HR-related information.

### Columns

| Column | Description |
|---|---|
| `employee_id` | Unique employee identifier |
| `employee_name` | Employee full name |
| `gender` | Employee gender |
| `country` | Employee country |
| `region` | Employee region |
| `department` | Department or business area |
| `role` | Employee job role |
| `seniority` | Employee seniority level |
| `hire_date` | Date when the employee joined the company |
| `termination_date` | Date when the employee left the company, if applicable |
| `employment_status` | Current status: active or terminated |

### Main Usage

- Calculate headcount.
- Identify new hires.
- Identify terminations.
- Calculate turnover rate.
- Analyze workforce distribution by region, department and seniority.

---

## 2. `assignments.xlsx`

This file contains employee assignments to clients and projects.

### Columns

| Column | Description |
|---|---|
| `assignment_id` | Unique assignment identifier |
| `employee_id` | Employee assigned to the client/project |
| `client_id` | Client receiving the service |
| `project_id` | Project identifier |
| `assignment_start_date` | Assignment start date |
| `assignment_end_date` | Assignment end date, if applicable |
| `allocation_percentage` | Percentage of the employee's capacity assigned to the project |
| `assignment_status` | Assignment status: active or ended |

### Main Usage

- Track which employees are assigned to each client.
- Analyze workforce allocation.
- Identify employees without active assignments.
- Support capacity utilization analysis.

---

## 3. `hours.csv`

This file contains monthly time tracking information.

### Columns

| Column | Description |
|---|---|
| `period` | Reporting period in YYYY-MM format |
| `employee_id` | Employee identifier |
| `client_id` | Client identifier |
| `project_id` | Project identifier |
| `available_hours` | Monthly available working hours |
| `worked_hours` | Total hours worked |
| `billable_hours` | Hours that can be billed to the client |
| `non_billable_hours` | Worked hours that are not billable |
| `overtime_hours` | Overtime hours worked |

### Main Usage

- Calculate capacity utilization.
- Calculate billable utilization.
- Analyze worked and available hours.
- Identify underutilization or overutilization.

---

## 4. `costs.json`

This file contains monthly workforce cost information.

### Columns

| Column | Description |
|---|---|
| `period` | Reporting period in YYYY-MM format |
| `employee_id` | Employee identifier |
| `region` | Region associated with the cost |
| `salary_cost` | Monthly salary cost |
| `benefits_cost` | Monthly benefits cost |
| `total_cost` | Total monthly workforce cost |
| `currency` | Currency of the cost value |

### Main Usage

- Calculate total workforce cost.
- Analyze cost by region.
- Compare costs against business targets.
- Calculate cost-related KPIs.

---

## 5. `goals.csv`

This file contains monthly business targets.

### Columns

| Column | Description |
|---|---|
| `period` | Reporting period in YYYY-MM format |
| `client_id` | Client identifier |
| `region` | Region related to the target |
| `target_turnover_rate` | Expected maximum turnover rate |
| `target_utilization_rate` | Expected capacity utilization rate |
| `target_cost` | Expected maximum cost |
| `target_billable_hours` | Expected billable hours |

### Main Usage

- Compare actual KPIs against targets.
- Calculate goal achievement.
- Support executive performance reporting.

---

## 6. `clients.xlsx`

This file contains client master data.

### Columns

| Column | Description |
|---|---|
| `client_id` | Unique client identifier |
| `client_name` | Client company name |
| `industry` | Client industry |
| `client_region` | Main client region |
| `account_manager` | WorkBridge account manager responsible for the client |
| `contract_type` | Type of commercial contract |

### Main Usage

- Enrich workforce and assignment data.
- Analyze KPIs by client.
- Group clients by industry or region.
- Support dashboard filtering.

---

## Intentional Data Quality Issues

The synthetic datasets include controlled data quality issues to simulate realistic problems commonly found in internal business systems.

These issues will be addressed during the ETL process through data cleaning, normalization, validation rules and rejected records outputs.

### `headcount.csv`

Planned data quality issues:

- Duplicated employee records.
- Inconsistent gender values.
- Invalid employee email formats.
- Inconsistent employment status values.
- Invalid termination dates.
- Region values written in different formats.

Examples:

- `F`, `Female`, `f` should be standardized as `Female`.
- `M`, `Male`, `m` should be standardized as `Male`.
- `Unknown`, `N/A` and blank values should be standardized as `Not specified`.
- `Latam`, `LATAM`, `Latin America` should be standardized into a single region identifier.

### `clients.xlsx`

Planned data quality issues:

- Potential duplicate client names.
- Inconsistent client region values.
- Inconsistent contract type values.
- Missing account manager values.

Examples:

- `Nova Retail`, `NovaRetail` and `Nova Retail Ltd.` may represent the same client.
- `fixed price`, `FP` and `Fixed Price` should be standardized.
- `T&M` should be standardized as `Time and Materials`.

### `assignments.xlsx`

Planned data quality issues:

- Invalid client identifiers.
- Invalid employee identifiers.
- Invalid allocation percentages.
- Assignment end dates earlier than assignment start dates.
- Inconsistent assignment status values.

Examples:

- `client_id = C999` does not exist in the client master data.
- `employee_id = E9999` does not exist in the employee master data.
- Allocation percentages below 0 or above 100 are invalid.

### `hours.csv`

Planned data quality issues:

- Negative worked hours.
- Billable hours greater than worked hours.
- Invalid employee identifiers.
- Invalid client identifiers.
- Invalid period formats.
- Missing available hours.

Examples:

- `worked_hours = -8` is invalid.
- `billable_hours = 130` with `worked_hours = 100` is invalid.
- `period = Jan-2026` should be reviewed or standardized.

### `costs.json`

Planned data quality issues:

- Missing total cost values.
- Negative salary cost values.
- Inconsistent total cost calculations.
- Inconsistent currency values.
- Invalid employee identifiers.
- Region values written in different formats.

Examples:

- `salary_cost = -3000` is invalid.
- `salary_cost + benefits_cost` should match `total_cost`.
- `usd`, `U$D` and `US Dollars` should be standardized as `USD`.

### `goals.csv`

Planned data quality issues:

- Utilization targets greater than 1.
- Negative turnover targets.
- Missing target cost values.
- Invalid client identifiers.
- Region values written in different formats.

Examples:

- `target_utilization_rate = 1.25` is invalid.
- `target_turnover_rate = -0.05` is invalid.
- `client_id = C999` does not exist in the client master data.