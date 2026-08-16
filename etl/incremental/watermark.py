"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : watermark.py
Purpose : High-Watermark Management for Incremental ETL
============================================================
"""

from datetime import datetime
from typing import Optional

from database.connection import get_connection
from etl.utils import logger


# ============================================================
# PIPELINE CONFIGURATION
# ============================================================

PIPELINE_NAME = "Enterprise Retail Sales Analytics DW"
SOURCE_SYSTEM = "POS_SALES"
WATERMARK_COLUMN = "transaction_date"


# ============================================================
# INITIALIZE WATERMARK
# ============================================================

def initialize_watermark() -> None:
    """
    Create the initial ETL control record if it does not exist.

    The initial watermark is NULL because no incremental
    records have been processed yet.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO retail_dw.etl_control
            (
                pipeline_name,
                source_system,
                watermark_column,
                last_watermark_date,
                last_watermark_id
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s
            )
            ON CONFLICT (
                pipeline_name,
                source_system
            )
            DO NOTHING
            """,
            (
                PIPELINE_NAME,
                SOURCE_SYSTEM,
                WATERMARK_COLUMN,
                None,
                None,
            ),
        )

        connection.commit()

        logger.info(
            "ETL watermark initialized for source system: %s",
            SOURCE_SYSTEM,
        )

    finally:
        cursor.close()
        connection.close()


# ============================================================
# GET CURRENT WATERMARK
# ============================================================

def get_watermark() -> tuple[
    Optional[datetime],
    Optional[str],
]:
    """
    Retrieve the current high-watermark for the source system.

    Returns
    -------
    tuple[Optional[datetime], Optional[str]]
        Last processed transaction date and transaction ID.

        Returns (None, None) when no incremental load
        has been completed yet.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT
                last_watermark_date,
                last_watermark_id
            FROM retail_dw.etl_control
            WHERE pipeline_name = %s
              AND source_system = %s
            """,
            (
                PIPELINE_NAME,
                SOURCE_SYSTEM,
            ),
        )

        result = cursor.fetchone()

        if result is None:
            raise ValueError(
                "ETL control record not found for "
                f"{SOURCE_SYSTEM}."
            )

        return result[0], result[1]

    finally:
        cursor.close()
        connection.close()

#============================================================
# GET LATEST WATERMARK
#============================================================


def get_latest_watermark(
    sales_header,
) -> tuple[datetime, str]:
    """
    Determine the latest successfully processed
    transaction date and transaction ID.
    """

    if sales_header.empty:
        raise ValueError(
            "Cannot determine watermark from empty sales data."
        )

    ordered = sales_header.sort_values(
        by=[
            "transaction_date",
            "transaction_id",
        ]
    )

    latest = ordered.iloc[-1]

    return (
        latest["transaction_date"],
        latest["transaction_id"],
    )


# ============================================================
# UPDATE WATERMARK
# ============================================================

def update_watermark(
    watermark_date: datetime,
    watermark_id: str,
) -> None:
    """
    Update the high-watermark after a successful ETL load.

    Parameters
    ----------
    watermark_date : datetime
        Latest successfully processed transaction date.

    watermark_id : str
        Latest successfully processed transaction ID.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE retail_dw.etl_control
            SET
                last_watermark_date = %s,
                last_watermark_id = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE pipeline_name = %s
              AND source_system = %s
            """,
            (
                watermark_date,
                watermark_id,
                PIPELINE_NAME,
                SOURCE_SYSTEM,
            ),
        )

        if cursor.rowcount == 0:
            raise ValueError(
                "ETL control record not found for "
                f"{SOURCE_SYSTEM}."
            )

        connection.commit()

        logger.info(
            "ETL watermark updated successfully. "
            "Date: %s | ID: %s",
            watermark_date,
            watermark_id,
        )

    finally:
        cursor.close()
        connection.close()