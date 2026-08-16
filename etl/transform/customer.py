"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : customer.py
Purpose : Transform Customer Dimension
============================================================
"""

import pandas as pd

from etl.utils.utils import (
    add_surrogate_key,
    logger,
)


def transform_customer(
    customers: pd.DataFrame,
    effective_start_date=None,
) -> pd.DataFrame:
    """
    Transform customer source data into the SCD Type 2
    dim_customer structure.

    Parameters
    ----------
    customers : pd.DataFrame
        Customer source data.

    effective_start_date : optional
        Date from which the initial customer dimension
        version becomes effective. If not provided, the
        current date is used.

    Returns
    -------
    pd.DataFrame
        Customer dimension.
    """

    logger.info("Transforming Customer Dimension...")

    # ==========================================================
    # Copy Source Data
    # ==========================================================

    dim_customer = customers.copy()

    # ==========================================================
    # Handle Optional SCD Attributes
    # ==========================================================

    if "date_of_birth" not in dim_customer.columns:
        dim_customer["date_of_birth"] = pd.NaT

    if "loyalty_tier" not in dim_customer.columns:
        dim_customer["loyalty_tier"] = None

    # ==========================================================
    # SCD Type 2 Columns
    # ==========================================================

    if effective_start_date is None:
        effective_start_date = pd.Timestamp.now().normalize()
    else:
        effective_start_date = pd.Timestamp(
            effective_start_date
        ).normalize()

    dim_customer["effective_start_date"] = (
        effective_start_date
    )

    dim_customer["effective_end_date"] = pd.Timestamp(
        "9999-12-31"
    )

    dim_customer["is_current"] = True

    # ==========================================================
    # Audit Columns
    # ==========================================================

    dim_customer["created_date"] = pd.Timestamp.now()

    dim_customer["updated_date"] = pd.Timestamp.now()

    # ==========================================================
    # Surrogate Key
    # ==========================================================

    dim_customer = add_surrogate_key(
        dim_customer,
        "customer_key",
    )

    # ==========================================================
    # Select Warehouse Columns
    # ==========================================================

    dim_customer = dim_customer[
        [
            "customer_key",
            "customer_id",
            "customer_name",
            "gender",
            "date_of_birth",
            "email",
            "phone",
            "city",
            "state",
            "country",
            "loyalty_tier",
            "effective_start_date",
            "effective_end_date",
            "is_current",
            "created_date",
            "updated_date",
        ]
    ]

    logger.info(
        "Customer Dimension : %s rows",
        f"{len(dim_customer):,}",
    )

    return dim_customer