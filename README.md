# WorkBridge Workforce Analytics

End-to-end data analytics project focused on automating monthly workforce executive reports for a fictitious professional services company.

## Business Problem

WorkBridge Solutions prepares monthly executive reports for its corporate clients using manual Excel-based processes. These reports include workforce turnover, regional costs, capacity utilization and goal achievement.

The current process takes approximately three days per client and presents risks related to manual errors, inconsistent data, duplicated work and limited traceability.

## Project Objective

The objective of this project is to design and implement an automated data pipeline that integrates multiple internal data sources, applies data cleaning and transformation processes, builds an analytical data model, and feeds an interactive Power BI dashboard with exportable executive reports.

## Fictitious Company

WorkBridge Solutions is a fictitious professional services company that manages distributed workforce teams assigned to different corporate clients across multiple regions.

## Planned Architecture

Raw data sources  
→ Bronze layer  
→ Silver layer  
→ Gold analytical model  
→ Power BI dashboard  
→ PDF executive report

## Main KPIs

- Headcount
- New hires
- Terminations
- Turnover rate
- Cost by region
- Capacity utilization
- Billable utilization
- Goal achievement

## Planned Data Sources

- `headcount.csv` — employee and HR data
- `assignments.xlsx` — employee assignments to clients and projects
- `hours.csv` — monthly worked, available and billable hours
- `costs.json` — monthly workforce costs
- `goals.csv` — monthly business targets
- `clients.xlsx` — client master data

## Planned Tools

- Python
- Pandas / PySpark
- Databricks
- Power BI
- GitHub
- CSV, Excel and JSON files

## Expected Deliverables

- Synthetic source datasets
- Automated ETL pipeline
- Bronze, Silver and Gold datasets
- Data quality validation outputs
- Rejected records output
- Analytical data model
- Power BI dashboard
- Sample PDF executive report
- Technical documentation
- User manual

## Project Status

In progress.