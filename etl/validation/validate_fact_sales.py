"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : validate_fact_sales.py
Purpose : Fact Sales Data Quality Validation
============================================================
"""

import pandas as pd

from etl.utils import logger

from etl.validation.completeness import validate_not_null
from etl.validation.uniqueness import validate_unique
from etl.validation.referential_integrity import (
    validate_referential_integrity,
)
from etl.validation.business_rules import (
    validate_positive_values,
    validate_non_negative_values,
    validate_sales_amounts,
)


def validate_fact_sales(
    fact_df: pd.DataFrame,
    dim_customer: pd.DataFrame,
    dim_employee: pd.DataFrame,
    dim_store: pd.DataFrame,
    dim_product: pd.DataFrame,
    dim_promotion: pd.DataFrame,
    dim_date: pd.DataFrame,
) -> None:
    """
    Execute all data-quality validations for Fact Sales.

    Validation categories:
        - Completeness
        - Uniqueness
        - Referential integrity
        - Positive values
        - Non-negative values
        - Sales amount business rules
    """

    logger.info(
        "========== FACT SALES VALIDATION STARTED =========="
    )

    # ======================================================
    # 1. COMPLETENESS
    # ======================================================

    validate_not_null(
        fact_df,
        [
            "transaction_id",
            "line_number",
            "date_key",
            "customer_key",
            "employee_key",
            "store_key",
            "product_key",
            "quantity",
            "unit_price",
            "discount_amount",
            "tax_amount",
            "total_amount",
        ],
    )

    # ======================================================
    # 2. UNIQUENESS
    # ======================================================

    validate_unique(
        fact_df,
        [
            "transaction_id",
            "line_number",
        ],
    )

    # ======================================================
    # 3. REFERENTIAL INTEGRITY
    # ======================================================

    validate_referential_integrity(
        fact_df,
        "customer_key",
        dim_customer,
        "customer_key",
    )

    validate_referential_integrity(
        fact_df,
        "employee_key",
        dim_employee,
        "employee_key",
    )

    validate_referential_integrity(
        fact_df,
        "store_key",
        dim_store,
        "store_key",
    )

    validate_referential_integrity(
        fact_df,
        "product_key",
        dim_product,
        "product_key",
    )

    validate_referential_integrity(
        fact_df,
        "promotion_key",
        dim_promotion,
        "promotion_key",
    )

    validate_referential_integrity(
        fact_df,
        "date_key",
        dim_date,
        "date_key",
    )

    # ======================================================
    # 4. POSITIVE VALUES
    # ======================================================

    validate_positive_values(
        fact_df,
        [
            "quantity",
            "unit_price",
        ],
    )

    # ======================================================
    # 5. NON-NEGATIVE VALUES
    # ======================================================

    validate_non_negative_values(
        fact_df,
        [
            "discount_amount",
            "tax_amount",
            "total_amount",
        ],
    )

    # ======================================================
    # 6. SALES AMOUNT BUSINESS RULE
    # ======================================================

    validate_sales_amounts(
        fact_df,
    )

    # ======================================================
    # VALIDATION COMPLETE
    # ======================================================

    logger.info(
        "========== FACT SALES VALIDATION PASSED =========="
    )