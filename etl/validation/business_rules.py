# ============================================================
# Project : Enterprise Retail Sales Analytics Data Warehouse
# File    : business_rules.py
# Purpose : Business Rule Validation Framework
# ============================================================

import pandas as pd


# ============================================================
# 1. POSITIVE VALUE VALIDATION
# ============================================================

def validate_positive_values(
    df: pd.DataFrame,
    columns: list[str],
) -> None:
    """
    Validate that specified columns contain values
    greater than zero.
    """

    missing_columns = [
        column
        for column in columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    for column in columns:

        invalid_count = (
            df[column].isna()
            | (df[column] <= 0)
        ).sum()

        if invalid_count > 0:
            raise ValueError(
                f"{column} must contain values "
                f"greater than zero. "
                f"Invalid rows: {invalid_count}"
            )


# ============================================================
# 2. NON-NEGATIVE VALUE VALIDATION
# ============================================================

def validate_non_negative_values(
    df: pd.DataFrame,
    columns: list[str],
) -> None:
    """
    Validate that specified columns contain
    non-negative values.
    """

    missing_columns = [
        column
        for column in columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    for column in columns:

        invalid_count = (
            df[column].isna()
            | (df[column] < 0)
        ).sum()

        if invalid_count > 0:
            raise ValueError(
                f"{column} must contain "
                f"non-negative values. "
                f"Invalid rows: {invalid_count}"
            )


# ============================================================
# 3. DATE ORDER VALIDATION
# ============================================================

def validate_date_order(
    df: pd.DataFrame,
    start_column: str,
    end_column: str,
) -> None:
    """
    Validate that the end date is greater than
    or equal to the start date.

    The warehouse default promotion record
    (promotion_key = 0) is excluded.
    """

    required_columns = [
        start_column,
        end_column,
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    default_row_mask = (
        (df["promotion_key"] == 0)
        if "promotion_key" in df.columns
        else pd.Series(False, index=df.index)
    )

    validation_df = df.loc[
        ~default_row_mask
    ].copy()

    if validation_df.empty:
        return

    start_dates = pd.to_datetime(
        validation_df[start_column],
        errors="coerce",
    )

    end_dates = pd.to_datetime(
        validation_df[end_column],
        errors="coerce",
    )

    invalid_mask = (
        start_dates.isna()
        | end_dates.isna()
        | (end_dates < start_dates)
    )

    invalid_count = invalid_mask.sum()

    if invalid_count == 0:
        return

    invalid_rows = validation_df.loc[
        invalid_mask
    ].copy()

    invalid_rows["_validated_start_date"] = (
        start_dates.loc[invalid_mask]
    )

    invalid_rows["_validated_end_date"] = (
        end_dates.loc[invalid_mask]
    )

    diagnostic_columns = [
        column
        for column in [
            "promotion_key",
            "promotion_id",
            "promotion_name",
            "promotion_type",
            start_column,
            end_column,
            "_validated_start_date",
            "_validated_end_date",
        ]
        if column in invalid_rows.columns
    ]

    print("\n" + "=" * 70)
    print("PROMOTION DATE VALIDATION FAILURE")
    print("=" * 70)
    print(
        invalid_rows[
            diagnostic_columns
        ].to_string(index=False)
    )
    print("=" * 70 + "\n")

    raise ValueError(
        f"{end_column} must be greater than "
        f"or equal to {start_column}. "
        f"Invalid rows: {invalid_count}"
    )


# ============================================================
# 4. SALES AMOUNT VALIDATION
# ============================================================

def validate_sales_amounts(
    df: pd.DataFrame,
) -> None:
    """
    Validate sales amount calculations.

    total_amount =
    (quantity × unit_price)
    - discount_amount
    + tax_amount
    """

    required_columns = [
        "quantity",
        "unit_price",
        "discount_amount",
        "tax_amount",
        "total_amount",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    expected_total = (
        df["quantity"]
        * df["unit_price"]
        - df["discount_amount"]
        + df["tax_amount"]
    )

    invalid_count = (
        expected_total.round(2)
        != df["total_amount"].round(2)
    ).sum()

    if invalid_count > 0:
        raise ValueError(
            "Sales amount calculation failed. "
            f"Invalid rows: {invalid_count}"
        )


# ============================================================
# 5. PROMOTION BUSINESS RULE VALIDATION
# ============================================================

def validate_promotion_rules(
    df: pd.DataFrame,
) -> None:
    """
    Validate promotion-specific business rules.
    """

    required_columns = [
        "promotion_type",
        "discount_percentage",
        "discount_amount",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # --------------------------------------------------------
    # Percentage Promotion
    # --------------------------------------------------------

    percentage_mask = (
        df["promotion_type"] == "Percentage"
    )

    invalid_percentage = (
        percentage_mask
        & (
            df["discount_percentage"].isna()
            | (df["discount_percentage"] < 0)
            | (df["discount_percentage"] > 100)
            | df["discount_amount"].notna()
        )
    ).sum()

    if invalid_percentage > 0:
        raise ValueError(
            "Percentage promotions must have a "
            "discount_percentage between 0 and 100 "
            "and no discount_amount. "
            f"Invalid rows: {invalid_percentage}"
        )

    # --------------------------------------------------------
    # Fixed Amount Promotion
    # --------------------------------------------------------

    fixed_mask = (
        df["promotion_type"] == "Fixed Amount"
    )

    invalid_fixed = (
        fixed_mask
        & (
            df["discount_amount"].isna()
            | (df["discount_amount"] < 0)
            | df["discount_percentage"].notna()
        )
    ).sum()

    if invalid_fixed > 0:
        raise ValueError(
            "Fixed Amount promotions must have a "
            "non-negative discount_amount and "
            "no discount_percentage. "
            f"Invalid rows: {invalid_fixed}"
        )

    # --------------------------------------------------------
    # Buy One Get One Promotion
    # --------------------------------------------------------

    bogo_mask = (
        df["promotion_type"] == "Buy One Get One"
    )

    invalid_bogo = (
        bogo_mask
        & (
            df["discount_percentage"].notna()
            | df["discount_amount"].notna()
        )
    ).sum()

    if invalid_bogo > 0:
        raise ValueError(
            "Buy One Get One promotions must not "
            "contain discount values. "
            f"Invalid rows: {invalid_bogo}"
        )

    # --------------------------------------------------------
    # Default Promotion
    # --------------------------------------------------------

    default_mask = (
        df["promotion_type"] == "None"
    )

    invalid_default = (
        default_mask
        & (
            df["discount_percentage"].notna()
            | df["discount_amount"].notna()
        )
    ).sum()

    if invalid_default > 0:
        raise ValueError(
            "Default 'No Promotion' records must "
            "not contain discount values. "
            f"Invalid rows: {invalid_default}"
        )