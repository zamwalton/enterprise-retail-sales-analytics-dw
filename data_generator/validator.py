"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : validator.py
Purpose : Data validation utilities
============================================================
"""

import pandas as pd


def validate_dataframe(df: pd.DataFrame, dataset_name: str) -> None:
    """
    Perform basic validation checks.
    """

    print(f"\nValidating {dataset_name}...")

    print(f"Rows    : {len(df):,}")
    print(f"Columns : {len(df.columns)}")

    if df.isnull().sum().sum() == 0:
        print("Missing Values : None")
    else:
        print(df.isnull().sum())

    print("Validation Completed.\n")