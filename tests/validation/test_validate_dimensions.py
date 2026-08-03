"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : test_validate_dimensions.py
Purpose : Test Dimension Validation Orchestrator
============================================================
"""

import pandas as pd

from etl.validation.validate_dimensions import (
    validate_all_dimensions,
)


def create_valid_dimensions():
    """
    Create representative transformed dimension
    DataFrames for validation testing.
    """

    return {
        "customer": pd.DataFrame(
            {
                "customer_id": ["C001", "C002"],
                "customer_name": ["Customer 1", "Customer 2"],
                "email": [
                    "customer1@example.com",
                    "customer2@example.com",
                ],
            }
        ),

        "employee": pd.DataFrame(
            {
                "employee_id": ["E001", "E002"],
                "employee_name": ["Employee 1", "Employee 2"],
            }
        ),

        "store": pd.DataFrame(
            {
                "store_id": ["S001", "S002"],
                "store_name": ["Store 1", "Store 2"],
                "store_type": [
                    "Supermarket",
                    "Express",
                ],
                "country": ["India", "India"],
                "store_status": ["Active", "Active"],
            }
        ),

        "supplier": pd.DataFrame(
            {
                "supplier_id": ["SUP001", "SUP002"],
                "supplier_name": [
                    "Supplier 1",
                    "Supplier 2",
                ],
            }
        ),

        "product": pd.DataFrame(
            {
                "product_id": ["P001", "P002"],
                "product_name": [
                    "Product 1",
                    "Product 2",
                ],
                "supplier_id": [
                    "SUP001",
                    "SUP002",
                ],
            }
        ),

        "promotion": pd.DataFrame(
            {
                "promotion_id": ["PROMO001", "PROMO002"],
                "promotion_name": [
                    "Campaign 1",
                    "Campaign 2",
                ],
                "promotion_type": [
                    "Percentage",
                    "Fixed Amount",
                ],
                "discount_percentage": [10, None],
                "discount_amount": [None, 100],
                "start_date": pd.to_datetime(
                    ["2026-01-01", "2026-02-01"]
                ).date,
                "end_date": pd.to_datetime(
                    ["2026-01-31", "2026-02-28"]
                ).date,
            }
        ),

        "date": pd.DataFrame(
            {
                "date_key": [20260101, 20260102],
                "full_date": pd.to_datetime(
                    ["2026-01-01", "2026-01-02"]
                ).date,
            }
        ),
    }


def test_validate_all_dimensions_passes():
    """
    Valid dimensions should pass the complete
    dimension validation framework.
    """

    dimensions = create_valid_dimensions()

    validate_all_dimensions(dimensions)