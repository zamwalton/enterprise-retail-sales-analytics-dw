"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : pipeline.py
Purpose : End-to-end ETL orchestration
============================================================
"""
import time
from etl.extract.extract import extract_data

from etl.transform.customer import transform_customer
from etl.transform.employee import transform_employee
from etl.transform.fact import fact_sales
from etl.transform.store import transform_store
from etl.transform.supplier import transform_supplier
from etl.transform.product import transform_product
from etl.transform.promotion import transform_promotion
from etl.transform.date import transform_date
from etl.load.clear_warehouse import clear_warehouse
from etl.validation.validate_dimensions import validate_all_dimensions
from etl.validation.validate_fact_sales import validate_fact_sales

from etl.transform.fact.merge_header_detail import (
    merge_header_detail
)

from etl.transform.fact.lookup_keys import (
    lookup_dimension_keys
)

from etl.transform.fact.fact_sales import (
    build_fact_sales
)

from etl.load.postgres_loader import load_dataframe

from etl.utils.utils import logger



def run_pipeline():
    start_time = time.perf_counter()

    logger.info("========== ETL PIPELINE STARTED ==========")

    # ======================================================
    # 1. EXTRACT
    # ======================================================

    logger.info("Extracting source datasets...")

    data = extract_data()

    logger.info("Extraction completed.")

    # ======================================================
    # 2. TRANSFORM DIMENSIONS
    # ======================================================

    logger.info("========== DIMENSION TRANSFORMATION STARTED ==========")

    #.Transforming Customer Dimension...
    dim_customer = transform_customer(
        data["customers"]
    )

    #.Transforming Employee Dimension...
    dim_employee = transform_employee(
        data["employees"]
    )

    #.Transforming Store Dimension...
    dim_store = transform_store(
        data["stores"]
    )

    #.Transforming Supplier Dimension...
    dim_supplier = transform_supplier(
        data["suppliers"]
    )

    #.Transforming Product Dimension...
    dim_product = transform_product(
        data["products"]
    )

    #.Transforming Promotion Dimension...
    dim_promotion = transform_promotion(
        data["promotions"]
    )

    #.Generating Date Dimension...
    dim_date = transform_date()

    logger.info("========== DIMENSION TRANSFORMATION COMPLETED ==========")

    # ======================================================
    # 2.1 VALIDATE DIMENSIONS
    # ======================================================

    dimensions = {
        "customer": dim_customer,
        "employee": dim_employee,
        "store": dim_store,
        "supplier": dim_supplier,
        "product": dim_product,
        "promotion": dim_promotion,
        "date": dim_date,
    }

    validate_all_dimensions(dimensions)

    # ======================================================
    # 3. MERGE SALES HEADER + DETAIL
    # ======================================================

    
    #.Merging Sales Header and Sales Detail...
    

    fact = merge_header_detail(
        data["sales_header"],
        data["sales_detail"]
    )

    

    # ======================================================
    # 4. LOOKUP SURROGATE KEYS
    # ======================================================

    #.Looking up surrogate keys...

    fact = lookup_dimension_keys(
        fact,
        dim_customer,
        dim_employee,
        dim_store,
        dim_product,
        dim_promotion,
        dim_date
    )

    #.Surrogate key lookup completed.

    # ======================================================
    # 5. BUILD FACT SALES
    # ======================================================

    #.Building Fact Sales...

    fact_sales = build_fact_sales(fact)

    #.Fact Sales built.


    # ======================================================
    # 6. FACT SALES DATA QUALITY VALIDATION
    # ======================================================

    logger.info(
        "Validating Fact Sales..."
    )

    validate_fact_sales(
        fact_sales,
        dim_customer,
        dim_employee,
        dim_store,
        dim_product,
        dim_promotion,
        dim_date,
    )

    logger.info(
        "Fact Sales validation completed successfully."
    )
    


    # ======================================================
    # 7. CLEAR EXISTING WAREHOUSE DATA
    # ======================================================

    logger.info(
        "Preparing warehouse for full-refresh load..."
    )

    clear_warehouse()

    # ======================================================
    # 8. LOAD DIMENSIONS
    # ======================================================



    logger.info("========== WAREHOUSE LOAD STARTED ==========")

    load_dataframe(
        dim_customer,
        "dim_customer"
    )

    load_dataframe(
        dim_employee,
        "dim_employee"
    )

    load_dataframe(
        dim_store,
        "dim_store"
    )

    load_dataframe(
        dim_supplier,
        "dim_supplier"
    )

    load_dataframe(
        dim_product,
        "dim_product"
    )

    load_dataframe(
        dim_promotion,
        "dim_promotion"
    )

    load_dataframe(
        dim_date,
        "dim_date"
    )

    # ======================================================
    # 9. LOAD FACT
    # ======================================================


    load_dataframe(
        fact_sales,
        "fact_sales"
    )

    logger.info("========== WAREHOUSE LOAD COMPLETED ==========")



    # ======================================================
    # 10. PIPELINE SUMMARY
    # ======================================================



    end_time = time.perf_counter()
    logger.info("========== ETL PIPELINE COMPLETED ==========")

    print("\n==========================================")
    print("        ETL LOAD SUMMARY")
    print("==========================================")

    print(
        f"dim_customer      : {len(dim_customer):,}"
    )

    print(
        f"dim_employee      : {len(dim_employee):,}"
    )

    print(
        f"dim_store         : {len(dim_store):,}"
    )

    print(
        f"dim_supplier      : {len(dim_supplier):,}"
    )

    print(
        f"dim_product       : {len(dim_product):,}"
    )

    print(
        f"dim_promotion     : {len(dim_promotion):,}"
    )

    print(
        f"dim_date          : {len(dim_date):,}"
    )

    print(
        f"fact_sales        : {len(fact_sales):,}"
    )


    print(
        f"Pipeline Duration : {end_time - start_time:.2f} seconds"
    )

    print("==========================================")
    print("        ETL PIPELINE SUCCESS")
    print("==========================================")


if __name__ == "__main__":
    run_pipeline()