"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : test_product_scd2.py
Purpose : Unit tests for Product Dimension SCD Type 2
============================================================
"""

from datetime import date
from decimal import Decimal
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from etl.scd.product_scd2 import (
    _normalize_value,
    process_product_scd2,
)


# ============================================================
# TEST DATA
# ============================================================

EFFECTIVE_DATE = date(2026, 1, 1)


def create_product(**overrides):
    """
    Create a standard Product source record for testing.
    """

    product = {
        "product_id": "P001",
        "product_name": "Laptop Pro 15",
        "brand": "TechBrand",
        "category": "Electronics",
        "subcategory": "Laptops",
        "supplier_id": "SUP001",
        "standard_cost": 500.00,
        "selling_price": 799.99,
        "product_status": "ACTIVE",
    }

    product.update(overrides)

    return product


def create_product_dataframe(**overrides):
    """
    Create a Product DataFrame for testing.
    """

    return pd.DataFrame(
        [create_product(**overrides)]
    )


def create_current_row(**overrides):
    """
    Create a warehouse current-version row matching the
    SELECT column order used by process_product_scd2().
    """

    current = {
        "product_key": 101,
        "product_id": "P001",
        "product_name": "Laptop Pro 15",
        "brand": "TechBrand",
        "category": "Electronics",
        "subcategory": "Laptops",
        "supplier_id": "SUP001",
        "standard_cost": Decimal("500.00"),
        "selling_price": Decimal("799.99"),
        "product_status": "ACTIVE",
        "effective_start_date": date(2025, 1, 1),
        "effective_end_date": date(9999, 12, 31),
        "is_current": True,
    }

    current.update(overrides)

    return tuple(current.values())


# ============================================================
# NORMALIZATION TESTS
# ============================================================


def test_normalize_value_returns_none_for_nan():
    """
    NaN values should be normalized to None.
    """

    assert _normalize_value(float("nan")) is None


def test_normalize_value_returns_none_for_none():
    """
    None values should remain None.
    """

    assert _normalize_value(None) is None


def test_normalize_value_rounds_float_to_two_decimals():
    """
    Float values should be rounded to two decimal places.
    """

    assert _normalize_value(799.999) == 800.00


def test_normalize_value_rounds_integer_to_float():
    """
    Integer values should be converted to float and rounded.
    """

    result = _normalize_value(500)

    assert result == 500.00
    assert isinstance(result, float)


def test_normalize_value_rounds_decimal_to_two_decimals():
    """
    Decimal values should be converted to float and rounded.
    """

    result = _normalize_value(
        Decimal("799.999")
    )

    assert result == 800.00
    assert isinstance(result, float)


def test_normalize_value_converts_timestamp_to_date():
    """
    pandas Timestamp values should be converted to date.
    """

    timestamp = pd.Timestamp("2026-01-15 10:30:00")

    result = _normalize_value(timestamp)

    assert result == date(2026, 1, 15)
    assert isinstance(result, date)


def test_normalize_value_preserves_string():
    """
    String values should remain unchanged.
    """

    assert _normalize_value("Electronics") == "Electronics"


# ============================================================
# EMPTY SOURCE TEST
# ============================================================


@patch("etl.scd.product_scd2.get_connection")
def test_empty_products_returns_zero_counts_without_connection(
    mock_get_connection,
):
    """
    Empty Product source data should skip processing and
    should not establish a database connection.
    """

    products = pd.DataFrame(
        columns=[
            "product_id",
            "product_name",
            "brand",
            "category",
            "subcategory",
            "supplier_id",
            "standard_cost",
            "selling_price",
            "product_status",
        ]
    )

    result = process_product_scd2(
        products,
        effective_date=EFFECTIVE_DATE,
    )

    assert result == (0, 0)

    mock_get_connection.assert_not_called()


# ============================================================
# NEW PRODUCT TEST
# ============================================================


@patch("etl.scd.product_scd2.get_connection")
def test_new_product_inserts_new_version(mock_get_connection):
    """
    A Product that does not currently exist in the warehouse
    should result in one inserted SCD2 version.
    """

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # No current warehouse version exists.
    mock_cursor.fetchone.return_value = None

    products = create_product_dataframe()

    inserted, closed = process_product_scd2(
        products,
        effective_date=EFFECTIVE_DATE,
    )

    assert inserted == 1
    assert closed == 0

    # SELECT + INSERT
    assert mock_cursor.execute.call_count == 2

    insert_call = mock_cursor.execute.call_args_list[1]

    assert "INSERT INTO retail_dw.dim_product" in insert_call.args[0]

    insert_values = insert_call.args[1]

    assert insert_values[0] == "P001"
    assert insert_values[1] == "Laptop Pro 15"
    assert insert_values[2] == "TechBrand"
    assert insert_values[3] == "Electronics"
    assert insert_values[4] == "Laptops"
    assert insert_values[5] == "SUP001"
    assert insert_values[6] == 500.00
    assert insert_values[7] == 799.99
    assert insert_values[8] == "ACTIVE"
    assert insert_values[9] == EFFECTIVE_DATE
    assert insert_values[10] == date(9999, 12, 31)

    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


# ============================================================
# EXISTING PRODUCT - NO CHANGE
# ============================================================


@patch("etl.scd.product_scd2.get_connection")
def test_existing_product_with_no_change_does_not_create_new_version(
    mock_get_connection,
):
    """
    An existing Product with no changed comparison attributes
    should not close or insert a new version.
    """

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = create_current_row()

    products = create_product_dataframe()

    inserted, closed = process_product_scd2(
        products,
        effective_date=EFFECTIVE_DATE,
    )

    assert inserted == 0
    assert closed == 0

    # Only the SELECT should execute.
    assert mock_cursor.execute.call_count == 1

    executed_sql = mock_cursor.execute.call_args.args[0]

    assert "SELECT" in executed_sql
    assert "is_current = TRUE" in executed_sql

    mock_conn.commit.assert_called_once()

    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


# ============================================================
# EXISTING PRODUCT - ATTRIBUTE CHANGE
# ============================================================


@patch("etl.scd.product_scd2.get_connection")
def test_changed_product_closes_old_version_and_inserts_new_version(
    mock_get_connection,
):
    """
    When a Product comparison attribute changes, the current
    version should be closed and a new version inserted.
    """

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = create_current_row()

    products = create_product_dataframe(
        selling_price=849.99
    )

    inserted, closed = process_product_scd2(
        products,
        effective_date=EFFECTIVE_DATE,
    )

    assert inserted == 1
    assert closed == 1

    # SELECT + UPDATE + INSERT
    assert mock_cursor.execute.call_count == 3

    select_call = mock_cursor.execute.call_args_list[0]
    update_call = mock_cursor.execute.call_args_list[1]
    insert_call = mock_cursor.execute.call_args_list[2]

    # --------------------------------------------------------
    # SELECT
    # --------------------------------------------------------

    assert "SELECT" in select_call.args[0]
    assert "FROM retail_dw.dim_product" in select_call.args[0]
    assert "product_id = %s" in select_call.args[0]
    assert "is_current = TRUE" in select_call.args[0]

    assert select_call.args[1] == ("P001",)

    # --------------------------------------------------------
    # UPDATE
    # --------------------------------------------------------

    assert "UPDATE retail_dw.dim_product" in update_call.args[0]
    assert "effective_end_date = %s" in update_call.args[0]
    assert "is_current = FALSE" in update_call.args[0]

    assert update_call.args[1] == (
        EFFECTIVE_DATE,
        101,
    )

    # --------------------------------------------------------
    # INSERT
    # --------------------------------------------------------

    assert "INSERT INTO retail_dw.dim_product" in insert_call.args[0]

    insert_values = insert_call.args[1]

    assert insert_values[0] == "P001"
    assert insert_values[1] == "Laptop Pro 15"
    assert insert_values[7] == 849.99
    assert insert_values[8] == "ACTIVE"
    assert insert_values[9] == EFFECTIVE_DATE
    assert insert_values[10] == date(9999, 12, 31)

    mock_conn.commit.assert_called_once()

    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


# ============================================================
# EACH SCD2 ATTRIBUTE CHANGE
# ============================================================


@pytest.mark.parametrize(
    "changed_column,new_value",
    [
        ("product_name", "Laptop Pro 16"),
        ("brand", "NewBrand"),
        ("category", "Computers"),
        ("subcategory", "Gaming Laptops"),
        ("supplier_id", "SUP002"),
        ("standard_cost", 550.00),
        ("selling_price", 899.99),
        ("product_status", "INACTIVE"),
    ],
)
@patch("etl.scd.product_scd2.get_connection")
def test_each_compare_column_change_creates_new_version(
    mock_get_connection,
    changed_column,
    new_value,
):
    """
    Every column listed in COMPARE_COLUMNS should trigger
    SCD Type 2 processing when its value changes.
    """

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = create_current_row()

    products = create_product_dataframe(
        **{changed_column: new_value}
    )

    inserted, closed = process_product_scd2(
        products,
        effective_date=EFFECTIVE_DATE,
    )

    assert inserted == 1
    assert closed == 1

    # SELECT + UPDATE + INSERT
    assert mock_cursor.execute.call_count == 3

    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


# ============================================================
# MULTIPLE PRODUCTS
# ============================================================


@patch("etl.scd.product_scd2.get_connection")
def test_multiple_products_process_correctly(
    mock_get_connection,
):
    """
    Multiple source Products should be processed independently.
    """

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Product 1 -> new
    # Product 2 -> existing and unchanged
    # Product 3 -> existing and changed
    mock_cursor.fetchone.side_effect = [
        None,
        create_current_row(
            product_id="P002",
        ),
        create_current_row(
            product_id="P003",
        ),
    ]

    products = pd.DataFrame(
        [
            create_product(
                product_id="P001",
            ),
            create_product(
                product_id="P002",
            ),
            create_product(
                product_id="P003",
                selling_price=899.99,
            ),
        ]
    )

    inserted, closed = process_product_scd2(
        products,
        effective_date=EFFECTIVE_DATE,
    )

    assert inserted == 2
    assert closed == 1

    # P001: SELECT + INSERT
    # P002: SELECT
    # P003: SELECT + UPDATE + INSERT
    assert mock_cursor.execute.call_count == 6

    mock_conn.commit.assert_called_once()

    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


# ============================================================
# NULL / NaN COMPARISON
# ============================================================


@patch("etl.scd.product_scd2.get_connection")
def test_nan_and_none_are_treated_as_equal(
    mock_get_connection,
):
    """
    NaN source values should normalize to None, allowing
    comparison against warehouse NULL values without
    incorrectly creating an SCD2 version.
    """

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = create_current_row(
        brand=None,
        category=None,
        subcategory=None,
        supplier_id=None,
    )

    products = create_product_dataframe(
        brand=float("nan"),
        category=float("nan"),
        subcategory=float("nan"),
        supplier_id=float("nan"),
    )

    inserted, closed = process_product_scd2(
        products,
        effective_date=EFFECTIVE_DATE,
    )

    assert inserted == 0
    assert closed == 0

    # Only SELECT
    assert mock_cursor.execute.call_count == 1

    mock_conn.commit.assert_called_once()


# ============================================================
# NUMERIC NORMALIZATION
# ============================================================


@patch("etl.scd.product_scd2.get_connection")
def test_numeric_precision_difference_does_not_create_change(
    mock_get_connection,
):
    """
    Numeric values that differ only beyond two decimal places
    should be considered equal after normalization.
    """

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = create_current_row(
        standard_cost=Decimal("500.00"),
        selling_price=Decimal("799.99"),
    )

    products = create_product_dataframe(
        standard_cost=500.004,
        selling_price=799.994,
    )

    inserted, closed = process_product_scd2(
        products,
        effective_date=EFFECTIVE_DATE,
    )

    assert inserted == 0
    assert closed == 0

    # Only SELECT
    assert mock_cursor.execute.call_count == 1

    mock_conn.commit.assert_called_once()


# ============================================================
# DATABASE ERROR / ROLLBACK
# ============================================================


@patch("etl.scd.product_scd2.get_connection")
def test_database_error_rolls_back_and_reraises(
    mock_get_connection,
):
    """
    A database exception should rollback the transaction,
    close resources, and re-raise the original exception.
    """

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.execute.side_effect = RuntimeError(
        "Database error"
    )

    products = create_product_dataframe()

    with pytest.raises(RuntimeError, match="Database error"):
        process_product_scd2(
            products,
            effective_date=EFFECTIVE_DATE,
        )

    mock_conn.rollback.assert_called_once()

    mock_conn.commit.assert_not_called()

    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


# ============================================================
# EFFECTIVE DATE TEST
# ============================================================


@patch("etl.scd.product_scd2.get_connection")
def test_effective_date_is_used_for_new_product(
    mock_get_connection,
):
    """
    The supplied effective_date should be used as the
    effective_start_date for a newly inserted Product version.
    """

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = None

    effective_date = date(2026, 7, 1)

    products = create_product_dataframe()

    inserted, closed = process_product_scd2(
        products,
        effective_date=effective_date,
    )

    assert inserted == 1
    assert closed == 0

    insert_call = mock_cursor.execute.call_args_list[1]

    insert_values = insert_call.args[1]

    assert insert_values[9] == effective_date
    assert insert_values[10] == date(9999, 12, 31)

    mock_conn.commit.assert_called_once()


# ============================================================
# DEFAULT EFFECTIVE DATE
# ============================================================


@patch("etl.scd.product_scd2.date")
@patch("etl.scd.product_scd2.get_connection")
def test_effective_date_defaults_to_today(
    mock_get_connection,
    mock_date,
):
    """
    When effective_date is not supplied, date.today() should
    be used.
    """

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = None

    expected_date = date(2026, 8, 16)

    mock_date.today.return_value = expected_date
    mock_date.side_effect = date

    products = create_product_dataframe()

    inserted, closed = process_product_scd2(
        products
    )

    assert inserted == 1
    assert closed == 0

    insert_call = mock_cursor.execute.call_args_list[1]

    insert_values = insert_call.args[1]

    assert insert_values[9] == expected_date
    assert insert_values[10] == date(9999, 12, 31)

    mock_conn.commit.assert_called_once()