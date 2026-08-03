from etl.extract.extract import extract_data

from etl.transform.customer import transform_customer
from etl.transform.employee import transform_employee
from etl.transform.store import transform_store
from etl.transform.product import transform_product
from etl.transform.promotion import transform_promotion
from etl.transform.date import transform_date

from etl.transform.fact.merge_header_detail import merge_header_detail
from etl.transform.fact.lookup_keys import lookup_dimension_keys


def main():

    data = extract_data()

    dim_customer = transform_customer(data["customers"])
    dim_employee = transform_employee(data["employees"])
    dim_store = transform_store(data["stores"])
    dim_product = transform_product(data["products"])
    dim_promotion = transform_promotion(data["promotions"])
    dim_date = transform_date()

    fact = merge_header_detail(
        data["sales_header"],
        data["sales_detail"],
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

    print("\n")
    print(fact.head())

    print("\n")
    print(fact.columns)


if __name__ == "__main__":
    main()