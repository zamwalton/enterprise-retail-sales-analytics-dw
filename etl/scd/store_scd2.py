"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : store_scd2.py
Purpose : SCD Type 2 Processing for Store Dimension
============================================================
"""

from datetime import date, timedelta

import pandas as pd

from datetime import date

from database.connection import get_connection
from etl.utils import logger


# ============================================================
# CONFIGURATION
# ============================================================

SCHEMA = "retail_dw"
TABLE = "dim_store"

BUSINESS_KEY = "store_id"

COMPARE_COLUMNS = [
    "store_name",
    "store_type",
    "city",
    "state",
    "country",
    "opening_date",
    "store_status",
]


# ============================================================
# NORMALIZE VALUES
# ============================================================

def _normalize_value(value):
    """
    Normalize values before comparing source and warehouse
    records.
    """

    if pd.isna(value):
        return None

    # Convert pandas timestamps to Python date
    if isinstance(value, pd.Timestamp):
        return value.date()

    # Convert Python datetime/date-like strings to date
    if isinstance(value, str):
        try:
            return pd.to_datetime(value).date()
        except (ValueError, TypeError):
            return value

    return value


# ============================================================
# APPLY SCD TYPE 2 IN MEMORY
# ============================================================

def apply_store_scd2(
    incoming: pd.DataFrame,
    existing: pd.DataFrame,
    effective_date: str | date,
) -> pd.DataFrame:
    """
    Apply SCD Type 2 logic to Store records in memory.

    Used for transformation-level testing.
    """

    effective_date = pd.Timestamp(
        effective_date
    ).normalize()

    end_of_time = pd.Timestamp(9999, 12, 31)

    # ----------------------------------------------------------
    # No incoming records
    # ----------------------------------------------------------

    if incoming.empty:
        return existing.copy()

    incoming = incoming.copy()

    # ----------------------------------------------------------
    # No existing dimension records
    # ----------------------------------------------------------

    if existing.empty:

        result = incoming.copy()

        result["effective_start_date"] = effective_date
        result["effective_end_date"] = end_of_time
        result["is_current"] = True

        return result.reset_index(drop=True)

    # ----------------------------------------------------------
    # Copy existing dimension
    # ----------------------------------------------------------

    result = existing.copy()
    result["effective_start_date"] = result[
        "effective_start_date"
    ].apply(
        lambda x: pd.Timestamp(x).normalize()
        if pd.notna(x)
        else x
    )

    result["effective_end_date"] = result[
        "effective_end_date"
    ].apply(
        lambda x: x.date()
        if isinstance(x, pd.Timestamp)
        else x
    )

    # ----------------------------------------------------------
    # Process each incoming store
    # ----------------------------------------------------------

    for _, source_row in incoming.iterrows():

        store_id = source_row[BUSINESS_KEY]

        current_mask = (
            (result[BUSINESS_KEY] == store_id)
            & (result["is_current"] == True)
        )

        current_rows = result.loc[current_mask]

        # ======================================================
        # NEW STORE
        # ======================================================

        if current_rows.empty:

            new_row = source_row.to_dict()

            new_row["effective_start_date"] = effective_date
            new_row["effective_end_date"] = end_of_time
            new_row["is_current"] = True

            result = pd.concat(
                [
                    result,
                    pd.DataFrame([new_row]),
                ],
                ignore_index=True,
            )

            continue

        # ======================================================
        # EXISTING STORE
        # ======================================================

        current_index = current_rows.index[0]

        current_row = result.loc[current_index]

        # ------------------------------------------------------
        # Detect changes
        # ------------------------------------------------------

        changed = False

        for column in COMPARE_COLUMNS:

            source_value = _normalize_value(
                source_row[column]
            )

            warehouse_value = _normalize_value(
                current_row[column]
            )

            if source_value != warehouse_value:
                changed = True
                break

        # ------------------------------------------------------
        # No change
        # ------------------------------------------------------

        if not changed:
            continue

        # ======================================================
        # CLOSE OLD VERSION
        # ======================================================

        result.loc[
            current_index,
            "effective_end_date",
        ] = (
            effective_date
            - pd.Timedelta(days=1)
        )

        result.loc[
            current_index,
            "is_current",
        ] = False

        # ======================================================
        # INSERT NEW VERSION
        # ======================================================

        new_row = source_row.to_dict()

        new_row["effective_start_date"] = effective_date
        new_row["effective_end_date"] = end_of_time
        new_row["is_current"] = True

        result = pd.concat(
            [
                result,
                pd.DataFrame([new_row]),
            ],
            ignore_index=True,
        )

    # ----------------------------------------------------------
    # Ensure correct boolean type
    # ----------------------------------------------------------

    result["is_current"] = result[
        "is_current"
    ].map(bool)

    return result.reset_index(drop=True)


# ============================================================
# PROCESS SCD TYPE 2
# ============================================================

def process_store_scd2(
    stores: pd.DataFrame,
    effective_date: date | None = None,
) -> tuple[int, int]:
    """
    Apply SCD Type 2 processing to the Store dimension.

    Parameters
    ----------
    stores : pd.DataFrame
        Transformed store source data.

    effective_date : date | None
        Date on which changes become effective.
        Defaults to today's date.

    Returns
    -------
    tuple[int, int]
        (inserted_versions, closed_versions)
    """

    if stores.empty:
        logger.info(
            "SCD2 Store processing skipped. No source records."
        )
        return 0, 0

    stores = stores.copy()

    if effective_date is None:
        effective_date = date.today()

    conn = None
    cursor = None

    inserted_versions = 0
    closed_versions = 0

    try:

        conn = get_connection()
        cursor = conn.cursor()

        logger.info(
            "========== STORE SCD2 PROCESSING STARTED =========="
        )

        for _, source_row in stores.iterrows():

            store_id = source_row[BUSINESS_KEY]

            # ------------------------------------------------
            # Get current warehouse version
            # ------------------------------------------------

            cursor.execute(
                f"""
                SELECT
                    store_key,
                    store_id,
                    store_name,
                    store_type,
                    city,
                    state,
                    country,
                    opening_date,
                    store_status,
                    effective_start_date,
                    effective_end_date,
                    is_current
                FROM {SCHEMA}.{TABLE}
                WHERE store_id = %s
                  AND is_current = TRUE
                """,
                (store_id,),
            )

            current_row = cursor.fetchone()

            # ------------------------------------------------
            # NEW STORE
            # ------------------------------------------------

            if current_row is None:

                cursor.execute(
                    f"""
                    INSERT INTO {SCHEMA}.{TABLE}
                    (
                        store_id,
                        store_name,
                        store_type,
                        city,
                        state,
                        country,
                        opening_date,
                        store_status,
                        effective_start_date,
                        effective_end_date,
                        is_current,
                        created_date,
                        updated_date
                    )
                    VALUES
                    (
                        %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, TRUE,
                        CURRENT_TIMESTAMP,
                        CURRENT_TIMESTAMP
                    )
                    """,
                    (
                        source_row["store_id"],
                        source_row["store_name"],
                        source_row["store_type"],
                        _normalize_value(source_row["city"]),
                        _normalize_value(source_row["state"]),
                        _normalize_value(source_row["country"]),
                        _normalize_value(source_row["opening_date"]),
                        source_row["store_status"],
                        effective_date,
                        date(9999, 12, 31),
                    ),
                )

                inserted_versions += 1

                continue

            # ------------------------------------------------
            # EXISTING STORE
            # ------------------------------------------------

            current = dict(
                zip(
                    [
                        "store_key",
                        "store_id",
                        "store_name",
                        "store_type",
                        "city",
                        "state",
                        "country",
                        "opening_date",
                        "store_status",
                        "effective_start_date",
                        "effective_end_date",
                        "is_current",
                    ],
                    current_row,
                )
            )

            # ------------------------------------------------
            # Detect attribute changes
            # ------------------------------------------------

            changed = False

            for column in COMPARE_COLUMNS:

                source_value = _normalize_value(
                    source_row[column]
                )

                warehouse_value = _normalize_value(
                    current[column]
                )

                if source_value != warehouse_value:
                    changed = True
                    break

            # ------------------------------------------------
            # No change
            # ------------------------------------------------

            if not changed:

                continue

            # ------------------------------------------------
            # Close current version
            # ------------------------------------------------

            cursor.execute(
                f"""
                UPDATE {SCHEMA}.{TABLE}
                SET
                    effective_end_date = %s,
                    is_current = FALSE,
                    updated_date = CURRENT_TIMESTAMP
                WHERE store_key = %s
                  AND is_current = TRUE
                """,
                (
                    effective_date - timedelta(days=1),
                    current["store_key"],
                ),
            )

            closed_versions += 1

            # ------------------------------------------------
            # Insert new version
            # ------------------------------------------------

            cursor.execute(
                f"""
                INSERT INTO {SCHEMA}.{TABLE}
                (
                    store_id,
                    store_name,
                    store_type,
                    city,
                    state,
                    country,
                    opening_date,
                    store_status,
                    effective_start_date,
                    effective_end_date,
                    is_current,
                    created_date,
                    updated_date
                )
                VALUES
                (
                    %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, TRUE,
                    CURRENT_TIMESTAMP,
                    CURRENT_TIMESTAMP
                )
                """,
                (
                    source_row["store_id"],
                    source_row["store_name"],
                    source_row["store_type"],
                    _normalize_value(source_row["city"]),
                    _normalize_value(source_row["state"]),
                    _normalize_value(source_row["country"]),
                    _normalize_value(source_row["opening_date"]),
                    source_row["store_status"],
                    effective_date,
                    date(9999, 12, 31),
                ),
            )

            inserted_versions += 1

            logger.info(
                "SCD2 change detected for %s. "
                "Old version closed and new version inserted.",
                store_id,
            )

        conn.commit()

        logger.info(
            "========== STORE SCD2 PROCESSING COMPLETED =========="
        )

        logger.info(
            "New versions inserted: %s",
            f"{inserted_versions:,}",
        )

        logger.info(
            "Old versions closed: %s",
            f"{closed_versions:,}",
        )

        return inserted_versions, closed_versions

    except Exception as e:

        if conn:
            conn.rollback()

        logger.error(
            "Store SCD2 processing failed: %s",
            e,
        )

        raise

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()