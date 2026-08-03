"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : completeness.py
Purpose : Data completeness validation utilities
============================================================
"""

from typing import Iterable

import pandas as pd

from etl.utils import logger


def validate_not_null(
    df: pd.DataFrame,
    required_columns: Iterable[str],
) -> bool:
    """
    Validate that required columns do not contain NULL values.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to validate.

    required_columns : Iterable[str]
        Columns that must not contain NULL values.

    Returns
    -------
    bool
        True when validation passes.

    Raises
    ------
    ValueError
        If required columns are missing or contain NULL values.
    """

    required_columns = list(required_columns)

    # =========================================================
    # Validate Column Existence
    # =========================================================

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            "Completeness validation failed. "
            f"Missing required columns: {missing_columns}"
        )

    # =========================================================
    # Check NULL Values
    # =========================================================

    null_counts = df[required_columns].isnull().sum()

    invalid_columns = (
        null_counts[null_counts > 0]
        .to_dict()
    )

    if invalid_columns:

        raise ValueError(
            "Completeness validation failed. "
            f"NULL values found: {invalid_columns}"
        )

    # =========================================================
    # Validation Passed
    # =========================================================

    logger.info(
        "Completeness validation passed for %s rows.",
        f"{len(df):,}",
    )

    return True