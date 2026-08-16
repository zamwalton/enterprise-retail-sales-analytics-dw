"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : test_customer_scd2.py
Purpose : Test Customer SCD Type 2 Processing
============================================================
"""

import pandas as pd

from etl.scd.customer_scd2 import apply_customer_scd2


# ==========================================================
# Test Data Helper
# ==========================================================

def create_customer(
    customer_id="CUST00001",
    customer_name="John Doe",
    email="john@example.com",
    loyalty_tier="Silver",
):
    return {
        "customer_id": customer_id,
        "customer_name": customer_name,
        "gender": "Male",
        "date_of_birth": pd.Timestamp("1995-01-01"),
        "email": email,
        "phone": "9876543210",
        "city": "Kochi",
        "state": "Kerala",
        "country": "India",
        "loyalty_tier": loyalty_tier,
    }


# ==========================================================
# Test 1 — New Customer
# ==========================================================

def test_new_customer():

    incoming = pd.DataFrame(
        [
            create_customer()
        ]
    )

    existing = pd.DataFrame()

    result = apply_customer_scd2(
        incoming,
        existing,
        effective_date="2024-07-23",
    )

    assert len(result) == 1

    assert result.iloc[0]["customer_id"] == "CUST00001"

    assert (
        result.iloc[0]["effective_start_date"]
        == pd.Timestamp("2024-07-23")
    )

    assert (
        result.iloc[0]["effective_end_date"]
        == pd.Timestamp("9999-12-31")
    )

    assert bool(result.iloc[0]["is_current"]) is True


# ==========================================================
# Test 2 — Unchanged Customer
# ==========================================================

def test_unchanged_customer():

    incoming = pd.DataFrame(
        [
            create_customer()
        ]
    )

    existing = incoming.copy()

    existing["effective_start_date"] = pd.Timestamp(
        "2024-07-23"
    )

    existing["effective_end_date"] = pd.Timestamp(
        "9999-12-31"
    )

    existing["is_current"] = True

    existing["created_date"] = pd.Timestamp(
        "2024-07-23"
    )

    existing["updated_date"] = pd.Timestamp(
        "2024-07-23"
    )

    result = apply_customer_scd2(
        incoming,
        existing,
        effective_date="2025-01-01",
    )

    assert len(result) == 1

    assert result.iloc[0]["customer_id"] == "CUST00001"

    assert bool(result.iloc[0]["is_current"]) is True

    assert (
        result.iloc[0]["effective_start_date"]
        == pd.Timestamp("2024-07-23")
    )

    assert (
        result.iloc[0]["effective_end_date"]
        == pd.Timestamp("9999-12-31")
    )


# ==========================================================
# Test 3 — Changed Customer
# ==========================================================

def test_changed_customer():

    existing = pd.DataFrame(
        [
            create_customer(
                loyalty_tier="Silver"
            )
        ]
    )

    existing["effective_start_date"] = pd.Timestamp(
        "2024-07-23"
    )

    existing["effective_end_date"] = pd.Timestamp(
        "9999-12-31"
    )

    existing["is_current"] = True

    existing["created_date"] = pd.Timestamp(
        "2024-07-23"
    )

    existing["updated_date"] = pd.Timestamp(
        "2024-07-23"
    )

    incoming = pd.DataFrame(
        [
            create_customer(
                loyalty_tier="Gold"
            )
        ]
    )

    result = apply_customer_scd2(
        incoming,
        existing,
        effective_date="2026-01-01",
    )

    # Two versions should exist
    assert len(result) == 2

    # One historical version
    historical = result[
        result["is_current"] == False
    ]

    assert len(historical) == 1

    assert (
        historical.iloc[0]["loyalty_tier"]
        == "Silver"
    )

    assert (
        historical.iloc[0]["effective_start_date"]
        == pd.Timestamp("2024-07-23")
    )

    assert (
        historical.iloc[0]["effective_end_date"]
        == pd.Timestamp("2025-12-31")
    )

    # One current version
    current = result[
        result["is_current"] == True
    ]

    assert len(current) == 1

    assert (
        current.iloc[0]["loyalty_tier"]
        == "Gold"
    )

    assert (
        current.iloc[0]["effective_start_date"]
        == pd.Timestamp("2026-01-01")
    )

    assert (
        current.iloc[0]["effective_end_date"]
        == pd.Timestamp("9999-12-31")
    )


# ==========================================================
# Test 4 — New + Existing + Changed Customers
# ==========================================================

def test_mixed_customer_changes():

    existing = pd.DataFrame(
        [
            create_customer(
                customer_id="CUST00001",
                loyalty_tier="Silver",
            ),
            create_customer(
                customer_id="CUST00002",
                loyalty_tier="Gold",
            ),
        ]
    )

    existing["effective_start_date"] = pd.Timestamp(
        "2024-07-23"
    )

    existing["effective_end_date"] = pd.Timestamp(
        "9999-12-31"
    )

    existing["is_current"] = True

    existing["created_date"] = pd.Timestamp(
        "2024-07-23"
    )

    existing["updated_date"] = pd.Timestamp(
        "2024-07-23"
    )

    incoming = pd.DataFrame(
        [
            # Changed customer
            create_customer(
                customer_id="CUST00001",
                loyalty_tier="Gold",
            ),

            # Unchanged customer
            create_customer(
                customer_id="CUST00002",
                loyalty_tier="Gold",
            ),

            # New customer
            create_customer(
                customer_id="CUST00003",
                loyalty_tier="Bronze",
            ),
        ]
    )

    result = apply_customer_scd2(
        incoming,
        existing,
        effective_date="2026-01-01",
    )

    # 2 existing versions
    # + 1 new version for changed customer
    # + 1 completely new customer
    assert len(result) == 4

    # Three customers should have current versions
    current = result[
        result["is_current"] == True
    ]

    assert len(current) == 3

    assert set(
        current["customer_id"]
    ) == {
        "CUST00001",
        "CUST00002",
        "CUST00003",
    }

    # Only CUST00001 should have a historical version
    historical = result[
        result["is_current"] == False
    ]

    assert len(historical) == 1

    assert (
        historical.iloc[0]["customer_id"]
        == "CUST00001"
    )

    assert (
        historical.iloc[0]["loyalty_tier"]
        == "Silver"
    )