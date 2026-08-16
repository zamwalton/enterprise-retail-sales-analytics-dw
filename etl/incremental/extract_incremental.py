"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : extract_incremental.py
Purpose : Incremental Source Data Extraction
============================================================
"""

import pandas as pd

from etl.utils import logger
from etl.extract.extract import extract_data
from etl.incremental.watermark import get_watermark


# ============================================================
# INCREMENTAL SALES EXTRACTION
# ============================================================

def extract_incremental_sales() -> pd.DataFrame:
    """
    Extract sales_header records newer than the current
    high-watermark.

    Returns
    -------
    pandas.DataFrame
        New sales_header records that have not yet been
        processed.
    """

    logger.info(
        "========== INCREMENTAL EXTRACTION STARTED =========="
    )

    last_watermark_date, last_watermark_id = get_watermark()

    logger.info(
        "Current watermark | Date: %s | ID: %s",
        last_watermark_date,
        last_watermark_id,
    )

    data = extract_data()

    sales_header = data["sales_header"].copy()

    # ========================================================
    # FIRST INCREMENTAL RUN
    # ========================================================

    if last_watermark_date is None:
        logger.info(
            "No previous watermark found. "
            "Initial incremental extraction selected."
        )

        return sales_header

    # ========================================================
    # SUBSEQUENT INCREMENTAL RUN
    # ========================================================

    sales_header["transaction_date"] = pd.to_datetime(
        sales_header["transaction_date"]
    )

    incremental_sales = sales_header[
        (
            sales_header["transaction_date"]
            > last_watermark_date
        )
        |
        (
            (
                sales_header["transaction_date"]
                == last_watermark_date
            )
            &
            (
                sales_header["transaction_id"]
                > last_watermark_id
            )
        )
    ].copy()

    logger.info(
        "Incremental sales records extracted: %s",
        len(incremental_sales),
    )

    logger.info(
        "========== INCREMENTAL EXTRACTION COMPLETED =========="
    )

    return incremental_sales

# ============================================================
# INCREMENTAL SALES DETAIL EXTRACTION
# ============================================================

def extract_incremental_details(
    incremental_sales: pd.DataFrame,
) -> pd.DataFrame:
    """
    Extract sales_detail records belonging to the
    incrementally extracted sales transactions.

    Parameters
    ----------
    incremental_sales : pandas.DataFrame
        Incremental records from sales_header.

    Returns
    -------
    pandas.DataFrame
        Sales detail records associated with the
        incremental transactions.
    """

    logger.info(
        "========== INCREMENTAL DETAIL EXTRACTION STARTED =========="
    )

    # --------------------------------------------------------
    # No new sales transactions
    # --------------------------------------------------------

    if incremental_sales.empty:

        logger.info(
            "No incremental sales transactions found."
        )

        return pd.DataFrame()

    # --------------------------------------------------------
    # Extract source datasets
    # --------------------------------------------------------

    data = extract_data()

    sales_detail = data["sales_detail"].copy()

    # --------------------------------------------------------
    # Identify incremental transaction IDs
    # --------------------------------------------------------

    transaction_ids = incremental_sales[
        "transaction_id"
    ].unique()

    # --------------------------------------------------------
    # Filter sales detail
    # --------------------------------------------------------

    incremental_details = sales_detail[
        sales_detail["transaction_id"].isin(
            transaction_ids
        )
    ].copy()

    logger.info(
        "Incremental sales detail records extracted: %s",
        len(incremental_details),
    )

    logger.info(
        "========== INCREMENTAL DETAIL EXTRACTION COMPLETED =========="
    )

    return incremental_details