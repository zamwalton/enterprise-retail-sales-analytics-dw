"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : product_scd2.py
Purpose : SCD Type 2 Processing for Product Dimension
============================================================
"""

from datetime import date

import pandas as pd

from decimal import Decimal

from database.connection import get_connection
from etl.utils import logger


# ============================================================
# CONFIGURATION
# ============================================================

SCHEMA = "retail_dw"
TABLE = "dim_product"

BUSINESS_KEY = "product_id"

COMPARE_COLUMNS = [
    "product_name",
    "brand",
    "category",
    "subcategory",
    "supplier_id",
    "standard_cost",
    "selling_price",
    "product_status",
]


# ============================================================
# NORMALIZE VALUES
# ============================================================

def _normalize_value(value):
    """
    Normalize values before comparing source and warehouse
    records.
    """

    if pd.isna(value):
        return None

    # Normalize timestamps
    if isinstance(value, pd.Timestamp):
        return value.date()

    # Normalize numeric values
    if isinstance(value, (float, int)):
        return round(float(value), 2)

    if isinstance(value, Decimal):
        return round(float(value), 2)

    return value


# ============================================================
# PROCESS SCD TYPE 2
# ============================================================

def process_product_scd2(
    products: pd.DataFrame,
    effective_date: date | None = None,
) -> tuple[int, int]:
    """
    Apply SCD Type 2 processing to the Product dimension.

    Parameters
    ----------
    products : pd.DataFrame
        Transformed product source data.

    effective_date : date | None
        Date on which changes become effective.
        Defaults to today's date.

    Returns
    -------
    tuple[int, int]
        (inserted_versions, closed_versions)
    """

    if products.empty:
        logger.info(
            "SCD2 Product processing skipped. No source records."
        )
        return 0, 0

    if effective_date is None:
        effective_date = date.today()

    conn = None
    cursor = None

    inserted_versions = 0
    closed_versions = 0

    try:

        conn = get_connection()
        cursor = conn.cursor()

        logger.info(
            "========== PRODUCT SCD2 PROCESSING STARTED =========="
        )

        for _, source_row in products.iterrows():

            product_id = source_row[BUSINESS_KEY]

            # ------------------------------------------------
            # Get current warehouse version
            # ------------------------------------------------

            cursor.execute(
                f"""
                SELECT
                    product_key,
                    product_id,
                    product_name,
                    brand,
                    category,
                    subcategory,
                    supplier_id,
                    standard_cost,
                    selling_price,
                    product_status,
                    effective_start_date,
                    effective_end_date,
                    is_current
                FROM {SCHEMA}.{TABLE}
                WHERE product_id = %s
                  AND is_current = TRUE
                """,
                (product_id,),
            )

            current_row = cursor.fetchone()

            # ------------------------------------------------
            # NEW PRODUCT
            # ------------------------------------------------

            if current_row is None:

                cursor.execute(
                    f"""
                    INSERT INTO {SCHEMA}.{TABLE}
                    (
                        product_id,
                        product_name,
                        brand,
                        category,
                        subcategory,
                        supplier_id,
                        standard_cost,
                        selling_price,
                        product_status,
                        effective_start_date,
                        effective_end_date,
                        is_current,
                        created_date,
                        updated_date
                    )
                    VALUES
                    (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, TRUE,
                        CURRENT_TIMESTAMP,
                        CURRENT_TIMESTAMP
                    )
                    """,
                    (
                        source_row["product_id"],
                        source_row["product_name"],
                        _normalize_value(source_row["brand"]),
                        _normalize_value(source_row["category"]),
                        _normalize_value(source_row["subcategory"]),
                        _normalize_value(source_row["supplier_id"]),
                        _normalize_value(source_row["standard_cost"]),
                        _normalize_value(source_row["selling_price"]),
                        source_row["product_status"],
                        effective_date,
                        date(9999, 12, 31),
                    ),
                )

                inserted_versions += 1

                continue

            # ------------------------------------------------
            # EXISTING PRODUCT
            # ------------------------------------------------

            current = dict(
                zip(
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
                    ],
                    current_row,
                )
            )

            # ------------------------------------------------
            # Detect attribute changes
            # ------------------------------------------------

            changed = False

            for column in COMPARE_COLUMNS:

                source_value = _normalize_value(
                    source_row[column]
                )

                warehouse_value = _normalize_value(
                    current[column]
                )

                if source_value != warehouse_value:
                    changed = True
                    break

            # ------------------------------------------------
            # No change
            # ------------------------------------------------

            if not changed:
                continue

            # ------------------------------------------------
            # Close current version
            # ------------------------------------------------

            cursor.execute(
                f"""
                UPDATE {SCHEMA}.{TABLE}
                SET
                    effective_end_date = %s,
                    is_current = FALSE,
                    updated_date = CURRENT_TIMESTAMP
                WHERE product_key = %s
                  AND is_current = TRUE
                """,
                (
                    effective_date,
                    current["product_key"],
                ),
            )

            closed_versions += 1

            # ------------------------------------------------
            # Insert new version
            # ------------------------------------------------

            cursor.execute(
                f"""
                INSERT INTO {SCHEMA}.{TABLE}
                (
                    product_id,
                    product_name,
                    brand,
                    category,
                    subcategory,
                    supplier_id,
                    standard_cost,
                    selling_price,
                    product_status,
                    effective_start_date,
                    effective_end_date,
                    is_current,
                    created_date,
                    updated_date
                )
                VALUES
                (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, TRUE,
                    CURRENT_TIMESTAMP,
                    CURRENT_TIMESTAMP
                )
                """,
                (
                    source_row["product_id"],
                    source_row["product_name"],
                    _normalize_value(source_row["brand"]),
                    _normalize_value(source_row["category"]),
                    _normalize_value(source_row["subcategory"]),
                    _normalize_value(source_row["supplier_id"]),
                    _normalize_value(source_row["standard_cost"]),
                    _normalize_value(source_row["selling_price"]),
                    source_row["product_status"],
                    effective_date,
                    date(9999, 12, 31),
                ),
            )

            inserted_versions += 1

            logger.info(
                "SCD2 change detected for %s. "
                "Old version closed and new version inserted.",
                product_id,
            )

        conn.commit()

        logger.info(
            "========== PRODUCT SCD2 PROCESSING COMPLETED =========="
        )

        logger.info(
            "New versions inserted: %s",
            f"{inserted_versions:,}",
        )

        logger.info(
            "Old versions closed: %s",
            f"{closed_versions:,}",
        )

        return inserted_versions, closed_versions

    except Exception as e:

        if conn:
            conn.rollback()

        logger.error(
            "Product SCD2 processing failed: %s",
            e,
        )

        raise

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()