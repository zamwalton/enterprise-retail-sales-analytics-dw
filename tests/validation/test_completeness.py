"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : test_completeness.py
Purpose : Test completeness validation utilities
============================================================
"""

import pandas as pd
import pytest

from etl.validation.completeness import validate_not_null


def test_validate_not_null_passes():

    df = pd.DataFrame(
        {
            "customer_id": [
                "CUST001",
                "CUST002",
                "CUST003",
            ],
            "customer_name": [
                "Customer One",
                "Customer Two",
                "Customer Three",
            ],
        }
    )

    result = validate_not_null(
        df,
        [
            "customer_id",
            "customer_name",
        ],
    )

    assert result is True


def test_validate_not_null_detects_null_values():

    df = pd.DataFrame(
        {
            "customer_id": [
                "CUST001",
                None,
                "CUST003",
            ],
            "customer_name": [
                "Customer One",
                "Customer Two",
                None,
            ],
        }
    )

    with pytest.raises(
        ValueError,
        match="NULL values found",
    ):
        validate_not_null(
            df,
            [
                "customer_id",
                "customer_name",
            ],
        )


def test_validate_not_null_detects_missing_columns():

    df = pd.DataFrame(
        {
            "customer_id": [
                "CUST001",
                "CUST002",
            ],
        }
    )

    with pytest.raises(
        ValueError,
        match="Missing required columns",
    ):
        validate_not_null(
            df,
            [
                "customer_id",
                "customer_name",
            ],
        )