"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : test_transform_fact_sales.py
Purpose : Test Fact Sales Transformation
============================================================
"""
import pandas as pd

from etl.extract.extract import extract_data
from etl.transform.customer import transform_customer
from etl.transform.employee import transform_employee
from etl.transform.store import transform_store
from etl.transform.product import transform_product
from etl.transform.promotion import transform_promotion
from etl.transform.date import transform_date

from etl.transform.fact.merge_header_detail import (
    merge_header_detail,
)

from etl.transform.fact.lookup_keys import (
    lookup_dimension_keys,
)

from etl.transform.fact.fact_sales import (
    build_fact_sales,
)


def test_fact_sales():

    sources = extract_data()

    dim_customer = transform_customer(sources["customers"])
    dim_employee = transform_employee(sources["employees"])
    dim_store = transform_store(sources["stores"])
    dim_product = transform_product(sources["products"])
    dim_promotion = transform_promotion(sources["promotions"])
    dim_date = transform_date()

    # ==========================================================
    # Align SCD2 Effective Dates With Fact Data
    # ==========================================================

    min_transaction_date = pd.to_datetime(
        sources["sales_header"]["transaction_date"]
    ).min().normalize()

    dim_customer["effective_start_date"] = min_transaction_date
    dim_store["effective_start_date"] = min_transaction_date
    dim_product["effective_start_date"] = min_transaction_date

    fact = merge_header_detail(
        sources["sales_header"],
        sources["sales_detail"],
    )

    fact = lookup_dimension_keys(
        fact,
        dim_customer,
        dim_employee,
        dim_store,
        dim_product,
        dim_promotion,
        dim_date,
    )

    fact_sales = build_fact_sales(fact)

    print(fact_sales.head())
    print(fact_sales.columns)
    print("Rows:", len(fact_sales))

    assert len(fact_sales) == 219939
    assert fact_sales["sales_key"].is_unique
    assert fact_sales["transaction_id"].notna().all()
    assert fact_sales["date_key"].notna().all()
    assert fact_sales["customer_key"].notna().all()
    assert fact_sales["employee_key"].notna().all()
    assert fact_sales["store_key"].notna().all()
    assert fact_sales["product_key"].notna().all()
    assert fact_sales["promotion_key"].notna().all()

    assert (
        fact_sales
        .duplicated(
            subset=["transaction_id", "line_number"]
        )
        .sum()
        == 0
    )

    assert (fact_sales["quantity"] > 0).all()
    assert (fact_sales["unit_price"] >= 0).all()
    assert (fact_sales["discount_amount"] >= 0).all()
    assert (fact_sales["tax_amount"] >= 0).all()