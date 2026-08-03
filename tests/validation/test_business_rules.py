"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : test_business_rules.py
Purpose : Test Business Rule Validation Framework
============================================================
"""

import pandas as pd
import pytest

from etl.validation.business_rules import (
    validate_positive_values,
    validate_non_negative_values,
    validate_date_order,
    validate_sales_amounts,
    validate_promotion_rules,
)


# =========================================================
# Positive Value Validation
# =========================================================

def test_validate_positive_values_passes():

    df = pd.DataFrame(
        {
            "quantity": [1, 2, 5, 10],
        }
    )

    validate_positive_values(
        df,
        ["quantity"],
    )


def test_validate_positive_values_detects_invalid_values():

    df = pd.DataFrame(
        {
            "quantity": [1, 0, -5, 10],
        }
    )

    with pytest.raises(ValueError):

        validate_positive_values(
            df,
            ["quantity"],
        )


# =========================================================
# Non-Negative Value Validation
# =========================================================

def test_validate_non_negative_values_passes():

    df = pd.DataFrame(
        {
            "discount_amount": [0, 10, 50, 100],
        }
    )

    validate_non_negative_values(
        df,
        ["discount_amount"],
    )


def test_validate_non_negative_values_detects_negative_values():

    df = pd.DataFrame(
        {
            "discount_amount": [0, 10, -50, 100],
        }
    )

    with pytest.raises(ValueError):

        validate_non_negative_values(
            df,
            ["discount_amount"],
        )


# =========================================================
# Date Order Validation
# =========================================================

def test_validate_date_order_passes():

    df = pd.DataFrame(
        {
            "start_date": [
                "2026-01-01",
                "2026-02-01",
            ],
            "end_date": [
                "2026-01-10",
                "2026-02-15",
            ],
        }
    )

    validate_date_order(
        df,
        "start_date",
        "end_date",
    )


def test_validate_date_order_detects_invalid_dates():

    df = pd.DataFrame(
        {
            "start_date": [
                "2026-01-10",
            ],
            "end_date": [
                "2026-01-01",
            ],
        }
    )

    with pytest.raises(ValueError):

        validate_date_order(
            df,
            "start_date",
            "end_date",
        )


# =========================================================
# Sales Amount Validation
# =========================================================

def test_validate_sales_amounts_passes():

    df = pd.DataFrame(
        {
            "quantity": [2],
            "unit_price": [100.00],
            "discount_amount": [10.00],
            "tax_amount": [18.00],
            "total_amount": [208.00],
        }
    )

    validate_sales_amounts(df)


def test_validate_sales_amounts_detects_incorrect_total():

    df = pd.DataFrame(
        {
            "quantity": [2],
            "unit_price": [100.00],
            "discount_amount": [10.00],
            "tax_amount": [18.00],
            "total_amount": [250.00],
        }
    )

    with pytest.raises(ValueError):

        validate_sales_amounts(df)


# =========================================================
# Promotion Validation
# =========================================================

def test_validate_promotion_rules_passes():

    df = pd.DataFrame(
        {
            "promotion_type": [
                "Percentage",
                "Fixed Amount",
                "Buy One Get One",
            ],
            "discount_percentage": [
                20.0,
                None,
                None,
            ],
            "discount_amount": [
                None,
                500.0,
                None,
            ],
        }
    )

    validate_promotion_rules(df)


def test_validate_promotion_rules_detects_invalid_percentage():

    df = pd.DataFrame(
        {
            "promotion_type": [
                "Percentage",
            ],
            "discount_percentage": [
                150.0,
            ],
            "discount_amount": [
                None,
            ],
        }
    )

    with pytest.raises(ValueError):

        validate_promotion_rules(df)


def test_validate_promotion_rules_detects_invalid_fixed_amount():

    df = pd.DataFrame(
        {
            "promotion_type": [
                "Fixed Amount",
            ],
            "discount_percentage": [
                None,
            ],
            "discount_amount": [
                -100.0,
            ],
        }
    )

    with pytest.raises(ValueError):

        validate_promotion_rules(df)


def test_validate_promotion_rules_detects_invalid_bogo():

    df = pd.DataFrame(
        {
            "promotion_type": [
                "Buy One Get One",
            ],
            "discount_percentage": [
                10.0,
            ],
            "discount_amount": [
                None,
            ],
        }
    )

    with pytest.raises(ValueError):

        validate_promotion_rules(df)