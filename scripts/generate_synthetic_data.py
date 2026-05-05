import json
import random
from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# Configuration
# ============================================================
# This section defines the main parameters used to generate the synthetic data.
# The random seed makes the generated data reproducible: every time the script
# runs, it will generate the same data.

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

# BASE_DIR points to the root folder of the project.
# RAW_DIR is the folder where the generated source files will be saved.

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Main dataset size configuration.

N_EMPLOYEES = 500
N_CLIENTS = 12
N_PROJECTS = 35

# The project will simulate one full year of monthly data.

PERIODS = pd.period_range(start="2026-01", periods=12, freq="M").astype(str)

# Standard regions used by the company.

REGIONS = ["LATAM", "NA", "EMEA", "APAC"]

# Countries are assigned based on each region to make the data more realistic.

REGION_COUNTRIES = {
    "LATAM": ["Argentina", "Brazil", "Chile", "Mexico", "Colombia"],
    "NA": ["United States", "Canada"],
    "EMEA": ["Spain", "Germany", "France", "United Kingdom", "Netherlands"],
    "APAC": ["India", "Japan", "Australia", "Singapore"],
}

# Region variants simulate inconsistent values coming from different systems.
# These values will later be standardized during the ETL process.

REGION_VARIANTS = {
    "LATAM": ["LATAM", "Latam", "Latin America", "latam"],
    "NA": ["NA", "North America", "north america"],
    "EMEA": ["EMEA", "Europe", "Europe Middle East Africa"],
    "APAC": ["APAC", "Asia Pacific", "Asia-Pacific"],
}

DEPARTMENTS = ["Data", "Engineering", "Operations", "Finance", "HR", "Customer Success"]
ROLES = ["Data Analyst", "Data Engineer", "Software Engineer", "Project Manager", "Business Analyst", "HR Specialist"]
SENIORITIES = ["Junior", "Semi Senior", "Senior", "Lead"]

# Gender variants simulate inconsistent categorical values.
# These will later be standardized into: Female, Male, Not specified.

GENDER_VALUES = ["Female", "Male", "Not specified"]
GENDER_VARIANTS = {
    "Female": ["Female", "F", "f"],
    "Male": ["Male", "M", "m"],
    "Not specified": ["Not specified", "Unknown", "N/A", ""],
}

FIRST_NAMES = [
    "Sofia", "Emma", "Olivia", "Mia", "Isabella", "Liam", "Noah", "Lucas",
    "Mateo", "Benjamin", "Ava", "Camila", "Valentina", "John", "James",
    "Emily", "Daniel", "Michael", "Lucia", "Martina"
]

LAST_NAMES = [
    "Garcia", "Smith", "Martinez", "Johnson", "Lopez", "Brown", "Gonzalez",
    "Davis", "Rodriguez", "Wilson", "Perez", "Anderson", "Sanchez",
    "Thomas", "Romero", "Taylor", "Ruiz", "Moore", "Silva", "Miller"
]


# ============================================================
# Helper functions
# ============================================================
# These functions are used several times throughout the script to avoid
# repeating logic.


def random_name():
    """Generate a random full name using predefined first and last names."""
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def random_date(start, end):
    """
    Generate a random date between two given dates.

    If the start date is after the end date, the function returns the end date.
    This prevents errors when generating termination or assignment dates close
    to the end of the simulated period.
    """
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    if start > end:
        return end

    days = (end - start).days
    return start + pd.to_timedelta(random.randint(0, days), unit="D")


def choose_region_variant(region):
    """Return a random inconsistent representation of a region."""
    return random.choice(REGION_VARIANTS[region])


def choose_gender_variant(gender):
    """Return a random inconsistent representation of a gender value."""
    return random.choice(GENDER_VARIANTS[gender])


def build_email(employee_name, employee_id):
    """Generate a standard corporate email for an employee."""
    clean_name = employee_name.lower().replace(" ", ".")
    return f"{clean_name}.{employee_id.lower()}@workbridge.com"


def introduce_invalid_emails(df, n=10):
    """
    Replace valid employee emails with invalid values.

    This simulates common data quality issues such as missing '@',
    incomplete domains, blank emails or invalid characters.
    """
    invalid_values = [
        "john.smith.workbridge.com",
        "maria@workbridge",
        "lucas@@workbridge.com",
        "",
        "invalid-email",
        "sofia@",
        "@workbridge.com",
        "ana.lopez@workbridge,com",
        "peter brown@workbridge.com",
        "michael#workbridge.com",
    ]

    indexes = random.sample(df.index.tolist(), n)

    for idx, value in zip(indexes, invalid_values):
        df.loc[idx, "employee_email"] = value

    return df


