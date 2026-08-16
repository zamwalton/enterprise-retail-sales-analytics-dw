"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : pipeline.py
Purpose : Incremental ETL Pipeline
============================================================
"""

from etl.utils import logger

from etl.extract.extract import extract_data

from etl.transform.customer import transform_customer
from etl.transform.employee import transform_employee
from etl.transform.store import transform_store
from etl.transform.product import transform_product
from etl.transform.promotion import transform_promotion
from etl.transform.date import transform_date

from etl.incremental.extract_incremental import (
    extract_incremental_sales,
    extract_incremental_details,
)

from etl.transform.fact.merge_header_detail import (
    merge_header_detail,
)

from etl.transform.fact.lookup_keys import (
    lookup_dimension_keys,
)

from etl.transform.fact.fact_sales import (
    build_fact_sales,
)

from etl.validation.validate_fact_sales import (
    validate_fact_sales,
)

from etl.incremental.load_incremental import (
    load_incremental_fact_sales,
)

from etl.incremental.watermark import (
    get_latest_watermark,
    update_watermark,
)


def run_incremental_pipeline():

    logger.info(
        "======================================================="
    )

    logger.info(
        "        INCREMENTAL ETL PIPELINE STARTED"
    )

    logger.info(
        "======================================================="
    )

    # ======================================================
    # 1. EXTRACT SOURCE DATA
    # ======================================================

    logger.info(
        "Loading source datasets..."
    )

    data = extract_data()

    # ======================================================
    # 2. TRANSFORM DIMENSIONS
    # ======================================================

    logger.info(
        "Transforming dimensions..."
    )

    dim_customer = transform_customer(
        data["customers"]
    )

    dim_employee = transform_employee(
        data["employees"]
    )

    dim_store = transform_store(
        data["stores"]
    )

    dim_product = transform_product(
        data["products"]
    )

    dim_promotion = transform_promotion(
        data["promotions"]
    )

    dim_date = transform_date()

    # ======================================================
    # 3. INCREMENTAL SALES HEADER
    # ======================================================

    sales_header = extract_incremental_sales()
    if sales_header.empty:

        logger.info(
            "No new incremental sales records found. "
            "Pipeline completed successfully."
        )

        logger.info(
            "======================================================="
        )

        logger.info(
            "        INCREMENTAL ETL PIPELINE COMPLETED"
        )

        logger.info(
            "Rows inserted: 0"
        )

        logger.info(
            "======================================================="
        )

        return 0

    # ======================================================
    # 4. INCREMENTAL SALES DETAIL
    # ======================================================

    sales_detail = extract_incremental_details(
        sales_header
    )

    # ======================================================
    # 5. MERGE HEADER + DETAIL
    # ======================================================

    fact = merge_header_detail(
        sales_header,
        sales_detail,
    )

    # ======================================================
    # 6. LOOKUP DIMENSION KEYS
    # ======================================================

    fact = lookup_dimension_keys(
        fact,
        dim_customer,
        dim_employee,
        dim_store,
        dim_product,
        dim_promotion,
        dim_date,
    )

    # ======================================================
    # 7. BUILD FACT SALES
    # ======================================================

    fact_sales = build_fact_sales(
        fact
    )

    # ======================================================
    # 8. VALIDATE FACT SALES
    # ======================================================

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
        "Incremental Fact Sales validation passed."
    )

    # ======================================================
    # 9. LOAD NEW FACT RECORDS
    # ======================================================

    inserted_rows = load_incremental_fact_sales(
        fact_sales
    )

    # ======================================================
    # 10. UPDATE WATERMARK
    # ======================================================

    if not sales_header.empty:

        latest_date, latest_id = get_latest_watermark(
            sales_header
        )

        update_watermark(
            watermark_date=latest_date,
            watermark_id=latest_id,
        )

        logger.info(
            "Incremental watermark advanced successfully."
        )

    else:

        logger.info(
            "No new fact rows inserted. "
            "Watermark unchanged."
        )

    # ======================================================
    # 11. SUMMARY
    # ======================================================

    logger.info(
        "======================================================="
    )

    logger.info(
        "        INCREMENTAL ETL PIPELINE COMPLETED"
    )

    logger.info(
        "Rows inserted: %s",
        f"{inserted_rows:,}",
    )

    logger.info(
        "======================================================="
    )

    return inserted_rows


if __name__ == "__main__":
    run_incremental_pipeline()