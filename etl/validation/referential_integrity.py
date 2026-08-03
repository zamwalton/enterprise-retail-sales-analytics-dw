"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : referential_integrity.py
Purpose : Referential Integrity Validation
============================================================
"""

import pandas as pd


def validate_referential_integrity(
    fact_df: pd.DataFrame,
    fact_column: str,
    dimension_df: pd.DataFrame,
    dimension_column: str,
) -> None:
    """
    Validate that every foreign-key value in the fact DataFrame
    exists in the corresponding dimension DataFrame.

    Raises:
        ValueError: If columns are missing or orphan keys exist.
    """

    # ---------------------------------------------------------
    # Validate required columns
    # ---------------------------------------------------------

    if fact_column not in fact_df.columns:
        raise ValueError(
            f"Fact column '{fact_column}' does not exist."
        )

    if dimension_column not in dimension_df.columns:
        raise ValueError(
            f"Dimension column '{dimension_column}' does not exist."
        )

    # ---------------------------------------------------------
    # Get dimension key values
    # ---------------------------------------------------------

    dimension_keys = set(
        dimension_df[dimension_column].dropna()
    )

    # ---------------------------------------------------------
    # Find orphan foreign keys
    # ---------------------------------------------------------

    fact_keys = fact_df[fact_column].dropna()

    orphan_keys = set(fact_keys) - dimension_keys

    # ---------------------------------------------------------
    # Raise validation error if orphan keys exist
    # ---------------------------------------------------------

    if orphan_keys:
        raise ValueError(
            f"Referential integrity validation failed for "
            f"'{fact_column}'. "
            f"Found {len(orphan_keys)} orphan key(s)."
        )