# ============================================================
# 1. Clients
# ============================================================
# This section generates the client master data.
# The output file will be: data/raw/clients.xlsx

industries = [
    "Banking", "Retail", "Healthcare", "Technology", "Telecommunications",
    "Manufacturing", "Energy", "Insurance"
]

# Industry variants simulate inconsistent values across CRM systems.

industry_variants = {
    "Technology": ["Technology", "Tech", "IT"],
    "Healthcare": ["Healthcare", "Health Care"],
    "Banking": ["Banking", "Financial Services"],
    "Retail": ["Retail"],
    "Telecommunications": ["Telecommunications", "Telecom"],
    "Manufacturing": ["Manufacturing"],
    "Energy": ["Energy"],
    "Insurance": ["Insurance"],
}

# Contract type variants simulate inconsistent commercial contract names.

contract_type_variants = {
    "Fixed Price": ["Fixed Price", "fixed price", "FP"],
    "Time and Materials": ["Time and Materials", "T&M", "time and materials"],
    "Managed Service": ["Managed Service", "managed services", "MS"],
}

base_client_names = [
    "Alpha Bank",
    "Nova Retail",
    "MediCore Health",
    "TechNova Systems",
    "BlueTel Communications",
    "IronWorks Manufacturing",
    "GreenGrid Energy",
    "SecureLife Insurance",
    "Andes Finance",
    "BrightMart",
    "CloudPath Technologies",
    "PrimeCare Services",
]

clients = []

# Generate the initial set of clients.

for i in range(1, N_CLIENTS + 1):
    region = random.choice(REGIONS)
    industry = random.choice(industries)
    contract_type = random.choice(list(contract_type_variants.keys()))

    clients.append({
        "client_id": f"C{i:03d}",
        "client_name": base_client_names[i - 1],
        "industry": random.choice(industry_variants[industry]),
        "client_region": choose_region_variant(region),
        "account_manager": random_name(),
        "contract_type": random.choice(contract_type_variants[contract_type]),
    })

clients_df = pd.DataFrame(clients)

# Add intentional potential duplicate client names.
# These records have different client IDs but similar names.
# Later, the ETL process can flag them for business review.

duplicate_clients = pd.DataFrame([
    {
        "client_id": "C013",
        "client_name": "NovaRetail",
        "industry": "Retail",
        "client_region": "LATAM",
        "account_manager": random_name(),
        "contract_type": "T&M",
    },
    {
        "client_id": "C014",
        "client_name": "Alpha Bank Ltd.",
        "industry": "Financial Services",
        "client_region": "Latin America",
        "account_manager": random_name(),
        "contract_type": "fixed price",
    },
    {
        "client_id": "C015",
        "client_name": "Tech Nova Systems",
        "industry": "Tech",
        "client_region": "North America",
        "account_manager": random_name(),
        "contract_type": "Managed Service",
    },
])

clients_df = pd.concat([clients_df, duplicate_clients], ignore_index=True)

# Add intentional missing account manager values.
# This is a warning-type issue, not necessarily a rejected record.

missing_manager_indexes = random.sample(clients_df.index.tolist(), 2)
clients_df.loc[missing_manager_indexes, "account_manager"] = ""


# ============================================================
# 2. Employees / Headcount
# ============================================================
# This section generates employee master data.
# The output file will be: data/raw/headcount.csv

employees = []

for i in range(1, N_EMPLOYEES + 1):
    region = random.choice(REGIONS)
    country = random.choice(REGION_COUNTRIES[region])

    hire_date = random_date("2023-01-01", "2026-11-30")

    # Around 12% of employees will be marked as terminated.
    # Status values are intentionally generated with different formats.

    if random.random() < 0.12:
        termination_date = random_date(hire_date + pd.Timedelta(days=60), "2026-12-31")
        employment_status = random.choice(["terminated", "Terminated", "TERMINATED"])
    else:
        termination_date = pd.NaT
        employment_status = random.choice(["active", "Active", "ACTIVE"])

    employee_name = random_name()
    employee_id = f"E{i:04d}"
    gender = random.choice(GENDER_VALUES)

    employees.append({
        "employee_id": employee_id,
        "employee_name": employee_name,
        "employee_email": build_email(employee_name, employee_id),
        "gender": choose_gender_variant(gender),
        "country": country,
        "region": choose_region_variant(region),
        "department": random.choice(DEPARTMENTS),
        "role": random.choice(ROLES),
        "seniority": random.choice(SENIORITIES),
        "hire_date": hire_date.date().isoformat(),
        "termination_date": "" if pd.isna(termination_date) else termination_date.date().isoformat(),
        "employment_status": employment_status,
    })

