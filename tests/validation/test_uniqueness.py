"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : test_uniqueness.py
Purpose : Test uniqueness validation utilities
============================================================
"""

import pandas as pd
import pytest

from etl.validation.uniqueness import validate_unique


def test_validate_unique_passes():

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

    result = validate_unique(
        df,
        ["customer_id"],
    )

    assert result is True


def test_validate_unique_detects_duplicates():

    df = pd.DataFrame(
        {
            "customer_id": [
                "CUST001",
                "CUST002",
                "CUST001",
            ],
            "customer_name": [
                "Customer One",
                "Customer Two",
                "Customer One Duplicate",
            ],
        }
    )

    with pytest.raises(
        ValueError,
        match="duplicate rows",
    ):
        validate_unique(
            df,
            ["customer_id"],
        )


def test_validate_composite_key_uniqueness():

    df = pd.DataFrame(
        {
            "transaction_id": [
                "TXN001",
                "TXN001",
                "TXN002",
            ],
            "line_number": [
                1,
                2,
                1,
            ],
        }
    )

    result = validate_unique(
        df,
        [
            "transaction_id",
            "line_number",
        ],
    )

    assert result is True


def test_validate_unique_detects_missing_column():

    df = pd.DataFrame(
        {
            "customer_id": [
                "CUST001",
                "CUST002",
            ]
        }
    )

    with pytest.raises(
        ValueError,
        match="Missing required columns",
    ):
        validate_unique(
            df,
            [
                "customer_id",
                "customer_name",
            ],
        )