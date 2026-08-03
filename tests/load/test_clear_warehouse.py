"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : test_clear_warehouse.py
Purpose : Test warehouse cleanup
============================================================
"""

from etl.load.clear_warehouse import clear_warehouse
from etl.load.validate_load import get_table_row_count


def test_clear_warehouse():

    clear_warehouse()

    tables = [
        "dim_customer",
        "dim_employee",
        "dim_store",
        "dim_supplier",
        "dim_product",
        "dim_promotion",
        "dim_date",
        "fact_sales",
    ]

    for table in tables:

        count = get_table_row_count(table)

        assert count == 0