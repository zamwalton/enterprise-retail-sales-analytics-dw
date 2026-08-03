"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : supplier.py
Purpose : Transform Supplier Dimension
============================================================
"""

import pandas as pd

from etl.utils import (
    logger,
    add_surrogate_key,
)


def transform_supplier(
    suppliers: pd.DataFrame,
) -> pd.DataFrame:
    """
    Transform supplier source data into the
    dim_supplier warehouse structure.
    """

    logger.info("Transforming Supplier Dimension...")

    # ==========================================================
    # Copy Source Data
    # ==========================================================

    dim_supplier = suppliers.copy()

    # ==========================================================
    # SCD Type 2 Columns
    # ==========================================================

    dim_supplier["effective_start_date"] = (
        pd.Timestamp.now().date()
    )

    dim_supplier["effective_end_date"] = (
        pd.Timestamp("9999-12-31").date()
    )

    dim_supplier["is_current"] = True

    # ==========================================================
    # Audit Columns
    # ==========================================================

    now = pd.Timestamp.now()

    dim_supplier["created_date"] = now
    dim_supplier["updated_date"] = now

    # ==========================================================
    # Surrogate Key
    # ==========================================================

    dim_supplier = add_surrogate_key(
        dim_supplier,
        "supplier_key",
    )

    # ==========================================================
    # Select Warehouse Columns
    # ==========================================================

    dim_supplier = dim_supplier[
        [
            "supplier_key",
            "supplier_id",
            "supplier_name",
            "supplier_category",
            "contact_name",
            "phone",
            "email",
            "city",
            "state",
            "country",
            "supplier_status",
            "effective_start_date",
            "effective_end_date",
            "is_current",
            "created_date",
            "updated_date",
        ]
    ]

    # ==========================================================
    # Data Quality Validation
    # ==========================================================

    valid_categories = {
        "Local",
        "National",
        "International",
    }

    invalid_categories = (
        ~dim_supplier["supplier_category"]
        .isin(valid_categories)
    ).sum()

    if invalid_categories > 0:
        raise ValueError(
            f"Supplier validation failed. "
            f"{invalid_categories} rows have an invalid "
            f"supplier category."
        )

    valid_statuses = {
        "Active",
        "Inactive",
    }

    invalid_statuses = (
        ~dim_supplier["supplier_status"]
        .isin(valid_statuses)
    ).sum()

    if invalid_statuses > 0:
        raise ValueError(
            f"Supplier validation failed. "
            f"{invalid_statuses} rows have an invalid "
            f"supplier status."
        )

    invalid_scd_dates = (
        dim_supplier["effective_end_date"]
        < dim_supplier["effective_start_date"]
    ).sum()

    if invalid_scd_dates > 0:
        raise ValueError(
            f"Supplier SCD validation failed. "
            f"{invalid_scd_dates} rows have invalid "
            f"effective dates."
        )

    # ==========================================================
    # Logging
    # ==========================================================

    logger.info(
        "Supplier Dimension : %s rows",
        f"{len(dim_supplier):,}",
    )

    return dim_supplier