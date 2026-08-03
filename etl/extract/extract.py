"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : extract.py
Purpose : Extract source data from CSV files
============================================================
"""

import pandas as pd

from data_generator.config import (
    CRM_DIR,
    HR_DIR,
    STORE_DIR,
    SUPPLIER_DIR,
    PRODUCT_DIR,
    PROMOTION_DIR,
    POS_DIR,
)


def extract_data():
    """
    Extract all source datasets.

    Returns
    -------
    dict
        Dictionary containing all source DataFrames.
    """

   

    data = {

        "customers": pd.read_csv(CRM_DIR / "customers.csv"),

        "employees": pd.read_csv(HR_DIR / "employees.csv"),

        "stores": pd.read_csv(STORE_DIR / "stores.csv"),

        "suppliers": pd.read_csv(SUPPLIER_DIR / "suppliers.csv"),

        "products": pd.read_csv(PRODUCT_DIR / "products.csv"),

        "promotions": pd.read_csv(PROMOTION_DIR / "promotions.csv"),

        "sales_header": pd.read_csv(POS_DIR / "sales_header.csv"),

        "sales_detail": pd.read_csv(POS_DIR / "sales_detail.csv"),
    }

    \

    for name, df in data.items():
        print(f"{name:<15}: {len(df):,} rows")

    return data