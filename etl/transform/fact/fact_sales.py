"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : fact_sales.py
Purpose : Build Fact Sales Table
============================================================
"""

import pandas as pd

from etl.utils import (
    logger,
    add_audit_columns,
)


def build_fact_sales(fact: pd.DataFrame) -> pd.DataFrame:
    """
    Build the final fact_sales table.
    """

    logger.info("Building Fact Sales...")

    fact = fact.copy()

    # ==========================================================
    # Add Fact Surrogate Key
    # ==========================================================

    fact.insert(
        0,
        "sales_key",
        range(1, len(fact) + 1),
    )

    # ==========================================================
    # Select Warehouse Columns
    # ==========================================================

    fact = fact[
        [
            "sales_key",
            "transaction_id",
            "line_number",
            "date_key",
            "customer_key",
            "employee_key",
            "store_key",
            "product_key",
            "promotion_key",
            "quantity",
            "unit_price",
            "discount_amount",
            "tax_amount",
            "total_amount",
            "payment_method",
            "transaction_status",
        ]
    ].copy()

    # ==========================================================
    # Data Validation
    # ==========================================================

    required_key_columns = [
        "date_key",
        "customer_key",
        "employee_key",
        "store_key",
        "product_key",
        "promotion_key",
    ]

    for column in required_key_columns:

        null_count = fact[column].isna().sum()

        if null_count > 0:
            raise ValueError(
                f"Fact validation failed. "
                f"{null_count:,} rows have NULL {column}."
            )

    # ==========================================================
    # Numeric Validation
    # ==========================================================

    if (fact["quantity"] <= 0).any():
        raise ValueError(
            "Fact validation failed. "
            "Quantity must be greater than zero."
        )

    if (fact["unit_price"] < 0).any():
        raise ValueError(
            "Fact validation failed. "
            "Unit price cannot be negative."
        )

    if (fact["discount_amount"] < 0).any():
        raise ValueError(
            "Fact validation failed. "
            "Discount amount cannot be negative."
        )

    if (fact["tax_amount"] < 0).any():
        raise ValueError(
            "Fact validation failed. "
            "Tax amount cannot be negative."
        )

    # ==========================================================
    # Duplicate Grain Validation
    # ==========================================================

    duplicate_count = fact.duplicated(
        subset=[
            "transaction_id",
            "line_number",
        ]
    ).sum()

    if duplicate_count > 0:
        raise ValueError(
            f"Fact validation failed. "
            f"{duplicate_count:,} duplicate transaction lines found."
        )

    # ==========================================================
    # Audit Columns
    # ==========================================================

    fact = add_audit_columns(fact)

    # ==========================================================
    # Final Logging
    # ==========================================================

    logger.info(
        "Fact Sales : %s rows",
        f"{len(fact):,}",
    )

    return fact