"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : test_postgres_loader.py
Purpose : Test PostgreSQL DataFrame Loader
============================================================
"""

import pandas as pd

from database.connection import get_connection
from etl.load.postgres_loader import load_dataframe


def clear_test_table():
    """
    Clear the PostgreSQL test table before running
    the loader test so the test remains repeatable.
    """

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "TRUNCATE TABLE retail_dw.fact_sales_test"
        )

        conn.commit()

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


def test_postgres_loader():

    # ======================================================
    # Clear previous test data
    # ======================================================

    clear_test_table()

    # ======================================================
    # Test Data
    # ======================================================

    df = pd.DataFrame(
        {
            "sales_key": [1, 2, 3],

            "transaction_id": [
                "TEST001",
                "TEST002",
                "TEST003",
            ],

            "line_number": [1, 1, 1],

            "date_key": [
                20260101,
                20260102,
                20260103,
            ],

            "customer_key": [1, 2, 3],

            "employee_key": [1, 2, 3],

            "store_key": [1, 2, 3],

            "product_key": [1, 2, 3],

            "promotion_key": [0, 0, 0],

            "quantity": [1, 2, 3],

            "unit_price": [
                100.00,
                200.00,
                300.00,
            ],

            "discount_amount": [
                0.00,
                10.00,
                20.00,
            ],

            "tax_amount": [
                18.00,
                36.00,
                54.00,
            ],

            "total_amount": [
                118.00,
                426.00,
                954.00,
            ],

            "payment_method": [
                "Cash",
                "UPI",
                "Card",
            ],

            "transaction_status": [
                "Completed",
                "Completed",
                "Completed",
            ],

            "created_date": pd.Timestamp(
                "2026-07-27"
            ),

            "updated_date": pd.NaT,

            "is_active": [
                True,
                True,
                True,
            ],
        }
    )

    # ======================================================
    # Execute Loader
    # ======================================================

    load_dataframe(
        df,
        "fact_sales_test",
        "retail_dw",
    )

    # ======================================================
    # Validate Load
    # ======================================================

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM retail_dw.fact_sales_test
            """
        )

        row_count = cursor.fetchone()[0]

        assert row_count == 3

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

    # ======================================================
    # Cleanup
    # ======================================================

    clear_test_table()

