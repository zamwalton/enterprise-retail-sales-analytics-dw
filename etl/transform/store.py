"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : store.py
Purpose : Transform Store Dimension
============================================================
"""

import pandas as pd

from etl.utils.utils import (
    logger,
    add_surrogate_key,
)


def transform_store(stores: pd.DataFrame) -> pd.DataFrame:
    """
    Transform store source data into the SCD Type 2
    dim_store structure.
    """

    logger.info("Transforming Store Dimension...")

    # ==========================================================
    # Copy Source Data
    # ==========================================================

    dim_store = stores.copy()

    # ==========================================================
    # Handle Optional Source Attributes
    # ==========================================================

    if "opening_date" not in dim_store.columns:
        dim_store["opening_date"] = pd.NaT

    if "store_status" not in dim_store.columns:
        dim_store["store_status"] = "Active"

    # ==========================================================
    # SCD Type 2 Columns
    # ==========================================================

    effective_start_date = pd.Timestamp.now().normalize()

    dim_store["effective_start_date"] = (
        effective_start_date
    )

    dim_store["effective_end_date"] = pd.Timestamp(
        "9999-12-31"
    )

    dim_store["is_current"] = True

    # ==========================================================
    # Audit Columns
    # ==========================================================

    dim_store["created_date"] = pd.Timestamp.now()

    dim_store["updated_date"] = pd.Timestamp.now()

    # ==========================================================
    # Surrogate Key
    # ==========================================================

    dim_store = add_surrogate_key(
        dim_store,
        "store_key",
    )

    # ==========================================================
    # Select Warehouse Columns
    # ==========================================================

    dim_store = dim_store[
        [
            "store_key",
            "store_id",
            "store_name",
            "store_type",
            "city",
            "state",
            "country",
            "opening_date",
            "store_status",
            "effective_start_date",
            "effective_end_date",
            "is_current",
            "created_date",
            "updated_date",
        ]
    ]

    logger.info(
        "Store Dimension : %s rows",
        f"{len(dim_store):,}",
    )

    return dim_store