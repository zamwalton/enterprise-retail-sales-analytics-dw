"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : hr_generator.py
Purpose : Generate HR Employee Source Data
============================================================
"""

import random
from faker import Faker

fake = Faker("en_IN")


DEPARTMENTS = [
    "Sales",
    "Operations",
    "Inventory",
    "Finance",
    "HR",
    "IT",
]

JOB_TITLES = {
    "Sales": ["Sales Associate", "Senior Sales Associate", "Store Manager"],
    "Operations": ["Operations Executive", "Operations Manager"],
    "Inventory": ["Inventory Executive", "Inventory Manager"],
    "Finance": ["Accountant", "Finance Manager"],
    "HR": ["HR Executive", "HR Manager"],
    "IT": ["Support Engineer", "System Administrator"],
}

EMPLOYMENT_STATUS = [
    "Active",
    "On Leave",
    "Terminated",
]


def generate_employees(num_employees: int, num_stores: int):

    employees = []

    for employee_id in range(1, num_employees + 1):

        department = random.choice(DEPARTMENTS)

        employees.append(
            {
                "employee_id": f"EMP{employee_id:05d}",
                "employee_name": fake.name(),
                "gender": random.choice(["Male", "Female"]),
                "department": department,
                "job_title": random.choice(JOB_TITLES[department]),

                # NEW
                "store_id": f"STORE{random.randint(1, num_stores):03d}",

                "hire_date": fake.date_between(
                    start_date="-10y",
                    end_date="today",
                ),
                "salary": random.randint(25000, 120000),
                "employment_status": random.choices(
                    EMPLOYMENT_STATUS,
                    weights=[90, 5, 5],
                    k=1,
                )[0],
            }
        )

    return employees