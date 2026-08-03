"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : utils.py
Purpose : Common ETL Utility Functions
============================================================
"""

import logging

import pandas as pd


# ==========================================================
# Logger Configuration
# ==========================================================

logger = logging.getLogger("retail_etl")

logger.setLevel(logging.INFO)

# Prevent log messages from being passed to the root logger.
# This avoids duplicate log output when another module
# configures the root logger.
logger.propagate = False

if not logger.handlers:

    handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s"
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)


# ==========================================================
# Surrogate Key
# ==========================================================

def add_surrogate_key(
    df: pd.DataFrame,
    key_name: str,
) -> pd.DataFrame:
    """
    Add a sequential surrogate key column.
    """

    df = df.copy()

    df.insert(
        0,
        key_name,
        range(1, len(df) + 1),
    )

    return df


# ==========================================================
# Audit Columns
# ==========================================================

def add_audit_columns(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add standard ETL audit columns.
    """

    df = df.copy()

    df["created_date"] = pd.Timestamp.now()
    df["updated_date"] = pd.NaT
    df["is_active"] = True

    return df

