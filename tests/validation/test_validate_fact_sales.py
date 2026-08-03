"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : test_validate_fact_sales.py
Purpose : Test Fact Sales Data Quality Validation
============================================================
"""

import pandas as pd
import pytest

from etl.validation.validate_fact_sales import (
    validate_fact_sales,
)


def create_dimensions():

    dim_customer = pd.DataFrame({
        "customer_key": [1, 2],
    })

    dim_employee = pd.DataFrame({
        "employee_key": [1, 2],
    })

    dim_store = pd.DataFrame({
        "store_key": [1, 2],
    })

    dim_product = pd.DataFrame({
        "product_key": [1, 2],
    })

    dim_promotion = pd.DataFrame({
        "promotion_key": [0, 1],
    })

    dim_date = pd.DataFrame({
        "date_key": [20260101, 20260102],
    })

    return (
        dim_customer,
        dim_employee,
        dim_store,
        dim_product,
        dim_promotion,
        dim_date,
    )


def create_valid_fact():

    return pd.DataFrame({
        "transaction_id": [
            "TXN001",
            "TXN002",
        ],
        "line_number": [
            1,
            1,
        ],
        "date_key": [
            20260101,
            20260102,
        ],
        "customer_key": [
            1,
            2,
        ],
        "employee_key": [
            1,
            2,
        ],
        "store_key": [
            1,
            2,
        ],
        "product_key": [
            1,
            2,
        ],
        "promotion_key": [
            0,
            1,
        ],
        "quantity": [
            2,
            3,
        ],
        "unit_price": [
            100.00,
            200.00,
        ],
        "discount_amount": [
            0.00,
            20.00,
        ],
        "tax_amount": [
            18.00,
            36.00,
        ],
        "total_amount": [
            218.00,
            616.00,
        ],
    })


def test_validate_fact_sales_passes():

    fact_df = create_valid_fact()

    dimensions = create_dimensions()

    validate_fact_sales(
        fact_df,
        *dimensions,
    )


def test_validate_fact_sales_detects_orphan_customer_key():

    fact_df = create_valid_fact()

    fact_df.loc[0, "customer_key"] = 999

    dimensions = create_dimensions()

    with pytest.raises(ValueError):

        validate_fact_sales(
            fact_df,
            *dimensions,
        )


def test_validate_fact_sales_detects_duplicate_transaction_line():

    fact_df = create_valid_fact()

    fact_df.loc[1, "transaction_id"] = "TXN001"

    dimensions = create_dimensions()

    with pytest.raises(ValueError):

        validate_fact_sales(
            fact_df,
            *dimensions,
        )


def test_validate_fact_sales_detects_invalid_quantity():

    fact_df = create_valid_fact()

    fact_df.loc[0, "quantity"] = 0

    dimensions = create_dimensions()

    with pytest.raises(ValueError):

        validate_fact_sales(
            fact_df,
            *dimensions,
        )


def test_validate_fact_sales_detects_incorrect_total():

    fact_df = create_valid_fact()

    fact_df.loc[0, "total_amount"] = 999.00

    dimensions = create_dimensions()

    with pytest.raises(ValueError):

        validate_fact_sales(
            fact_df,
            *dimensions,
        )