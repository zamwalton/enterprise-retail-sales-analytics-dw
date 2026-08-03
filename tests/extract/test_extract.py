from etl.extract.extract import extract_data


def main():

    data = extract_data()

    print("\nAvailable datasets\n")

    for dataset in data:
        print(dataset)


if __name__ == "__main__":
    main()