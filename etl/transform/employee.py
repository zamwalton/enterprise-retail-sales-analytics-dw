"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : employee.py
Purpose : Transform Employee Dimension
============================================================
"""

import pandas as pd

from etl.utils.utils import (
    add_surrogate_key,
    logger,
)


def transform_employee(employees: pd.DataFrame) -> pd.DataFrame:
    """
    Transform employee source data into the SCD Type 2
    dim_employee structure.
    """

    logger.info("Transforming Employee Dimension...")

    # ==========================================================
    # Copy Source Data
    # ==========================================================

    dim_employee = employees.copy()

    # ==========================================================
    # Handle Optional Source Attributes
    # ==========================================================

    if "manager_id" not in dim_employee.columns:
        dim_employee["manager_id"] = None

    if "hire_date" not in dim_employee.columns:
        dim_employee["hire_date"] = pd.NaT

    if "employment_status" not in dim_employee.columns:
        dim_employee["employment_status"] = "Active"

    # ==========================================================
    # SCD Type 2 Columns
    # ==========================================================

    effective_start_date = pd.Timestamp.now().normalize()

    dim_employee["effective_start_date"] = (
        effective_start_date
    )

    dim_employee["effective_end_date"] = pd.Timestamp(
        "9999-12-31"
    )

    dim_employee["is_current"] = True

    # ==========================================================
    # Audit Columns
    # ==========================================================

    dim_employee["created_date"] = pd.Timestamp.now()

    dim_employee["updated_date"] = pd.Timestamp.now()

    # ==========================================================
    # Surrogate Key
    # ==========================================================

    dim_employee = add_surrogate_key(
        dim_employee,
        "employee_key",
    )

    # ==========================================================
    # Select Warehouse Columns
    # ==========================================================

    dim_employee = dim_employee[
        [
            "employee_key",
            "employee_id",
            "employee_name",
            "department",
            "job_title",
            "manager_id",
            "hire_date",
            "employment_status",
            "effective_start_date",
            "effective_end_date",
            "is_current",
            "created_date",
            "updated_date",
        ]
    ]

    logger.info(
        "Employee Dimension : %s rows",
        f"{len(dim_employee):,}",
    )

    return dim_employee