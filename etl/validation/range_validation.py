"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : range_validation.py
Purpose : Range and Domain Validation
============================================================
"""

import pandas as pd


def validate_numeric_range(
    df: pd.DataFrame,
    column: str,
    minimum: float | None = None,
    maximum: float | None = None,
) -> None:
    """
    Validate that numeric values fall within an allowed range.

    Raises:
        ValueError: If the column is missing or values fall
                    outside the specified range.
    """

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' does not exist."
        )

    values = pd.to_numeric(
        df[column],
        errors="coerce",
    )

    invalid_mask = pd.Series(False, index=df.index)

    if minimum is not None:
        invalid_mask |= values < minimum

    if maximum is not None:
        invalid_mask |= values > maximum

    invalid_count = invalid_mask.sum()

    if invalid_count > 0:
        raise ValueError(
            f"Range validation failed for '{column}'. "
            f"Found {invalid_count} invalid value(s)."
        )