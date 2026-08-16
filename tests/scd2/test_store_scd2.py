"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : test_store_scd2.py
Purpose : Test Store SCD Type 2 Processing
============================================================
"""

import pandas as pd

from datetime import date

from etl.scd.store_scd2 import apply_store_scd2


# ==========================================================
# Test Data Factory
# ==========================================================

def create_store(
    store_id="STORE00001",
    store_name="Main Store",
    store_type="Retail",
    city="Mumbai",
):
    return {
        "store_id": store_id,
        "store_name": store_name,
        "store_type": store_type,
        "city": city,
        "state": "Maharashtra",
        "country": "India",
        "opening_date": "2020-01-01",
        "store_status": "Active",
    }

# ==========================================================
# TEST 1 — NEW STORE
# ==========================================================

def test_new_store():

    incoming = pd.DataFrame(
        [
            create_store()
        ]
    )

    existing = pd.DataFrame()

    result = apply_store_scd2(
        incoming,
        existing,
        effective_date="2024-07-23",
    )

    assert len(result) == 1

    assert result.iloc[0]["store_id"] == "STORE00001"

    assert (
        result.iloc[0]["effective_start_date"]
        == pd.Timestamp("2024-07-23")
    )

    assert (
        result.iloc[0]["effective_end_date"]
        == pd.Timestamp(9999, 12, 31)
    )

    assert bool(result.iloc[0]["is_current"]) is True


# ==========================================================
# TEST 2 — UNCHANGED STORE
# ==========================================================

def test_unchanged_store():

    existing = pd.DataFrame(
        [
            {
                **create_store(),
                "store_key": 1,
                "effective_start_date": pd.Timestamp(
                    "2024-07-23"
                ),
                "effective_end_date": pd.Timestamp(
                    "9999-12-31"
                ),
                "is_current": True,
            }
        ]
    )

    incoming = pd.DataFrame(
        [
            create_store()
        ]
    )

    result = apply_store_scd2(
        incoming,
        existing,
        effective_date="2025-01-01",
    )

    assert len(result) == 1

    assert (
        result.iloc[0]["store_id"]
        == "STORE00001"
    )

    assert bool(
        result.iloc[0]["is_current"]
    ) is True

    assert (
        result.iloc[0]["effective_start_date"]
        == pd.Timestamp("2024-07-23")
    )

    assert (
        result.iloc[0]["effective_end_date"]
        == date(9999, 12, 31)
    )


# ==========================================================
# TEST 3 — CHANGED STORE
# ==========================================================

def test_changed_store():

    existing = pd.DataFrame(
        [
            {
                **create_store(
                    city="Mumbai"
                ),
                "store_key": 1,
                "effective_start_date": pd.Timestamp(
                    "2024-07-23"
                ),
                "effective_end_date": pd.Timestamp(
                    "9999-12-31"
                ),
                "is_current": True,
            }
        ]
    )

    incoming = pd.DataFrame(
        [
            create_store(
                city="Pune"
            )
        ]
    )

    result = apply_store_scd2(
        incoming,
        existing,
        effective_date="2025-01-01",
    )

    assert len(result) == 2

    # ------------------------------------------------------
    # Old Version
    # ------------------------------------------------------

    old_version = result[
        result["effective_start_date"]
        == pd.Timestamp("2024-07-23")
    ].iloc[0]

    assert old_version["city"] == "Mumbai"

    assert (  
        old_version["effective_end_date"]
        == pd.Timestamp("2024-12-31")
    )

    assert bool(
        old_version["is_current"]
    ) is False

    # ------------------------------------------------------
    # New Version
    # ------------------------------------------------------

    new_version = result[
        result["effective_start_date"]
        == pd.Timestamp("2025-01-01")
    ].iloc[0]

    assert new_version["city"] == "Pune"

    assert (
        new_version["effective_end_date"]
        == pd.Timestamp("9999-12-31")
    )

    assert bool(
        new_version["is_current"]
    ) is True


# ==========================================================
# TEST 4 — MIXED STORE CHANGES
# ==========================================================

def test_mixed_store_changes():

    existing = pd.DataFrame(
        [
            {
                **create_store(
                    store_id="STORE00001",
                    city="Mumbai",
                ),
                "store_key": 1,
                "effective_start_date": pd.Timestamp(
                    "2024-07-23"
                ),
                "effective_end_date": pd.Timestamp(
                    "9999-12-31"
                ),
                "is_current": True,
            },
            {
                **create_store(
                    store_id="STORE00002",
                    city="Delhi",
                ),
                "store_key": 2,
                "effective_start_date": pd.Timestamp(
                    "2024-07-23"
                ),
                "effective_end_date": pd.Timestamp(
                    "9999-12-31"
                ),
                "is_current": True,
            },
        ]
    )

    incoming = pd.DataFrame(
        [
            # STORE00001 unchanged
            create_store(
                store_id="STORE00001",
                city="Mumbai",
            ),

            # STORE00002 changed
            create_store(
                store_id="STORE00002",
                city="Bangalore",
            ),

            # New store
            create_store(
                store_id="STORE00003",
                city="Kochi",
            ),
        ]
    )

    result = apply_store_scd2(
        incoming,
        existing,
        effective_date="2025-01-01",
    )

    # 2 existing versions
    # + 1 new version for changed store
    # + 1 new store
    assert len(result) == 4

    # ------------------------------------------------------
    # Unchanged Store
    # ------------------------------------------------------

    unchanged = result[
        result["store_id"]
        == "STORE00001"
    ]

    assert len(unchanged) == 1

    assert unchanged.iloc[0]["city"] == "Mumbai"

    assert bool(
        unchanged.iloc[0]["is_current"]
    ) is True

    # ------------------------------------------------------
    # Changed Store
    # ------------------------------------------------------

    changed = result[
        result["store_id"]
        == "STORE00002"
    ]

    assert len(changed) == 2

    old_version = changed[
        changed["effective_start_date"]
        == pd.Timestamp("2024-07-23")
    ].iloc[0]

    new_version = changed[
        changed["effective_start_date"]
        == pd.Timestamp("2025-01-01")
    ].iloc[0]

    assert old_version["city"] == "Delhi"

    assert (
        old_version["effective_end_date"]
        == pd.Timestamp("2024-12-31")
    )

    assert bool(
        old_version["is_current"]
    ) is False

    assert new_version["city"] == "Bangalore"

    assert (
        new_version["effective_end_date"]
        == pd.Timestamp("9999-12-31")
    )

    assert bool(
        new_version["is_current"]
    ) is True

    # ------------------------------------------------------
    # New Store
    # ------------------------------------------------------

    new_store = result[
        result["store_id"]
        == "STORE00003"
    ]

    assert len(new_store) == 1

    assert new_store.iloc[0]["city"] == "Kochi"

    assert bool(
        new_store.iloc[0]["is_current"]
    ) is True