
"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : promotion.py
Purpose : Transform Promotion Dimension
============================================================
"""

import pandas as pd

from etl.utils import (
    logger,
    add_surrogate_key,
)


# ==========================================================
# Promotion Dimension Transformation
# ==========================================================

def transform_promotion(
    promotions: pd.DataFrame,
) -> pd.DataFrame:
    """
    Transform promotion source data into the
    dim_promotion warehouse structure.

    Includes:
    - Default warehouse member
    - Promotion discount transformation
    - Date standardization
    - SCD Type 2 attributes
    - Audit columns
    - Surrogate key generation

    Business rule validation is performed separately
    by the validation framework.
    """

    logger.info("Transforming Promotion Dimension...")

    # ======================================================
    # 1. COPY SOURCE DATA
    # ======================================================

    dim_promotion = promotions.copy()

    # ======================================================
    # 2. CREATE PROMOTION-SPECIFIC DISCOUNT COLUMNS
    # ======================================================

    dim_promotion["discount_percentage"] = pd.Series(
        pd.NA,
        index=dim_promotion.index,
        dtype="Float64",
    )

    dim_promotion["discount_amount"] = pd.Series(
        pd.NA,
        index=dim_promotion.index,
        dtype="Float64",
    )

    # ======================================================
    # 3. PERCENTAGE PROMOTIONS
    # ======================================================

    percentage_mask = (
        dim_promotion["promotion_type"] == "Percentage"
    )

    dim_promotion.loc[
        percentage_mask,
        "discount_percentage",
    ] = pd.to_numeric(
        dim_promotion.loc[
            percentage_mask,
            "discount_value",
        ],
        errors="coerce",
    )

    # ======================================================
    # 4. FIXED AMOUNT PROMOTIONS
    # ======================================================

    fixed_amount_mask = (
        dim_promotion["promotion_type"] == "Fixed Amount"
    )

    dim_promotion.loc[
        fixed_amount_mask,
        "discount_amount",
    ] = pd.to_numeric(
        dim_promotion.loc[
            fixed_amount_mask,
            "discount_value",
        ],
        errors="coerce",
    )

    # ======================================================
    # 5. BUY ONE GET ONE PROMOTIONS
    # ======================================================

    bogo_mask = (
        dim_promotion["promotion_type"]
        == "Buy One Get One"
    )

    dim_promotion.loc[
        bogo_mask,
        "discount_percentage",
    ] = pd.NA

    dim_promotion.loc[
        bogo_mask,
        "discount_amount",
    ] = pd.NA

    # ======================================================
    # 6. STANDARDIZE NUMERIC COLUMNS
    # ======================================================

    dim_promotion["discount_percentage"] = (
        pd.to_numeric(
            dim_promotion["discount_percentage"],
            errors="coerce",
        ).astype("Float64")
    )

    dim_promotion["discount_amount"] = (
        pd.to_numeric(
            dim_promotion["discount_amount"],
            errors="coerce",
        ).astype("Float64")
    )

    # ======================================================
    # 7. STANDARDIZE DATE COLUMNS
    # ======================================================

    dim_promotion["start_date"] = pd.to_datetime(
        dim_promotion["start_date"],
        errors="coerce",
    ).dt.date

    dim_promotion["end_date"] = pd.to_datetime(
        dim_promotion["end_date"],
        errors="coerce",
    ).dt.date

    # ======================================================
    # 8. SCD TYPE 2 & AUDIT TIMESTAMP
    # ======================================================

    now = pd.Timestamp.now()
    effective_start_date = now.date()

    dim_promotion["effective_start_date"] = effective_start_date
    dim_promotion["effective_end_date"] = (
        pd.Timestamp("9999-12-31").date()
    )

    dim_promotion["is_current"] = True

    # ======================================================
    # 9. AUDIT COLUMNS
    # ======================================================

    dim_promotion["created_date"] = now
    dim_promotion["updated_date"] = now

    # ======================================================
    # 10. CREATE SURROGATE KEYS
    # ======================================================

    dim_promotion = add_surrogate_key(
        dim_promotion,
        "promotion_key",
    )

    # ======================================================
    # 11. SELECT WAREHOUSE COLUMNS
    # ======================================================

    dim_promotion = dim_promotion[
        [
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
    ]



    # ======================================================
    # 12. CREATE DEFAULT / UNKNOWN PROMOTION RECORD
    # ======================================================
    #
    # promotion_key = 0 is the warehouse default member.
    #
    # It represents transactions where no promotion applies.
    #
    # IMPORTANT:
    # The default member receives a valid date range so that
    # generic dimension date validation will also pass.
    # ======================================================

    default_promotion = pd.DataFrame(
        [
            {
                "promotion_key": 0,
                "promotion_id": 0,
                "promotion_name": "No Promotion",
                "promotion_type": "None",
                "discount_percentage": pd.NA,
                "discount_amount": pd.NA,

                # --------------------------------------------------
                # Valid date range for the default warehouse member
                # --------------------------------------------------
                "start_date": pd.Timestamp(
                    "1900-01-01"
                ).date(),

                "end_date": pd.Timestamp(
                    "9999-12-31"
                ).date(),

                "promotion_status": "Not Applicable",

                "effective_start_date": effective_start_date,

                "effective_end_date": pd.Timestamp(
                    "9999-12-31"
                ).date(),

                "is_current": True,

                "created_date": now,
                "updated_date": now,
            }
        ]
    )

    # ======================================================
    # 13. MATCH DATA TYPES BEFORE CONCATENATION
    # ======================================================
    #
    # Explicit dtype handling prevents pandas FutureWarning
    # messages during DataFrame concatenation.
    # ======================================================

    default_promotion[
        "discount_percentage"
    ] = default_promotion[
        "discount_percentage"
    ].astype("Float64")

    default_promotion[
        "discount_amount"
    ] = default_promotion[
        "discount_amount"
    ].astype("Float64")

    dim_promotion[
        "discount_percentage"
    ] = dim_promotion[
        "discount_percentage"
    ].astype("Float64")

    dim_promotion[
        "discount_amount"
    ] = dim_promotion[
        "discount_amount"
    ].astype("Float64")

    # ======================================================
    # 14. APPEND DEFAULT PROMOTION RECORD
    # ======================================================

    dim_promotion = pd.concat(
        [
            default_promotion,
            dim_promotion,
        ],
        ignore_index=True,
    )

 
    # ======================================================
    # 15. FINAL LOGGING
    # ======================================================

    logger.info(
    "Promotion Dimension transformed successfully (%s rows).",
    f"{len(dim_promotion):,}",
    )

    return dim_promotion

