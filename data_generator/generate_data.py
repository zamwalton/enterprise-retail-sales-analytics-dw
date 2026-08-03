"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : generate_data.py
Purpose : Generate all enterprise source system datasets
============================================================
"""

import pandas as pd

from data_generator.config import (
    CRM_DIR,
    HR_DIR,
    NUM_CUSTOMERS,
    NUM_EMPLOYEES,
    NUM_STORES,
    STORE_DIR,
    NUM_STORES,
    SUPPLIER_DIR,
    NUM_SUPPLIERS,
    PRODUCT_DIR,
    NUM_PRODUCTS,
    NUM_SUPPLIERS,
    PROMOTION_DIR,
    NUM_PROMOTIONS,
    POS_DIR,
    RAW_DATA_DIR,
    NUM_SALES_TRANSACTIONS,
)

from data_generator.crm_generator import generate_customers
from data_generator.hr_generator import generate_employees
from data_generator.store_generator import generate_stores
from data_generator.supplier_generator import generate_suppliers
from data_generator.product_generator import generate_products
from data_generator.promotion_generator import generate_promotions
from data_generator.sales_header_generator import generate_sales_header
from data_generator.sales_detail_generator import generate_sales_detail 

from data_generator.utils import (
    ensure_directory,
    print_generation_summary,
)

from data_generator.validator import validate_dataframe


# ==========================================================
# CRM DATA GENERATION
# ==========================================================

def generate_crm():
    """Generate CRM customer data."""

    ensure_directory(CRM_DIR)

    customers = generate_customers(NUM_CUSTOMERS)

    df = pd.DataFrame(customers)

    validate_dataframe(df, "CRM Customers")

    output_file = CRM_DIR / "customers.csv"

    df.to_csv(output_file, index=False)

    print_generation_summary(
        "CRM Customers",
        len(df),
        output_file,
    )


# ==========================================================
# HR DATA GENERATION
# ==========================================================

def generate_hr():
    """Generate HR employee data."""

    ensure_directory(HR_DIR)

    employees = generate_employees(NUM_EMPLOYEES, NUM_STORES)

    df = pd.DataFrame(employees)

    validate_dataframe(df, "HR Employees")

    output_file = HR_DIR / "employees.csv"

    df.to_csv(output_file, index=False)

    print_generation_summary(
        "HR Employees",
        len(df),
        output_file,
    )








# ==========================================================
# STORE DATA GENERATION
# ==========================================================

def generate_store():

    ensure_directory(STORE_DIR)

    stores = generate_stores(NUM_STORES)

    df = pd.DataFrame(stores)

    validate_dataframe(df, "Store Master")

    output_file = STORE_DIR / "stores.csv"

    df.to_csv(output_file, index=False)

    print_generation_summary(
        "Store Master",
        len(df),
        output_file,
    )


# ==========================================================
# SUPPLIER DATA GENERATION
# ==========================================================

def generate_supplier():

    ensure_directory(SUPPLIER_DIR)

    suppliers = generate_suppliers(NUM_SUPPLIERS)

    df = pd.DataFrame(suppliers)

    validate_dataframe(df, "Supplier Master")

    output_file = SUPPLIER_DIR / "suppliers.csv"

    df.to_csv(output_file, index=False)

    print_generation_summary(
        "Supplier Master",
        len(df),
        output_file,
    )


#=========================================================
# PRODUCT DATA GENERATION
#=========================================================

def generate_product():

    ensure_directory(PRODUCT_DIR)

    products = generate_products(
        NUM_PRODUCTS,
        NUM_SUPPLIERS,
    )

    df = pd.DataFrame(products)

    validate_dataframe(df, "Product Master")

    output_file = PRODUCT_DIR / "products.csv"

    df.to_csv(output_file, index=False)

    print_generation_summary(
        "Product Master",
        len(df),
        output_file,
    )

# ==========================================================
# PROMOTION DATA GENERATION
# ==========================================================

def generate_promotion():

    ensure_directory(PROMOTION_DIR)

    promotions = generate_promotions(
        NUM_PROMOTIONS
    )

    df = pd.DataFrame(promotions)

    validate_dataframe(
        df,
        "Promotion Master"
    )

    output_file = PROMOTION_DIR / "promotions.csv"

    df.to_csv(output_file, index=False)

    print_generation_summary(
        "Promotion Master",
        len(df),
        output_file,
    )


#=========================================================
# SALES HEADER DATA GENERATION
#=========================================================

def generate_pos_header():

    ensure_directory(POS_DIR)

    headers = generate_sales_header(
        NUM_SALES_TRANSACTIONS,
        RAW_DATA_DIR,
    )

    df = pd.DataFrame(headers)

    validate_dataframe(
        df,
        "POS Sales Header"
    )

    output_file = POS_DIR / "sales_header.csv"

    df.to_csv(output_file, index=False)

    print_generation_summary(
        "POS Sales Header",
        len(df),
        output_file,
    )

#=========================================================
# SALES DETAIL DATA GENERATION
#=========================================================

def generate_pos_detail():

    details = generate_sales_detail(
        RAW_DATA_DIR
    )

    df = pd.DataFrame(details)

    validate_dataframe(
        df,
        "POS Sales Detail"
    )

    output_file = POS_DIR / "sales_detail.csv"

    df.to_csv(output_file, index=False)

    print_generation_summary(
        "POS Sales Detail",
        len(df),
        output_file,
    )


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("\n" + "=" * 60)
    print("Generating Enterprise Source System Data")
    print("=" * 60)

    generate_crm()

    generate_hr()

    generate_store()

    generate_supplier()

    generate_product()

    generate_promotion()

    #pos header and detail generation should be done after all master data is generated
    
    generate_pos_header()

    generate_pos_detail()

    print("\n" + "=" * 60)
    print("All datasets generated successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()