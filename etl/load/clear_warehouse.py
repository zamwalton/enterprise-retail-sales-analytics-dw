"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : clear_warehouse.py
Purpose : Clear warehouse tables before full-refresh load
============================================================
"""

from psycopg2 import sql

from database.connection import get_connection
from etl.utils import logger


WAREHOUSE_TABLES = [
    "fact_sales",
    "dim_date",
    "dim_promotion",
    "dim_product",
    "dim_store",
    "dim_supplier",
    "dim_employee",
    "dim_customer",
]


def clear_warehouse(
    schema: str = "retail_dw",
):
    """
    Clear all warehouse tables before a full-refresh ETL load.

    Tables are truncated and surrogate-key sequences are reset.
    CASCADE is used because fact tables depend on dimensions.
    """

    logger.info(
        "Clearing existing warehouse data..."
    )

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        tables = sql.SQL(", ").join(
            sql.Identifier(schema, table)
            for table in WAREHOUSE_TABLES
        )

        query = sql.SQL(
            """
            TRUNCATE TABLE {}
            RESTART IDENTITY
            CASCADE
            """
        ).format(tables)

        cursor.execute(query)

        conn.commit()

        logger.info(
            "Warehouse data cleared successfully."
        )

    except Exception as e:

        if conn:
            conn.rollback()

        logger.error(
            "Failed to clear warehouse: %s",
            e,
        )

        raise

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

        logger.info(
            "Warehouse cleanup database resources closed."
        )