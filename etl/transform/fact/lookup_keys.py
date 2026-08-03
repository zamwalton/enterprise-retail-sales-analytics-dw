"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : lookup_keys.py
Purpose : Replace Business Keys with Surrogate Keys
============================================================
"""

import pandas as pd

from etl.utils import logger


def lookup_dimension_keys(
    fact: pd.DataFrame,
    dim_customer: pd.DataFrame,
    dim_employee: pd.DataFrame,
    dim_store: pd.DataFrame,
    dim_product: pd.DataFrame,
    dim_promotion: pd.DataFrame,
    dim_date: pd.DataFrame,
) -> pd.DataFrame:
    """
    Replace business keys with warehouse surrogate keys.
    """

    logger.info("Looking up surrogate keys...")

    # ==========================================================
    # Customer
    # ==========================================================

    fact = fact.merge(
        dim_customer[["customer_id", "customer_key"]],
        on="customer_id",
        how="left",
    )

    # ==========================================================
    # Employee
    # ==========================================================

    fact = fact.merge(
        dim_employee[["employee_id", "employee_key"]],
        on="employee_id",
        how="left",
    )

    # ==========================================================
    # Store
    # ==========================================================

    fact = fact.merge(
        dim_store[["store_id", "store_key"]],
        on="store_id",
        how="left",
    )

    # ==========================================================
    # Product
    # ==========================================================

    fact = fact.merge(
        dim_product[["product_id", "product_key"]],
        on="product_id",
        how="left",
    )

    # ==========================================================
    # Promotion
    # ==========================================================

    fact = fact.merge(
        dim_promotion[["promotion_id", "promotion_key"]],
        on="promotion_id",
        how="left",
    )

    fact["promotion_key"] = (
    fact["promotion_key"]
        .fillna(0)
        .astype(int)
    )

    # ==========================================================
    # Date
    # ==========================================================

    fact["transaction_date"] = pd.to_datetime(
    fact["transaction_date"]
    ).dt.normalize()

    dim_date_lookup = dim_date[
        ["full_date", "date_key"]
     ].copy()

    dim_date_lookup["full_date"] = pd.to_datetime(
        dim_date_lookup["full_date"]
     ).dt.normalize()

    fact = fact.merge(
        dim_date_lookup,
        left_on="transaction_date",
        right_on="full_date",
        how="left",
    )

    fact.drop(columns=["full_date"], inplace=True)

    # ==========================================================
    # Validate Dimension Key Lookups
    # ==========================================================

    required_keys = [
        "customer_key",
        "employee_key",
        "store_key",
        "product_key",
        "date_key",
    ]

    for key in required_keys:
        missing_count = fact[key].isna().sum()

        if missing_count > 0:
            raise ValueError(
                f"Surrogate key lookup failed for {key}: "
                f"{missing_count:,} rows have no matching dimension record."
            )

    fact["customer_key"] = fact["customer_key"].astype(int)
    fact["employee_key"] = fact["employee_key"].astype(int)
    fact["store_key"] = fact["store_key"].astype(int)
    fact["product_key"] = fact["product_key"].astype(int)
    fact["date_key"] = fact["date_key"].astype(int)

    logger.info("Surrogate key lookup completed.")

    return fact