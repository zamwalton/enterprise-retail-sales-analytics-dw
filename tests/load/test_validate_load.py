
"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : test_validate_load.py
Purpose : Test PostgreSQL Load Validation
============================================================
"""

from database.connection import get_connection

from etl.load.validate_load import validate_row_count


def setup_test_data():
    """
    Insert controlled test data into dim_customer.
    """

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        # Remove any previous test data.
        cursor.execute(
            """
            DELETE FROM retail_dw.dim_customer
            WHERE customer_id IN (
                'TEST001',
                'TEST002',
                'TEST003'
            )
            """
        )

        # Insert controlled test records.
        cursor.execute(
            """
            INSERT INTO retail_dw.dim_customer
            (
                customer_id,
                customer_name,
                gender,
                date_of_birth,
                email,
                phone,
                city,
                state,
                country,
                loyalty_tier,
                effective_start_date,
                effective_end_date,
                is_current
            )
            VALUES
            (
                'TEST001',
                'Test Customer 1',
                'Male',
                '1995-01-01',
                'test1@example.com',
                '9999999999',
                'Kochi',
                'Kerala',
                'India',
                'Silver',
                CURRENT_DATE,
                '9999-12-31',
                TRUE
            ),
            (
                'TEST002',
                'Test Customer 2',
                'Female',
                '1996-02-02',
                'test2@example.com',
                '9999999998',
                'Thrissur',
                'Kerala',
                'India',
                'Gold',
                CURRENT_DATE,
                '9999-12-31',
                TRUE
            ),
            (
                'TEST003',
                'Test Customer 3',
                'Male',
                '1997-03-03',
                'test3@example.com',
                '9999999997',
                'Kozhikode',
                'Kerala',
                'India',
                'Bronze',
                CURRENT_DATE,
                '9999-12-31',
                TRUE
            )
            """
        )

        conn.commit()

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


def cleanup_test_data():
    """
    Remove only the records created by this test.
    """

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM retail_dw.dim_customer
            WHERE customer_id IN (
                'TEST001',
                'TEST002',
                'TEST003'
            )
            """
        )

        conn.commit()

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


def test_validate_dim_customer():

    setup_test_data()

    try:

        validate_row_count(
            table_name="dim_customer",
            expected_count=3,
        )

    finally:

        cleanup_test_data()
