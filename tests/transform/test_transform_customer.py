from etl.extract.extract import extract_data
from etl.transform.customer import transform_customer


def main():

    data = extract_data()

    dim_customer = transform_customer(
        data["customers"]
    )

    print()

    print(dim_customer.head())

    print()

    print(dim_customer.columns)


if __name__ == "__main__":
    main()