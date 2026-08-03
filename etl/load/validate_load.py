"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : validate_load.py
Purpose : Validate PostgreSQL warehouse loads
============================================================
"""

from psycopg2 import sql

from database.connection import get_connection
from etl.utils import logger


def get_table_row_count(
    table_name: str,
    schema: str = "retail_dw",
) -> int:
    """
    Return the number of rows currently loaded
    into a PostgreSQL table.
    """

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        query = sql.SQL(
            "SELECT COUNT(*) FROM {}.{}"
        ).format(
            sql.Identifier(schema),
            sql.Identifier(table_name),
        )

        cursor.execute(query)

        count = cursor.fetchone()[0]

        logger.info(
            "%s.%s row count : %s",
            schema,
            table_name,
            f"{count:,}",
        )

        return count

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


def validate_row_count(
    table_name: str,
    expected_count: int,
    schema: str = "retail_dw",
):
    """
    Validate that PostgreSQL contains the expected
    number of rows.
    """

    actual_count = get_table_row_count(
        table_name,
        schema,
    )

    if actual_count != expected_count:

        raise ValueError(
            f"Row count validation failed for "
            f"{schema}.{table_name}. "
            f"Expected {expected_count:,}, "
            f"found {actual_count:,}."
        )

    logger.info(
        "Row count validation passed for "
        "%s.%s : %s rows",
        schema,
        table_name,
        f"{actual_count:,}",
    )