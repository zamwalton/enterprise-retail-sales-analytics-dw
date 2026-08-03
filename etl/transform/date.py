"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : date.py
Purpose : Generate Date Dimension
============================================================
"""

import pandas as pd

from etl.utils import logger


def transform_date(
    start_date: str = "2023-01-01",
    end_date: str = "2028-12-31",
) -> pd.DataFrame:
    """
    Generate the Date Dimension.
    """

    logger.info("Generating Date Dimension...")

    # ==========================================================
    # Generate Calendar Dates
    # ==========================================================

    dates = pd.date_range(
        start=start_date,
        end=end_date,
        freq="D",
    )

    dim_date = pd.DataFrame()

    dim_date["full_date"] = dates

    # ==========================================================
    # Date Key
    # ==========================================================

    dim_date["date_key"] = (
        dim_date["full_date"]
        .dt.strftime("%Y%m%d")
        .astype(int)
    )

    # ==========================================================
    # Calendar Attributes
    # ==========================================================

    dim_date["day"] = (
        dim_date["full_date"].dt.day
    )

    dim_date["day_name"] = (
        dim_date["full_date"].dt.day_name()
    )

    dim_date["week_of_year"] = (
        dim_date["full_date"]
        .dt.isocalendar()
        .week
        .astype(int)
    )

    dim_date["month"] = (
        dim_date["full_date"].dt.month
    )

    dim_date["month_name"] = (
        dim_date["full_date"].dt.month_name()
    )

    dim_date["quarter"] = (
        dim_date["full_date"].dt.quarter
    )

    dim_date["year"] = (
        dim_date["full_date"].dt.year
    )

    # ==========================================================
    # Business Calendar Flags
    # ==========================================================

    dim_date["is_weekend"] = (
        dim_date["full_date"].dt.weekday >= 5
    )

    dim_date["is_month_end"] = (
        dim_date["full_date"].dt.is_month_end
    )

    dim_date["is_quarter_end"] = (
        dim_date["full_date"].dt.is_quarter_end
    )

    dim_date["is_year_end"] = (
        dim_date["full_date"].dt.is_year_end
    )

    # ==========================================================
    # Final Column Order
    # ==========================================================

    columns = [
        "date_key",
        "full_date",
        "day",
        "day_name",
        "week_of_year",
        "month",
        "month_name",
        "quarter",
        "year",
        "is_weekend",
        "is_month_end",
        "is_quarter_end",
        "is_year_end",
    ]

    dim_date = dim_date[columns]

    # ==========================================================
    # Data Quality Validation
    # ==========================================================

    if dim_date["date_key"].duplicated().any():
        raise ValueError(
            "Date Dimension validation failed: "
            "duplicate date_key values found."
        )

    if dim_date["full_date"].duplicated().any():
        raise ValueError(
            "Date Dimension validation failed: "
            "duplicate full_date values found."
        )

    if dim_date["date_key"].isna().any():
        raise ValueError(
            "Date Dimension validation failed: "
            "NULL date_key values found."
        )

    if dim_date["full_date"].isna().any():
        raise ValueError(
            "Date Dimension validation failed: "
            "NULL full_date values found."
        )

    # ==========================================================
    # Logging
    # ==========================================================

    logger.info(
        "Date Dimension : %s rows",
        f"{len(dim_date):,}",
    )

    return dim_date