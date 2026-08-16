"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : product.py
Purpose : Transform Product Dimension
============================================================
"""

import pandas as pd

from etl.utils.utils import (
    logger,
    add_surrogate_key,
)


def transform_product(
    products: pd.DataFrame,
    effective_start_date=None,
) -> pd.DataFrame:
    """
    Transform product source data into the SCD Type 2
    dim_product structure.

    Parameters
    ----------
    products : pd.DataFrame
        Product source data.

    effective_start_date : optional
        Initial effective date for the SCD Type 2 version.
        If not supplied, today's date is used for backward
        compatibility.

    Returns
    -------
    pd.DataFrame
        Transformed Product Dimension.
    """

    logger.info("Transforming Product Dimension...")

    # ==========================================================
    # Copy Source Data
    # ==========================================================

    dim_product = products.copy()

    # ==========================================================
    # Rename Source Column to Warehouse Column
    # ==========================================================

    dim_product = dim_product.rename(
        columns={
            "cost_price": "standard_cost"
        }
    )

    # ==========================================================
    # Handle Optional Source Attributes
    # ==========================================================

    if "subcategory" not in dim_product.columns:
        dim_product["subcategory"] = None

    # ==========================================================
    # Determine Initial SCD Type 2 Effective Date
    # ==========================================================

    if effective_start_date is None:
        effective_start_date = pd.Timestamp.now().normalize()
    else:
        effective_start_date = pd.Timestamp(
            effective_start_date
        ).normalize()

    # ==========================================================
    # SCD Type 2 Columns
    # ==========================================================

    dim_product["effective_start_date"] = (
        effective_start_date
    )

    dim_product["effective_end_date"] = pd.Timestamp(
        "9999-12-31"
    )

    dim_product["is_current"] = True

    # ==========================================================
    # Audit Columns
    # ==========================================================

    current_timestamp = pd.Timestamp.now()

    dim_product["created_date"] = current_timestamp
    dim_product["updated_date"] = current_timestamp

    # ==========================================================
    # Surrogate Key
    # ==========================================================

    dim_product = add_surrogate_key(
        dim_product,
        "product_key",
    )

    # ==========================================================
    # Select Warehouse Columns
    # ==========================================================

    dim_product = dim_product[
        [
            "product_key",
            "product_id",
            "product_name",
            "brand",
            "category",
            "subcategory",
            "supplier_id",
            "standard_cost",
            "selling_price",
            "product_status",
            "effective_start_date",
            "effective_end_date",
            "is_current",
            "created_date",
            "updated_date",
        ]
    ]

    # ==========================================================
    # Validate Pricing Rule
    # ==========================================================

    invalid_prices = (
        dim_product["selling_price"]
        < dim_product["standard_cost"]
    ).sum()

    if invalid_prices > 0:
        raise ValueError(
            f"Product pricing validation failed. "
            f"{invalid_prices} rows have selling_price "
            f"lower than standard_cost."
        )

    logger.info(
        "Product Dimension : %s rows",
        f"{len(dim_product):,}",
    )

    return dim_product