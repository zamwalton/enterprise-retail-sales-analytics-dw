"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : customer_scd2.py
Purpose : Customer SCD Type 2 Processing
============================================================
"""

import pandas as pd

from etl.utils import logger


# ==========================================================
# Constants
# ==========================================================

DEFAULT_END_DATE = pd.Timestamp("9999-12-31")


# ==========================================================
# Customer SCD Type 2
# ==========================================================

def apply_customer_scd2(
    incoming: pd.DataFrame,
    existing: pd.DataFrame,
    effective_date,
) -> pd.DataFrame:
    """
    Apply Slowly Changing Dimension Type 2 logic to Customer.

    Parameters
    ----------
    incoming : pd.DataFrame
        Newly extracted customer records.

    existing : pd.DataFrame
        Existing customer dimension records.

    effective_date : date-like
        Date on which the incoming customer version becomes effective.

    Returns
    -------
    pd.DataFrame
        Customer dimension containing historical and current versions.

    SCD Type 2 Rules
    ---------------
    1. New customer
       -> Insert a new current version.

    2. Existing customer with no tracked attribute change
       -> Keep the existing version.

    3. Existing customer with tracked attribute change
       -> Expire the old version.
       -> Insert a new current version.

    4. Historical records are never overwritten.
    """

    logger.info(
        "Applying Customer SCD Type 2 processing..."
    )

    # ======================================================
    # Validate Inputs
    # ======================================================

    if incoming is None:
        raise ValueError(
            "Incoming customer data cannot be None."
        )

    if existing is None:
        raise ValueError(
            "Existing customer dimension cannot be None."
        )

    incoming = incoming.copy()
    existing = existing.copy()

    # ======================================================
    # Normalize Effective Date
    # ======================================================

    effective_date = pd.Timestamp(
        effective_date
    ).normalize()

    # ======================================================
    # Business Key
    # ======================================================

    business_key = "customer_id"

    if business_key not in incoming.columns:
        raise ValueError(
            "Incoming customer data must contain "
            "'customer_id'."
        )

    if not existing.empty and business_key not in existing.columns:
        raise ValueError(
            "Existing customer dimension must contain "
            "'customer_id'."
        )

    # ======================================================
    # Tracked Attributes
    # ======================================================

    tracked_columns = [
        "customer_name",
        "gender",
        "date_of_birth",
        "email",
        "phone",
        "city",
        "state",
        "country",
        "loyalty_tier",
    ]

    missing_incoming = [
        column
        for column in tracked_columns
        if column not in incoming.columns
    ]

    if missing_incoming:
        raise ValueError(
            "Incoming customer data is missing tracked "
            f"columns: {missing_incoming}"
        )

    # ======================================================
    # Empty Existing Dimension
    # ======================================================

    if existing.empty:

        logger.info(
            "Existing Customer Dimension is empty. "
            "Creating initial SCD2 versions."
        )

        result = incoming.copy()

        result["effective_start_date"] = effective_date

        result["effective_end_date"] = (
            DEFAULT_END_DATE
        )

        result["is_current"] = True

        return result

    # ======================================================
    # Validate Existing Current Records
    # ======================================================

    current_records = existing[
        existing["is_current"] == True
    ].copy()

    if current_records[business_key].duplicated().any():

        raise ValueError(
            "Customer SCD2 validation failed: "
            "multiple current records exist for the "
            "same customer_id."
        )

    # ======================================================
    # Prepare Incoming Data
    # ======================================================

    incoming = incoming.drop_duplicates(
        subset=[business_key]
    ).copy()

    # ======================================================
    # Identify New Customers
    # ======================================================

    existing_customer_ids = set(
        existing[business_key]
    )

    new_customers = incoming[
        ~incoming[business_key].isin(
            existing_customer_ids
        )
    ].copy()

    # ======================================================
    # Identify Existing Customers
    # ======================================================

    existing_customers = incoming[
        incoming[business_key].isin(
            existing_customer_ids
        )
    ].copy()

    # ======================================================
    # Compare Current Versions
    # ======================================================

    comparison = existing_customers.merge(
        current_records[
            [
                business_key,
                *tracked_columns,
            ]
        ],
        on=business_key,
        how="left",
        suffixes=("_incoming", "_existing"),
        validate="one_to_one",
    )

    # ======================================================
    # Detect Changed Customers
    # ======================================================

    changed_mask = pd.Series(
        False,
        index=comparison.index,
    )

    for column in tracked_columns:

        incoming_column = f"{column}_incoming"
        existing_column = f"{column}_existing"

        difference = (
            comparison[incoming_column]
            != comparison[existing_column]
        )

        # Treat NaN / None on both sides as equal.
        both_null = (
            comparison[incoming_column].isna()
            & comparison[existing_column].isna()
        )

        changed_mask |= (
            difference & ~both_null
        )

    changed_customer_ids = comparison.loc[
        changed_mask,
        business_key,
    ].tolist()

    # ======================================================
    # No Changes
    # ======================================================

    unchanged_customer_ids = comparison.loc[
        ~changed_mask,
        business_key,
    ].tolist()

    logger.info(
        "Customer SCD2 comparison completed. "
        "New: %s | Changed: %s | Unchanged: %s",
        f"{len(new_customers):,}",
        f"{len(changed_customer_ids):,}",
        f"{len(unchanged_customer_ids):,}",
    )

    # ======================================================
    # Expire Changed Current Versions
    # ======================================================

    result = existing.copy()

    if changed_customer_ids:

        expire_mask = (
            result[business_key].isin(
                changed_customer_ids
            )
            & result["is_current"]
        )

        result.loc[
            expire_mask,
            "effective_end_date",
        ] = (
            effective_date
            - pd.Timedelta(days=1)
        )

        result.loc[
            expire_mask,
            "is_current",
        ] = False

        result.loc[
            expire_mask,
            "updated_date",
        ] = pd.Timestamp.now()

    # ======================================================
    # Create New Versions
    # ======================================================

    new_versions = incoming[
        incoming[business_key].isin(
            changed_customer_ids
        )
        | incoming[business_key].isin(
            new_customers[business_key]
        )
    ].copy()

    if not new_versions.empty:

        new_versions["effective_start_date"] = (
            effective_date
        )

        new_versions["effective_end_date"] = (
            DEFAULT_END_DATE
        )

        new_versions["is_current"] = True

        now = pd.Timestamp.now()

        new_versions["created_date"] = now
        new_versions["updated_date"] = now

        # Surrogate keys are assigned by the
        # warehouse transformation/loading layer.

    # ======================================================
    # Preserve Existing Records
    # ======================================================

    result = pd.concat(
        [
            result,
            new_versions,
        ],
        ignore_index=True,
    )

    # ======================================================
    # Final Validation
    # ======================================================

    current_counts = (
        result[result["is_current"]]
        .groupby(business_key)
        .size()
    )

    invalid_current = (
        current_counts > 1
    ).sum()

    if invalid_current > 0:

        raise ValueError(
            "Customer SCD2 validation failed: "
            f"{invalid_current:,} customers have "
            "multiple current versions."
        )

    logger.info(
        "Customer SCD2 processing completed. "
        "Total rows: %s",
        f"{len(result):,}",
    )

    return result