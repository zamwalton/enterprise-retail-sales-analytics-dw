"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : postgres_loader.py
Purpose : Generic PostgreSQL DataFrame Loader
============================================================
"""

import io
import re

from psycopg2 import sql

from database.connection import get_connection
from etl.utils import logger


# ==========================================================
# Identifier Validation
# ==========================================================

def validate_identifier(value):
    """
    Validate PostgreSQL schema/table identifiers.

    Prevents unsafe identifiers from being inserted
    directly into SQL statements.
    """

    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value):
        raise ValueError(
            f"Invalid PostgreSQL identifier: {value}"
        )

    return value


# ==========================================================
# DataFrame Loader
# ==========================================================

def load_dataframe(
    df,
    table_name,
    schema="retail_dw"
):
    """
    Load a pandas DataFrame into PostgreSQL.

    Uses PostgreSQL COPY for efficient bulk loading.
    """

    validate_identifier(schema)
    validate_identifier(table_name)

    if df.empty:
        logger.warning(
            f"{schema}.{table_name} contains 0 rows. "
            "Skipping load."
        )
        return

    logger.info(
        f"Loading Dimension: {table_name} "
        f"({len(df):,} rows)..."
    )

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        # --------------------------------------------------
        # Convert DataFrame to CSV in memory
        # --------------------------------------------------

        buffer = io.StringIO()

        df.to_csv(
            buffer,
            index=False,
            header=False,
            na_rep="\\N",
        )

        buffer.seek(0)

        # --------------------------------------------------
        # Build safe SQL statement
        # --------------------------------------------------

        copy_sql = sql.SQL(
            """
            COPY {}.{}
            ({})
            FROM STDIN
            WITH (
                FORMAT CSV,
                NULL '\\N'
            )
            """
        ).format(
            sql.Identifier(schema),
            sql.Identifier(table_name),
            sql.SQL(", ").join(
                sql.Identifier(column)
                for column in df.columns
            ),
        )

        # --------------------------------------------------
        # Bulk load
        # --------------------------------------------------

        cursor.copy_expert(
            copy_sql.as_string(conn),
            buffer,
        )

        conn.commit()

        logger.info(
            f"{table_name} loaded successfully. "
            f"Rows: {len(df):,}"
        )

    except Exception as e:

        if conn:
            conn.rollback()

        logger.error(
            f"Failed to load "
            f"{schema}.{table_name}: {e}"
        )

        raise

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

        