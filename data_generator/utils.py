"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : utils.py
Purpose : Common utility functions for data generation
============================================================
"""

from pathlib import Path


def ensure_directory(directory: Path) -> None:
    """
    Create a directory if it does not already exist.

    Parameters
    ----------
    directory : Path
        Directory path.
    """
    directory.mkdir(parents=True, exist_ok=True)


def print_generation_summary(dataset_name: str, row_count: int, output_file: Path) -> None:
    """
    Print dataset generation summary.

    Parameters
    ----------
    dataset_name : str
        Dataset name.
    row_count : int
        Number of rows generated.
    output_file : Path
        Output CSV path.
    """

    print("=" * 60)
    print(f"{dataset_name} Generation Completed")
    print("=" * 60)
    print(f"Rows Generated : {row_count:,}")
    print(f"Output File    : {output_file}")
    print("=" * 60)