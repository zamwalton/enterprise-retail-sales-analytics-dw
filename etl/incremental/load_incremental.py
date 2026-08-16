"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : load_incremental.py
Purpose : Incremental Fact Sales Loader
============================================================
"""

import pandas as pd
from psycopg2 import sql

from database.connection import get_connection
from etl.utils import logger


def load_incremental_fact_sales(
    fact_df: pd.DataFrame,
) -> int:
    """
    Load new Fact Sales records into PostgreSQL.

    Existing records are identified using:
        transaction_id + line_number

    Returns
    -------
    int
        Number of rows successfully inserted.
    """

    logger.info(
        "========== INCREMENTAL FACT LOAD STARTED =========="
    )

    if fact_df.empty:
        logger.info(
            "No incremental fact records to load."
        )
        return 0

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        # ==================================================
        # 1. GET CURRENT MAX SALES KEY
        # ==================================================

        cursor.execute(
            """
            SELECT COALESCE(MAX(sales_key), 0)
            FROM retail_dw.fact_sales
            """
        )

        max_sales_key = cursor.fetchone()[0]

        logger.info(
            "Current maximum sales_key: %s",
            max_sales_key,
        )

        # ==================================================
        # 2. CHECK EXISTING BUSINESS KEYS
        # ==================================================

        existing_keys = set()

        cursor.execute(
            """
            SELECT transaction_id, line_number
            FROM retail_dw.fact_sales
            """
        )

        for transaction_id, line_number in cursor.fetchall():
            existing_keys.add(
                (transaction_id, line_number)
            )

        # ==================================================
        # 3. REMOVE ALREADY LOADED RECORDS
        # ==================================================

        fact_df = fact_df.copy()

        fact_df["_business_key"] = list(
            zip(
                fact_df["transaction_id"],
                fact_df["line_number"],
            )
        )

        fact_df = fact_df[
            ~fact_df["_business_key"].isin(existing_keys)
        ].copy()

        fact_df.drop(
            columns=["_business_key"],
            inplace=True,
        )

        logger.info(
            "New incremental fact records: %s",
            f"{len(fact_df):,}",
        )

        if fact_df.empty:
            logger.info(
                "All incremental records already exist."
            )
            conn.rollback()
            return 0

        # ==================================================
        # 4. ASSIGN NEW SURROGATE KEYS
        # ==================================================

        fact_df["sales_key"] = range(
            max_sales_key + 1,
            max_sales_key + 1 + len(fact_df),
        )

        fact_df = fact_df[
                [
                    "sales_key",
                    "transaction_id",
                    "line_number",
                    "date_key",
                    "customer_key",
                    "employee_key",
                    "store_key",
                    "product_key",
                    "promotion_key",
                    "quantity",
                    "unit_price",
                    "discount_amount",
                    "tax_amount",
                    "total_amount",
                    "payment_method",
                    "transaction_status",
                    "created_date",
                    "updated_date",
                    "is_active",
                ]
            ]

        # ==================================================
        # 5. PREPARE COPY BUFFER
        # ==================================================

        import io

        buffer = io.StringIO()

        fact_df.to_csv(
            buffer,
            index=False,
            header=False,
            na_rep="\\N",
        )

        buffer.seek(0)

        columns = [
            sql.Identifier(column)
            for column in fact_df.columns
        ]

        copy_sql = sql.SQL(
            """
            COPY retail_dw.fact_sales
            ({})
            FROM STDIN
            WITH (
                FORMAT CSV,
                NULL '\\N'
            )
            """
        ).format(
            sql.SQL(", ").join(columns)
        )

        # ==================================================
        # 6. LOAD INTO FACT TABLE
        # ==================================================

        cursor.copy_expert(
            copy_sql.as_string(conn),
            buffer,
        )

        conn.commit()

        inserted_rows = len(fact_df)

        logger.info(
            "Incremental Fact Sales loaded successfully. "
            "Rows inserted: %s",
            f"{inserted_rows:,}",
        )

        logger.info(
            "========== INCREMENTAL FACT LOAD COMPLETED =========="
        )

        return inserted_rows

    except Exception as error:

        if conn:
            conn.rollback()

        logger.error(
            "Incremental Fact Sales load failed: %s",
            error,
        )

        raise

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()