headcount_df = pd.DataFrame(employees)

# Add intentional duplicated employee records.

duplicate_indexes = random.sample(headcount_df.index.tolist(), 8)
headcount_df = pd.concat([headcount_df, headcount_df.loc[duplicate_indexes]], ignore_index=True)

# Add intentional invalid email formats.

headcount_df = introduce_invalid_emails(headcount_df, n=10)

# Add intentional invalid termination dates.
# These records have termination dates earlier than hire dates.

invalid_date_indexes = random.sample(headcount_df.index.tolist(), 3)

for idx in invalid_date_indexes:
    hire_date = pd.to_datetime(headcount_df.loc[idx, "hire_date"])
    invalid_termination_date = hire_date - pd.Timedelta(days=random.randint(1, 30))
    headcount_df.loc[idx, "termination_date"] = invalid_termination_date.date().isoformat()
    headcount_df.loc[idx, "employment_status"] = "terminated"

# Add intentional inconsistent employment status values.

status_indexes = random.sample(headcount_df.index.tolist(), 5)
status_values = ["inactive", "INACTIVE", "terminated ", " active", "unknown"]

for idx, status in zip(status_indexes, status_values):
    headcount_df.loc[idx, "employment_status"] = status


# ============================================================
# 3. Assignments
# ============================================================
# This section generates employee assignments to clients and projects.
# The output file will be: data/raw/assignments.xlsx

projects = [f"P{i:03d}" for i in range(1, N_PROJECTS + 1)]
assignments = []
assignment_counter = 1

# Only the original 12 clients are considered valid for assignments.
# The additional similar clients are used to simulate duplicate client issues.

valid_client_ids = clients_df[clients_df["client_id"].isin([f"C{i:03d}" for i in range(1, N_CLIENTS + 1)])]["client_id"].tolist()

for employee_id in headcount_df["employee_id"].drop_duplicates():
    number_of_assignments = np.random.choice([1, 1, 1, 2], p=[0.55, 0.20, 0.15, 0.10])

    for _ in range(number_of_assignments):
        start_date = random_date("2026-01-01", "2026-10-01")

        if random.random() < 0.25:
            end_date = random_date(start_date + pd.Timedelta(days=30), "2026-12-31")
            assignment_status = random.choice(["ended", "Ended", "closed"])
        else:
            end_date = ""
            assignment_status = random.choice(["active", "Active", "ACTIVE"])

        assignments.append({
            "assignment_id": f"A{assignment_counter:05d}",
            "employee_id": employee_id,
            "client_id": random.choice(valid_client_ids),
            "project_id": random.choice(projects),
            "assignment_start_date": pd.to_datetime(start_date).date().isoformat(),
            "assignment_end_date": "" if end_date == "" else pd.to_datetime(end_date).date().isoformat(),
            "allocation_percentage": random.choice([50, 75, 100]),
            "assignment_status": assignment_status,
        })

        assignment_counter += 1

assignments_df = pd.DataFrame(assignments)

# Add invalid client IDs.
# These records reference clients that do not exist in the client master data.

invalid_client_indexes = random.sample(assignments_df.index.tolist(), 3)
assignments_df.loc[invalid_client_indexes, "client_id"] = "C999"

# Add invalid employee IDs.
# These records reference employees that do not exist in the headcount data.

invalid_employee_indexes = random.sample(assignments_df.index.tolist(), 3)
assignments_df.loc[invalid_employee_indexes, "employee_id"] = "E9999"

# Add invalid allocation percentages.

invalid_allocation_indexes = random.sample(assignments_df.index.tolist(), 5)
invalid_allocations = [-20, 0, 150, 120, -5]

for idx, allocation in zip(invalid_allocation_indexes, invalid_allocations):
    assignments_df.loc[idx, "allocation_percentage"] = allocation

# Add invalid assignment date ranges.
# These records have an end date earlier than the start date.

invalid_assignment_date_indexes = random.sample(assignments_df.index.tolist(), 3)

