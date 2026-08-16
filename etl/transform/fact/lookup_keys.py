"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : lookup_keys.py
Purpose : Replace Business Keys with Surrogate Keys
          and perform SCD Type 2 temporal lookups
============================================================
"""

import pandas as pd

from etl.utils import logger


def lookup_dimension_keys(
    fact: pd.DataFrame,
    dim_customer: pd.DataFrame,
    dim_employee: pd.DataFrame,
    dim_store: pd.DataFrame,
    dim_product: pd.DataFrame,
    dim_promotion: pd.DataFrame,
    dim_date: pd.DataFrame,
) -> pd.DataFrame:
    """
    Replace business keys with warehouse surrogate keys.

    Lookup strategy
    ---------------

    Customer  : SCD Type 2 temporal lookup
    Employee  : Standard business-key lookup
    Store     : SCD Type 2 temporal lookup
    Product    : SCD Type 2 temporal lookup
    Promotion : Standard business-key lookup
    Date      : Calendar date lookup

    SCD Type 2 rule
    ---------------

    A fact record matches a dimension version when:

        effective_start_date <= transaction_date
        AND
        transaction_date < effective_end_date

    This uses a half-open interval.
    """

    logger.info("Looking up surrogate keys...")

    # ==========================================================
    # Validate Input
    # ==========================================================

    if fact.empty:
        logger.warning("Fact DataFrame contains 0 rows.")
        return fact

    fact = fact.copy()

    # ==========================================================
    # Stable Fact Row Identifier
    # ==========================================================

    fact["_fact_row_id"] = range(len(fact))

    # ==========================================================
    # Normalize Transaction Date
    # ==========================================================

    if "transaction_date" not in fact.columns:
        raise ValueError(
            "Fact data does not contain transaction_date."
        )

    fact["transaction_date"] = pd.to_datetime(
        fact["transaction_date"],
        errors="coerce",
    ).dt.normalize()

    invalid_transaction_dates = (
        fact["transaction_date"].isna().sum()
    )

    if invalid_transaction_dates > 0:
        raise ValueError(
            "Transaction date validation failed: "
            f"{invalid_transaction_dates:,} rows contain "
            "invalid or missing transaction_date values."
        )

    # ==========================================================
    # CUSTOMER — SCD TYPE 2
    # ==========================================================

    logger.info(
        "Looking up Customer surrogate keys using SCD Type 2..."
    )

    dim_customer_lookup = dim_customer[
        [
            "customer_id",
            "customer_key",
            "effective_start_date",
            "effective_end_date",
        ]
    ].copy()

    # ----------------------------------------------------------
    # Normalize Customer effective dates
    # ----------------------------------------------------------

    dim_customer_lookup["effective_start_date"] = (
        pd.to_datetime(
            dim_customer_lookup["effective_start_date"],
            errors="coerce",
        ).dt.normalize()
    )

    dim_customer_lookup["effective_end_date"] = (
        pd.to_datetime(
            dim_customer_lookup["effective_end_date"],
            errors="coerce",
        ).dt.normalize()
    )

    # ----------------------------------------------------------
    # Validate Customer effective dates
    # ----------------------------------------------------------

    invalid_customer_dates = (
        dim_customer_lookup[
            [
                "effective_start_date",
                "effective_end_date",
            ]
        ]
        .isna()
        .any(axis=1)
        .sum()
    )

    if invalid_customer_dates > 0:
        raise ValueError(
            "Customer SCD2 validation failed: "
            f"{invalid_customer_dates:,} rows contain "
            "missing or invalid effective dates."
        )

    # ----------------------------------------------------------
    # Validate Customer effective date ranges
    # ----------------------------------------------------------

    invalid_customer_ranges = (
        dim_customer_lookup[
            "effective_end_date"
        ]
        <= dim_customer_lookup[
            "effective_start_date"
        ]
    ).sum()

    if invalid_customer_ranges > 0:
        raise ValueError(
            "Customer SCD2 validation failed: "
            f"{invalid_customer_ranges:,} rows contain "
            "invalid effective date ranges."
        )

    # ----------------------------------------------------------
    # Merge candidate Customer versions
    # ----------------------------------------------------------

    fact = fact.merge(
        dim_customer_lookup,
        on="customer_id",
        how="left",
        suffixes=("", "_customer"),
    )

    # ----------------------------------------------------------
    # Determine valid Customer version
    # ----------------------------------------------------------

    customer_match = (
        fact["transaction_date"]
        >= fact["effective_start_date"]
    ) & (
        fact["transaction_date"]
        < fact["effective_end_date"]
    )

    # ----------------------------------------------------------
    # Count valid Customer versions per original fact row
    # ----------------------------------------------------------

    customer_match_counts = (
        customer_match
        .groupby(fact["_fact_row_id"])
        .transform("sum")
    )

    # ----------------------------------------------------------
    # No Customer version found
    # ----------------------------------------------------------

    unmatched_customer = (
        customer_match_counts == 0
    ).sum()

    if unmatched_customer > 0:

        unmatched_customer_ids = (
            fact.loc[
                customer_match_counts == 0,
                "customer_id",
            ]
            .drop_duplicates()
            .head(10)
            .tolist()
        )

        raise ValueError(
            "Customer SCD2 lookup failed: "
            f"{unmatched_customer:,} fact rows have no "
            "dimension version valid for transaction_date. "
            f"Example customer IDs: "
            f"{unmatched_customer_ids}"
        )

    # ----------------------------------------------------------
    # Multiple Customer versions found
    # ----------------------------------------------------------

    duplicate_customer_matches = (
        customer_match_counts > 1
    ).sum()

    if duplicate_customer_matches > 0:

        duplicate_customer_ids = (
            fact.loc[
                customer_match_counts > 1,
                "customer_id",
            ]
            .drop_duplicates()
            .head(10)
            .tolist()
        )

        raise ValueError(
            "Customer SCD2 lookup failed: "
            f"{duplicate_customer_matches:,} fact rows match "
            "multiple dimension versions. "
            f"Example customer IDs: "
            f"{duplicate_customer_ids}"
        )

    # ----------------------------------------------------------
    # Keep only valid Customer version
    # ----------------------------------------------------------

    fact = fact.loc[
        customer_match
    ].copy()

    fact.drop(
        columns=[
            "effective_start_date",
            "effective_end_date",
        ],
        inplace=True,
    )

    # ==========================================================
    # EMPLOYEE
    # ==========================================================

    logger.info(
        "Looking up Employee surrogate keys..."
    )

    employee_lookup = dim_employee[
        [
            "employee_id",
            "employee_key",
        ]
    ].copy()

    if employee_lookup[
        "employee_id"
    ].duplicated().any():

        raise ValueError(
            "Employee dimension contains duplicate "
            "employee_id values."
        )

    fact = fact.merge(
        employee_lookup,
        on="employee_id",
        how="left",
        validate="many_to_one",
    )

    # ==========================================================
    # STORE — SCD TYPE 2
    # ==========================================================

    logger.info(
        "Looking up Store surrogate keys using SCD Type 2..."
    )

    dim_store_lookup = dim_store[
        [
            "store_id",
            "store_key",
            "effective_start_date",
            "effective_end_date",
        ]
    ].copy()

    dim_store_lookup["effective_start_date"] = (
        pd.to_datetime(
            dim_store_lookup["effective_start_date"],
            errors="coerce",
        ).dt.normalize()
    )

    dim_store_lookup["effective_end_date"] = (
        pd.to_datetime(
            dim_store_lookup["effective_end_date"],
            errors="coerce",
        ).dt.normalize()
    )

    invalid_store_dates = (
        dim_store_lookup[
            [
                "effective_start_date",
                "effective_end_date",
            ]
        ]
        .isna()
        .any(axis=1)
        .sum()
    )

    if invalid_store_dates > 0:
        raise ValueError(
            "Store SCD2 validation failed: "
            f"{invalid_store_dates:,} rows contain "
            "missing or invalid effective dates."
        )

    invalid_store_ranges = (
        dim_store_lookup[
            "effective_end_date"
        ]
        <= dim_store_lookup[
            "effective_start_date"
        ]
    ).sum()

    if invalid_store_ranges > 0:
        raise ValueError(
            "Store SCD2 validation failed: "
            f"{invalid_store_ranges:,} rows contain "
            "invalid effective date ranges."
        )

    fact = fact.merge(
        dim_store_lookup,
        on="store_id",
        how="left",
        suffixes=("", "_store"),
    )

    store_match = (
        fact["transaction_date"]
        >= fact["effective_start_date"]
    ) & (
        fact["transaction_date"]
        < fact["effective_end_date"]
    )

    store_match_counts = (
        store_match
        .groupby(fact["_fact_row_id"])
        .transform("sum")
    )

    unmatched_store = (
        store_match_counts == 0
    ).sum()

    if unmatched_store > 0:

        unmatched_store_ids = (
            fact.loc[
                store_match_counts == 0,
                "store_id",
            ]
            .drop_duplicates()
            .head(10)
            .tolist()
        )

        raise ValueError(
            "Store SCD2 lookup failed: "
            f"{unmatched_store:,} fact rows have no "
            "dimension version valid for transaction_date. "
            f"Example store IDs: {unmatched_store_ids}"
        )

    duplicate_store_matches = (
        store_match_counts > 1
    ).sum()

    if duplicate_store_matches > 0:

        duplicate_store_ids = (
            fact.loc[
                store_match_counts > 1,
                "store_id",
            ]
            .drop_duplicates()
            .head(10)
            .tolist()
        )

        raise ValueError(
            "Store SCD2 lookup failed: "
            f"{duplicate_store_matches:,} fact rows match "
            "multiple dimension versions. "
            f"Example store IDs: {duplicate_store_ids}"
        )

    fact = fact.loc[
        store_match
    ].copy()

    fact.drop(
        columns=[
            "effective_start_date",
            "effective_end_date",
        ],
        inplace=True,
    )

    # ==========================================================
    # PRODUCT — SCD TYPE 2
    # ==========================================================

    logger.info(
        "Looking up Product surrogate keys using SCD Type 2..."
    )

    dim_product_lookup = dim_product[
        [
            "product_id",
            "product_key",
            "effective_start_date",
            "effective_end_date",
        ]
    ].copy()

    dim_product_lookup["effective_start_date"] = (
        pd.to_datetime(
            dim_product_lookup["effective_start_date"],
            errors="coerce",
        ).dt.normalize()
    )

    dim_product_lookup["effective_end_date"] = (
        pd.to_datetime(
            dim_product_lookup["effective_end_date"],
            errors="coerce",
        ).dt.normalize()
    )

    invalid_product_dates = (
        dim_product_lookup[
            [
                "effective_start_date",
                "effective_end_date",
            ]
        ]
        .isna()
        .any(axis=1)
        .sum()
    )

    if invalid_product_dates > 0:
        raise ValueError(
            "Product SCD2 validation failed: "
            f"{invalid_product_dates:,} rows contain "
            "missing or invalid effective dates."
        )

    invalid_product_ranges = (
        dim_product_lookup[
            "effective_end_date"
        ]
        <= dim_product_lookup[
            "effective_start_date"
        ]
    ).sum()

    if invalid_product_ranges > 0:
        raise ValueError(
            "Product SCD2 validation failed: "
            f"{invalid_product_ranges:,} rows contain "
            "invalid effective date ranges."
        )

    fact = fact.merge(
        dim_product_lookup,
        on="product_id",
        how="left",
        suffixes=("", "_product"),
    )

    product_match = (
        fact["transaction_date"]
        >= fact["effective_start_date"]
    ) & (
        fact["transaction_date"]
        < fact["effective_end_date"]
    )

    product_match_counts = (
        product_match
        .groupby(fact["_fact_row_id"])
        .transform("sum")
    )

    unmatched_product = (
        product_match_counts == 0
    ).sum()

    if unmatched_product > 0:

        unmatched_product_ids = (
            fact.loc[
                product_match_counts == 0,
                "product_id",
            ]
            .drop_duplicates()
            .head(10)
            .tolist()
        )

        raise ValueError(
            "Product SCD2 lookup failed: "
            f"{unmatched_product:,} fact rows have no "
            "dimension version valid for transaction_date. "
            f"Example product IDs: "
            f"{unmatched_product_ids}"
        )

    duplicate_product_matches = (
        product_match_counts > 1
    ).sum()

    if duplicate_product_matches > 0:

        duplicate_product_ids = (
            fact.loc[
                product_match_counts > 1,
                "product_id",
            ]
            .drop_duplicates()
            .head(10)
            .tolist()
        )

        raise ValueError(
            "Product SCD2 lookup failed: "
            f"{duplicate_product_matches:,} fact rows match "
            "multiple dimension versions. "
            f"Example product IDs: "
            f"{duplicate_product_ids}"
        )

    fact = fact.loc[
        product_match
    ].copy()

    fact.drop(
        columns=[
            "effective_start_date",
            "effective_end_date",
        ],
        inplace=True,
    )

    # ==========================================================
    # PROMOTION
    # ==========================================================

    logger.info(
        "Looking up Promotion surrogate keys..."
    )

    promotion_lookup = dim_promotion[
        [
            "promotion_id",
            "promotion_key",
        ]
    ].copy()

    if promotion_lookup[
        "promotion_id"
    ].duplicated().any():

        raise ValueError(
            "Promotion dimension contains duplicate "
            "promotion_id values."
        )

    fact = fact.merge(
        promotion_lookup,
        on="promotion_id",
        how="left",
        validate="many_to_one",
    )

    fact["promotion_key"] = (
        fact["promotion_key"]
        .fillna(0)
        .astype(int)
    )

    # ==========================================================
    # DATE
    # ==========================================================

    logger.info(
        "Looking up Date surrogate keys..."
    )

    dim_date_lookup = dim_date[
        [
            "full_date",
            "date_key",
        ]
    ].copy()

    dim_date_lookup["full_date"] = (
        pd.to_datetime(
            dim_date_lookup["full_date"],
            errors="coerce",
        ).dt.normalize()
    )

    if dim_date_lookup[
        "full_date"
    ].duplicated().any():

        raise ValueError(
            "Date dimension contains duplicate full_date values."
        )

    fact = fact.merge(
        dim_date_lookup,
        left_on="transaction_date",
        right_on="full_date",
        how="left",
        validate="many_to_one",
    )

    fact.drop(
        columns=["full_date"],
        inplace=True,
    )

    # ==========================================================
    # FINAL SURROGATE KEY VALIDATION
    # ==========================================================

    required_keys = [
        "customer_key",
        "employee_key",
        "store_key",
        "product_key",
        "date_key",
    ]

    logger.info(
        "Validating surrogate key lookups..."
    )

    for key in required_keys:

        missing_count = fact[key].isna().sum()

        if missing_count > 0:

            raise ValueError(
                f"Surrogate key lookup failed for {key}: "
                f"{missing_count:,} rows have no matching "
                "dimension record."
            )

    # ==========================================================
    # Convert Surrogate Keys to Integer
    # ==========================================================

    fact["customer_key"] = (
        fact["customer_key"].astype(int)
    )

    fact["employee_key"] = (
        fact["employee_key"].astype(int)
    )

    fact["store_key"] = (
        fact["store_key"].astype(int)
    )

    fact["product_key"] = (
        fact["product_key"].astype(int)
    )

    fact["date_key"] = (
        fact["date_key"].astype(int)
    )

    # ==========================================================
    # Remove Temporary Technical Column
    # ==========================================================

    fact.drop(
        columns=["_fact_row_id"],
        inplace=True,
    )

    # ==========================================================
    # Final Logging
    # ==========================================================

    logger.info(
        "SCD2-aware surrogate key lookup completed."
    )

    logger.info(
        "Fact rows after dimension lookup: %s",
        f"{len(fact):,}",
    )

    return fact