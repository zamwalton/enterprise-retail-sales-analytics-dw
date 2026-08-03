"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : validate_dimensions.py
Purpose : Central Dimension Data Quality Validation
============================================================
"""

import pandas as pd

from etl.utils import logger

from etl.validation.completeness import validate_not_null
from etl.validation.uniqueness import validate_unique
from etl.validation.business_rules import (
    validate_date_order,
    validate_promotion_rules,
)


def validate_customer_dimension(
    df: pd.DataFrame,
) -> None:
    """
    Validate Customer Dimension before warehouse loading.
    """

    logger.info("Validating Customer Dimension...")

    validate_not_null(
        df,
        [
            "customer_id",
            "customer_name",
            "email",
        ],
    )

    validate_unique(
        df,
        ["customer_id"],
    )

    logger.info(
        "Customer Dimension validation passed."
    )


def validate_employee_dimension(
    df: pd.DataFrame,
) -> None:
    """
    Validate Employee Dimension before warehouse loading.
    """

    logger.info("Validating Employee Dimension...")

    validate_not_null(
        df,
        [
            "employee_id",
            "employee_name",
        ],
    )

    validate_unique(
        df,
        ["employee_id"],
    )

    logger.info(
        "Employee Dimension validation passed."
    )


def validate_store_dimension(
    df: pd.DataFrame,
) -> None:
    """
    Validate Store Dimension before warehouse loading.
    """

    logger.info("Validating Store Dimension...")

    validate_not_null(
        df,
        [
            "store_id",
            "store_name",
            "store_type",
            "country",
            "store_status",
        ],
    )

    validate_unique(
        df,
        ["store_id"],
    )

    logger.info(
        "Store Dimension validation passed."
    )


def validate_supplier_dimension(
    df: pd.DataFrame,
) -> None:
    """
    Validate Supplier Dimension before warehouse loading.
    """

    logger.info("Validating Supplier Dimension...")

    validate_not_null(
        df,
        [
            "supplier_id",
            "supplier_name",
        ],
    )

    validate_unique(
        df,
        ["supplier_id"],
    )

    logger.info(
        "Supplier Dimension validation passed."
    )


def validate_product_dimension(
    df: pd.DataFrame,
) -> None:
    """
    Validate Product Dimension before warehouse loading.
    """

    logger.info("Validating Product Dimension...")

    validate_not_null(
        df,
        [
            "product_id",
            "product_name",
            "supplier_id",
        ],
    )

    validate_unique(
        df,
        ["product_id"],
    )

    logger.info("Product Dimension validation passed.")


def validate_promotion_dimension(
    df: pd.DataFrame,
) -> None:
    """
    Validate Promotion Dimension before warehouse loading.
    """

    logger.info("Validating Promotion Dimension...")

    validate_not_null(
        df,
        [
            "promotion_id",
            "promotion_name",
            "promotion_type",
        ],
    )

    validate_unique(
        df,
        ["promotion_id"],
    )

    validate_promotion_rules(df)

    validate_date_order(
        df,
        "start_date",
        "end_date",
    )

    logger.info(
        "Promotion Dimension validation passed."
    )


def validate_date_dimension(
    df: pd.DataFrame,
) -> None:
    """
    Validate Date Dimension before warehouse loading.
    """

    logger.info("Validating Date Dimension...")

    validate_not_null(
        df,
        [
            "date_key",
            "full_date",
        ],
    )

    validate_unique(
        df,
        ["date_key"],
    )

    validate_unique(
        df,
        ["full_date"],
    )

    logger.info(
        "Date Dimension validation passed."
    )


def validate_all_dimensions(
    dimensions: dict[str, pd.DataFrame],
) -> None:
    """
    Execute all dimension validation rules.

    The function fails immediately if any dimension
    violates a data-quality rule.
    """

    logger.info(
        "========== DIMENSION VALIDATION STARTED =========="
    )

    validate_customer_dimension(
        dimensions["customer"]
    )

    validate_employee_dimension(
        dimensions["employee"]
    )

    validate_store_dimension(
        dimensions["store"]
    )

    validate_supplier_dimension(
        dimensions["supplier"]
    )

    validate_product_dimension(
        dimensions["product"]
    )

    validate_promotion_dimension(
        dimensions["promotion"]
    )

    validate_date_dimension(
        dimensions["date"]
    )

    logger.info(
        "========== DIMENSION VALIDATION PASSED =========="
    )