for idx in invalid_assignment_date_indexes:
    start_date = pd.to_datetime(assignments_df.loc[idx, "assignment_start_date"])
    invalid_end_date = start_date - pd.Timedelta(days=random.randint(1, 20))
    assignments_df.loc[idx, "assignment_end_date"] = invalid_end_date.date().isoformat()
    assignments_df.loc[idx, "assignment_status"] = "ended"


# ============================================================
# 4. Hours
# ============================================================
# This section generates monthly time tracking data.
# The output file will be: data/raw/hours.csv

hours = []

for period in PERIODS:
    period_start = pd.Period(period).start_time
    period_end = pd.Period(period).end_time

    # Select employees that were active during the current period.

    active_employees = headcount_df[
        (pd.to_datetime(headcount_df["hire_date"]) <= period_end)
        & (
            (headcount_df["termination_date"] == "")
            | (pd.to_datetime(headcount_df["termination_date"], errors="coerce") >= period_start)
        )
    ]["employee_id"].drop_duplicates().tolist()

    # Not every employee reports hours every month.
    # This simulates employees without assignments, missing timesheets or inactive workload.

    sampled_employees = random.sample(
        active_employees,
        k=min(len(active_employees), int(len(active_employees) * 0.85))
    )

    for employee_id in sampled_employees:
        employee_assignments = assignments_df[assignments_df["employee_id"] == employee_id]

        if employee_assignments.empty:
            continue

        assignment = employee_assignments.sample(1, random_state=random.randint(1, 99999)).iloc[0]

        available_hours = 160
        worked_hours = max(0, int(np.random.normal(145, 25)))
        billable_hours = max(0, int(worked_hours * np.random.uniform(0.65, 0.95)))
        non_billable_hours = worked_hours - billable_hours
        overtime_hours = max(0, worked_hours - available_hours)

        hours.append({
            "period": period,
            "employee_id": employee_id,
            "client_id": assignment["client_id"],
            "project_id": assignment["project_id"],
            "available_hours": available_hours,
            "worked_hours": worked_hours,
            "billable_hours": billable_hours,
            "non_billable_hours": non_billable_hours,
            "overtime_hours": overtime_hours,
        })

hours_df = pd.DataFrame(hours)

# Add negative worked hours.

negative_hours_indexes = random.sample(hours_df.index.tolist(), 5)
hours_df.loc[negative_hours_indexes, "worked_hours"] = -8

# Add records where billable hours are greater than worked hours.

invalid_billable_indexes = random.sample(hours_df.index.tolist(), 5)

for idx in invalid_billable_indexes:
    hours_df.loc[idx, "worked_hours"] = 100
    hours_df.loc[idx, "billable_hours"] = 130
    hours_df.loc[idx, "non_billable_hours"] = -30

# Add invalid employee IDs.

invalid_hour_employee_indexes = random.sample(hours_df.index.tolist(), 3)
hours_df.loc[invalid_hour_employee_indexes, "employee_id"] = "E9999"

# Add invalid client IDs.

invalid_hour_client_indexes = random.sample(hours_df.index.tolist(), 3)
hours_df.loc[invalid_hour_client_indexes, "client_id"] = "C999"

# Add invalid period formats.

invalid_period_indexes = random.sample(hours_df.index.tolist(), 4)
invalid_period_values = ["2026/01", "Jan-2026", "202601", "2026.04"]

for idx, value in zip(invalid_period_indexes, invalid_period_values):
    hours_df.loc[idx, "period"] = value

# Add missing available hours.

missing_available_indexes = random.sample(hours_df.index.tolist(), 3)
hours_df.loc[missing_available_indexes, "available_hours"] = np.nan


# ============================================================
# 5. Costs
# ============================================================
# This section generates monthly workforce cost data.
# The output file will be: data/raw/costs.json

costs = []

# Salary ranges depend on seniority level.

seniority_cost = {
    "Junior": (1800, 2600),
    "Semi Senior": (2600, 4200),
    "Senior": (4200, 6500),
    "Lead": (6500, 9000),
}

employees_clean = headcount_df.drop_duplicates("employee_id")

