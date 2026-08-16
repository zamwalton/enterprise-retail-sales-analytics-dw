import pandas as pd

from etl.extract.extract import extract_data

from etl.transform.customer import transform_customer
from etl.transform.employee import transform_employee
from etl.transform.store import transform_store
from etl.transform.product import transform_product
from etl.transform.promotion import transform_promotion
from etl.transform.date import transform_date

from etl.transform.fact.merge_header_detail import merge_header_detail
from etl.transform.fact.lookup_keys import lookup_dimension_keys


def test_lookup_dimension_keys():

    data = extract_data()

    # ==========================================================
    # Transform Dimensions
    # ==========================================================

    dim_customer = transform_customer(data["customers"])
    dim_employee = transform_employee(data["employees"])
    dim_store = transform_store(data["stores"])
    dim_product = transform_product(data["products"])
    dim_promotion = transform_promotion(data["promotions"])
    dim_date = transform_date()

    # ==========================================================
    # Align SCD2 Effective Dates With Fact Data
    # ==========================================================

    min_transaction_date = pd.to_datetime(
        data["sales_header"]["transaction_date"]
    ).min().normalize()

    # Customer — SCD Type 2
    dim_customer["effective_start_date"] = min_transaction_date
    dim_customer["effective_end_date"] = pd.Timestamp("9999-12-31")

    # Store — SCD Type 2
    dim_store["effective_start_date"] = min_transaction_date
    dim_store["effective_end_date"] = pd.Timestamp("9999-12-31")

    # Product — SCD Type 2
    dim_product["effective_start_date"] = min_transaction_date
    dim_product["effective_end_date"] = pd.Timestamp("9999-12-31")

    # ==========================================================
    # Build Fact Dataset
    # ==========================================================

    fact = merge_header_detail(
        data["sales_header"],
        data["sales_detail"],
    )

    # ==========================================================
    # Lookup Surrogate Keys
    # ==========================================================

    fact = lookup_dimension_keys(
        fact,
        dim_customer,
        dim_employee,
        dim_store,
        dim_product,
        dim_promotion,
        dim_date,
    )

    # ==========================================================
    # Basic Validation
    # ==========================================================

    required_keys = [
        "customer_key",
        "employee_key",
        "store_key",
        "product_key",
        "promotion_key",
        "date_key",
    ]

    for key in required_keys:
        assert key in fact.columns, (
            f"Missing surrogate key column: {key}"
        )

    # Required dimension keys must not be NULL
    required_non_null_keys = [
        "customer_key",
        "employee_key",
        "store_key",
        "product_key",
        "date_key",
    ]

    for key in required_non_null_keys:
        assert fact[key].notna().all(), (
            f"{key} contains NULL values"
        )

    # ==========================================================
    # Validate Key Data Types
    # ==========================================================

    for key in required_non_null_keys:
        assert fact[key].dtype.kind in "iu", (
            f"{key} is not an integer type"
        )

    # Promotion key uses 0 for "no promotion"
    assert fact["promotion_key"].notna().all()

    # ==========================================================
    # Validate Row Count
    # ==========================================================

    assert len(fact) == len(data["sales_detail"])

    print("\nSurrogate key lookup test passed.")
    print(f"Fact rows: {len(fact):,}")