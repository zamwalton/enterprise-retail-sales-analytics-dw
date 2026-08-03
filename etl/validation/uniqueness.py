"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : uniqueness.py
Purpose : Data uniqueness validation utilities
============================================================
"""

from typing import Iterable

import pandas as pd

from etl.utils import logger


def validate_unique(
    df: pd.DataFrame,
    columns: Iterable[str],
) -> bool:
    """
    Validate that the specified column or combination
    of columns contains unique values.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to validate.

    columns : Iterable[str]
        Column or columns that together must be unique.

    Returns
    -------
    bool
        True when validation passes.

    Raises
    ------
    ValueError
        If required columns are missing or duplicate
        records are found.
    """

    columns = list(columns)

    # =========================================================
    # Validate Column List
    # =========================================================

    if not columns:

        raise ValueError(
            "Uniqueness validation failed. "
            "At least one column must be provided."
        )

    # =========================================================
    # Validate Column Existence
    # =========================================================

    missing_columns = [
        column
        for column in columns
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            "Uniqueness validation failed. "
            f"Missing required columns: {missing_columns}"
        )

    # =========================================================
    # Find Duplicate Records
    # =========================================================

    duplicate_mask = df.duplicated(
        subset=columns,
        keep=False,
    )

    duplicate_count = int(
        duplicate_mask.sum()
    )

    if duplicate_count > 0:

        duplicate_records = (
            df.loc[
                duplicate_mask,
                columns
            ]
            .drop_duplicates()
            .to_dict("records")
        )

        raise ValueError(
            "Uniqueness validation failed. "
            f"Found {duplicate_count:,} duplicate rows "
            f"for columns {columns}. "
            f"Duplicate keys: {duplicate_records}"
        )

    # =========================================================
    # Validation Passed
    # =========================================================

    logger.info(
        "Uniqueness validation passed for columns %s.",
        columns,
    )

    return True