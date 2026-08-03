from etl.extract.extract import extract_data
from etl.transform.employee import transform_employee


def main():

    data = extract_data()

    dim_employee = transform_employee(
        data["employees"]
    )

    print()

    print(dim_employee.head())

    print()

    print(dim_employee.columns)


if __name__ == "__main__":
    main()