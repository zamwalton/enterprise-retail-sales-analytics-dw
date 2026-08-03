from etl.extract.extract import extract_data

from etl.transform.fact.merge_header_detail import (
    merge_header_detail,
)


def main():

    data = extract_data()

    fact = merge_header_detail(
        data["sales_header"],
        data["sales_detail"],
    )

    print()

    print(fact.head())

    print()

    print(fact.columns)


if __name__ == "__main__":
    main()