for period in PERIODS:
    period_start = pd.Period(period).start_time
    period_end = pd.Period(period).end_time

    active_rows = employees_clean[
        (pd.to_datetime(employees_clean["hire_date"]) <= period_end)
        & (
            (employees_clean["termination_date"] == "")
            | (pd.to_datetime(employees_clean["termination_date"], errors="coerce") >= period_start)
        )
    ]

    for _, row in active_rows.iterrows():
        low, high = seniority_cost[row["seniority"]]
        salary_cost = round(random.uniform(low, high), 2)
        benefits_cost = round(salary_cost * random.uniform(0.12, 0.22), 2)
        total_cost = round(salary_cost + benefits_cost, 2)

        costs.append({
            "period": period,
            "employee_id": row["employee_id"],
            "region": row["region"],
            "salary_cost": salary_cost,
            "benefits_cost": benefits_cost,
            "total_cost": total_cost,
            "currency": random.choice(["USD", "usd", "U$D", "US Dollars"]),
        })

costs_df = pd.DataFrame(costs)

# Add missing total cost values.

missing_total_cost_indexes = random.sample(costs_df.index.tolist(), 5)
costs_df.loc[missing_total_cost_indexes, "total_cost"] = None

# Add negative salary cost values.

negative_cost_indexes = random.sample(costs_df.index.tolist(), 5)
costs_df.loc[negative_cost_indexes, "salary_cost"] = -3000

# Add inconsistent total cost calculations.
# In these rows, total_cost does not match salary_cost + benefits_cost.

inconsistent_total_indexes = random.sample(costs_df.index.tolist(), 5)

for idx in inconsistent_total_indexes:
    costs_df.loc[idx, "total_cost"] = 1000

# Add invalid employee IDs.

invalid_cost_employee_indexes = random.sample(costs_df.index.tolist(), 3)
costs_df.loc[invalid_cost_employee_indexes, "employee_id"] = "E9999"


# ============================================================
# 6. Goals
# ============================================================
# This section generates monthly target values by client and region.
# The output file will be: data/raw/goals.csv

goals = []

for period in PERIODS:
    for client_id in valid_client_ids:
        for region in REGIONS:
            goals.append({
                "period": period,
                "client_id": client_id,
                "region": choose_region_variant(region),
                "target_turnover_rate": round(random.uniform(0.02, 0.08), 4),
                "target_utilization_rate": round(random.uniform(0.72, 0.88), 4),
                "target_cost": round(random.uniform(180000, 420000), 2),
                "target_billable_hours": random.randint(2500, 6500),
            })

goals_df = pd.DataFrame(goals)

# Add utilization targets greater than 1.
# Since utilization is a rate, values should normally be between 0 and 1.

invalid_utilization_indexes = random.sample(goals_df.index.tolist(), 4)
goals_df.loc[invalid_utilization_indexes, "target_utilization_rate"] = 1.25

# Add negative turnover targets.

negative_turnover_indexes = random.sample(goals_df.index.tolist(), 3)
goals_df.loc[negative_turnover_indexes, "target_turnover_rate"] = -0.05

# Add missing target cost values.

missing_target_cost_indexes = random.sample(goals_df.index.tolist(), 3)
goals_df.loc[missing_target_cost_indexes, "target_cost"] = np.nan

# Add invalid client IDs.

invalid_goal_client_indexes = random.sample(goals_df.index.tolist(), 3)
goals_df.loc[invalid_goal_client_indexes, "client_id"] = "C999"


# ============================================================
# Export files
# ============================================================
# This section writes each generated DataFrame into the raw data folder.
# Each file uses a different format to simulate multiple internal systems.

headcount_df.to_csv(RAW_DIR / "headcount.csv", index=False)
assignments_df.to_excel(RAW_DIR / "assignments.xlsx", index=False)
hours_df.to_csv(RAW_DIR / "hours.csv", index=False)

with open(RAW_DIR / "costs.json", "w", encoding="utf-8") as f:
    json.dump(costs_df.to_dict(orient="records"), f, indent=2)

goals_df.to_csv(RAW_DIR / "goals.csv", index=False)
clients_df.to_excel(RAW_DIR / "clients.xlsx", index=False)

# Print a short execution summary in the terminal.

print("Synthetic data generated successfully.")
print(f"Files saved in: {RAW_DIR}")
print()
print("Generated files:")
print("- headcount.csv")
print("- assignments.xlsx")
print("- hours.csv")
print("- costs.json")
print("- goals.csv")
print("- clients.xlsx")
print()
print("Dataset sizes:")
print(f"- headcount.csv: {len(headcount_df)} rows")
print(f"- assignments.xlsx: {len(assignments_df)} rows")
print(f"- hours.csv: {len(hours_df)} rows")
print(f"- costs.json: {len(costs_df)} rows")
print(f"- goals.csv: {len(goals_df)} rows")
print(f"- clients.xlsx: {len(clients_df)} rows")