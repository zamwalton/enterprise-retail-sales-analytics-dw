from etl.extract.extract import extract_data

from etl.transform.customer import transform_customer
from etl.transform.employee import transform_employee
from etl.transform.store import transform_store
from etl.transform.supplier import transform_supplier
from etl.transform.product import transform_product
from etl.transform.promotion import transform_promotion
from etl.transform.date import transform_date

def main():

    data = extract_data()

    dim_customer = transform_customer(data["customers"])
    dim_employee = transform_employee(data["employees"])
    dim_store = transform_store(data["stores"])
    dim_supplier = transform_supplier(data["suppliers"])
    dim_product = transform_product(data["products"])
    dim_promotion = transform_promotion(data["promotions"])
    dim_date = transform_date()
    print("\n========== Dimension Summary ==========\n")

    print(f"Customer  : {len(dim_customer):,}")
    print(f"Employee  : {len(dim_employee):,}")
    print(f"Store     : {len(dim_store):,}")
    print(f"Supplier  : {len(dim_supplier):,}")
    print(f"Product   : {len(dim_product):,}")
    print(f"Promotion : {len(dim_promotion):,}")
    print(f"Date      : {len(dim_date):,}")
    

if __name__ == "__main__":
    main()