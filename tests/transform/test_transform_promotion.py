"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : test_transform_promotion.py
Purpose : Test Promotion Dimension Transformation
============================================================
"""

import pandas as pd
import pytest

from etl.transform.promotion import transform_promotion
from etl.validation.business_rules import (validate_promotion_rules,validate_date_order,)


# ==========================================================
# Test Promotion Dimension Transformation
# ==========================================================

def test_transform_promotion():

    # ======================================================
    # 1. CREATE TEST SOURCE DATA
    # ======================================================

    source = pd.DataFrame(
        {
            "promotion_id": [
                "PROMO001",
                "PROMO002",
                "PROMO003",
            ],
            "promotion_name": [
                "Summer Sale",
                "Festival Offer",
                "BOGO Campaign",
            ],
            "promotion_type": [
                "Percentage",
                "Fixed Amount",
                "Buy One Get One",
            ],
            "discount_value": [
                20,
                1000,
                0,
            ],
            "start_date": [
                "2026-07-01",
                "2026-07-05",
                "2026-07-10",
            ],
            "end_date": [
                "2026-07-15",
                "2026-07-20",
                "2026-07-25",
            ],
            "promotion_status": [
                "Active",
                "Active",
                "Scheduled",
            ],
        }
    )

    # ======================================================
    # 2. EXECUTE TRANSFORMATION
    # ======================================================

    result = transform_promotion(source)

    # ======================================================
    # 3. ROW COUNT VALIDATION
    # ======================================================
    #
    # 3 source promotions
    # + 1 default / unknown promotion row
    # = 4 warehouse rows
    #
    # ======================================================

    assert len(result) == 4

    # ======================================================
    # 4. DEFAULT / UNKNOWN PROMOTION VALIDATION
    # ======================================================

    default_rows = result[
        result["promotion_key"] == 0
    ]

    assert len(default_rows) == 1

    default_row = default_rows.iloc[0]

    # ------------------------------------------------------
    # Default surrogate key
    # ------------------------------------------------------

    assert default_row["promotion_key"] == 0

    # ------------------------------------------------------
    # Default business key
    # ------------------------------------------------------

    assert default_row["promotion_id"] == 0

    # ------------------------------------------------------
    # Default descriptive attributes
    # ------------------------------------------------------

    assert (
        default_row["promotion_name"]
        == "No Promotion"
    )

    assert (
        default_row["promotion_type"]
        == "None"
    )

    assert (
        default_row["promotion_status"]
        == "Not Applicable"
    )

    # ------------------------------------------------------
    # Default discount values
    # ------------------------------------------------------

    assert pd.isna(
        default_row["discount_percentage"]
    )

    assert pd.isna(
        default_row["discount_amount"]
    )

    # ======================================================
    # 5. REQUIRED COLUMN VALIDATION
    # ======================================================

    required_columns = [
        "promotion_key",
        "promotion_id",
        "promotion_name",
        "promotion_type",
        "discount_percentage",
        "discount_amount",
        "start_date",
        "end_date",
        "promotion_status",
        "effective_start_date",
        "effective_end_date",
        "is_current",
        "created_date",
        "updated_date",
    ]

    for column in required_columns:
        assert column in result.columns

    # ======================================================
    # 6. PERCENTAGE PROMOTION VALIDATION
    # ======================================================

    percentage = result[
        result["promotion_type"] == "Percentage"
    ].iloc[0]

    # ------------------------------------------------------
    # Discount percentage should contain source value
    # ------------------------------------------------------

    assert (
        percentage["discount_percentage"]
        == 20
    )

    # ------------------------------------------------------
    # Discount amount should be NULL
    # ------------------------------------------------------

    assert pd.isna(
        percentage["discount_amount"]
    )

    # ======================================================
    # 7. FIXED AMOUNT PROMOTION VALIDATION
    # ======================================================

    fixed_amount = result[
        result["promotion_type"] == "Fixed Amount"
    ].iloc[0]

    # ------------------------------------------------------
    # Discount percentage should be NULL
    # ------------------------------------------------------

    assert pd.isna(
        fixed_amount["discount_percentage"]
    )

    # ------------------------------------------------------
    # Discount amount should contain source value
    # ------------------------------------------------------

    assert (
        fixed_amount["discount_amount"]
        == 1000
    )

    # ======================================================
    # 8. BUY ONE GET ONE PROMOTION VALIDATION
    # ======================================================

    bogo = result[
        result["promotion_type"]
        == "Buy One Get One"
    ].iloc[0]

    # ------------------------------------------------------
    # BOGO has no percentage discount
    # ------------------------------------------------------

    assert pd.isna(
        bogo["discount_percentage"]
    )

    # ------------------------------------------------------
    # BOGO has no fixed amount discount
    # ------------------------------------------------------

    assert pd.isna(
        bogo["discount_amount"]
    )

    # ======================================================
    # 9. SCD TYPE 2 VALIDATION
    # ======================================================

    # ------------------------------------------------------
    # Every promotion must be marked current
    # ------------------------------------------------------

    assert result["is_current"].all()

    # ------------------------------------------------------
    # Current records have open-ended effective dates
    # ------------------------------------------------------

    assert (
        result["effective_end_date"]
        == pd.Timestamp(
            "9999-12-31"
        ).date()
    ).all()

    # ======================================================
    # 10. SURROGATE KEY VALIDATION
    # ======================================================
    #
    # Expected:
    #
    # 0 = Default / Unknown Promotion
    # 1 = PROMO001
    # 2 = PROMO002
    # 3 = PROMO003
    #
    # ======================================================

    assert (
        result["promotion_key"].tolist()
        == [0, 1, 2, 3]
    )

    # ======================================================
    # 11. BUSINESS KEY VALIDATION
    # ======================================================

    assert (
        result["promotion_id"].tolist()
        == [
            0,
            "PROMO001",
            "PROMO002",
            "PROMO003",
        ]
    )


# ==========================================================
# Test Invalid Percentage Promotion
# ==========================================================

def test_transform_promotion_invalid_percentage():

    # ======================================================
    # 1. CREATE INVALID SOURCE DATA
    # ======================================================

    source = pd.DataFrame(
        {
            "promotion_id": [
                "PROMO001"
            ],
            "promotion_name": [
                "Invalid Sale"
            ],
            "promotion_type": [
                "Percentage"
            ],
            "discount_value": [
                150
            ],
            "start_date": [
                "2026-07-01"
            ],
            "end_date": [
                "2026-07-15"
            ],
            "promotion_status": [
                "Active"
            ],
        }
    )

    # ======================================================
    # 2. EXPECT VALIDATION FAILURE
    # ======================================================

    result = transform_promotion(source)

    with pytest.raises(
        ValueError,
        match="Percentage promotions",
    ):
        validate_promotion_rules(result)


# ==========================================================
# Test Invalid Promotion Dates
# ==========================================================

def test_transform_promotion_invalid_dates():

    # ======================================================
    # 1. CREATE INVALID SOURCE DATA
    # ======================================================

    source = pd.DataFrame(
        {
            "promotion_id": [
                "PROMO001"
            ],
            "promotion_name": [
                "Invalid Date Sale"
            ],
            "promotion_type": [
                "Percentage"
            ],
            "discount_value": [
                20
            ],
            "start_date": [
                "2026-07-20"
            ],
            "end_date": [
                "2026-07-01"
            ],
            "promotion_status": [
                "Active"
            ],
        }
    )

    # ======================================================
    # 2. EXPECT VALIDATION FAILURE
    # ======================================================

    result = transform_promotion(source)

    with pytest.raises(
        ValueError,
        match="end_date",
    ):
        validate_date_order(
            result,
            "start_date",
            "end_date",
        )

