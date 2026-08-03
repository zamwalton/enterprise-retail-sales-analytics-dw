"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : sales_header_generator.py
Purpose : Generate POS Sales Header Data
============================================================
"""

import random
from pathlib import Path

import pandas as pd
from faker import Faker

fake = Faker("en_IN")

PAYMENT_METHODS = [
    "UPI",
    "Card",
    "Cash",
    "Wallet"
]

PAYMENT_WEIGHTS = [
    45,
    30,
    15,
    10
]

TRANSACTION_STATUS = [
    "Completed",
    "Cancelled",
    "Returned"
]

TRANSACTION_STATUS_WEIGHTS = [
    95,
    3,
    2
]


def generate_sales_header(num_transactions: int, raw_data_dir: Path):
    """
    Generate POS Sales Header Data.

    Parameters
    ----------
    num_transactions : int
        Number of transactions to generate.

    raw_data_dir : Path
        Path to data/raw directory.

    Returns
    -------
    list[dict]
        Sales header records.
    """

    # ==========================================================
    # Read Master Data
    # ==========================================================

    customers = pd.read_csv(
        raw_data_dir / "crm" / "customers.csv"
    )

    employees = pd.read_csv(
        raw_data_dir / "hr" / "employees.csv"
    )

    promotions = pd.read_csv(
        raw_data_dir / "promotion" / "promotions.csv"
    )

    # ==========================================================
    # Prepare Lookup Lists
    # ==========================================================

    customer_ids = customers["customer_id"].tolist()

    promotion_ids = promotions["promotion_id"].tolist()

    # Keep employee-store relationship
    employee_records = employees[
        ["employee_id", "store_id"]
    ].to_dict("records")

    headers = []

    # ==========================================================
    # Generate Transactions
    # ==========================================================

    for transaction in range(1, num_transactions + 1):

        employee = random.choice(employee_records)

        use_promotion = random.random() < 0.30

        headers.append(
            {
                "transaction_id": f"TXN{transaction:09d}",

                "transaction_date": fake.date_between(
                    start_date="-2y",
                    end_date="today",
                ),

                "customer_id": random.choice(customer_ids),

                # Employee works in one assigned store
                "employee_id": employee["employee_id"],
                "store_id": employee["store_id"],

                "promotion_id": (
                    random.choice(promotion_ids)
                    if use_promotion
                    else None
                ),

                "payment_method": random.choices(
                    PAYMENT_METHODS,
                    weights=PAYMENT_WEIGHTS,
                    k=1,
                )[0],

                "transaction_status": random.choices(
                    TRANSACTION_STATUS,
                    weights=TRANSACTION_STATUS_WEIGHTS,
                    k=1,
                )[0],
            }
        )

    return headers