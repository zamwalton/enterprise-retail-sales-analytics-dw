"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : sales_detail_generator.py
Purpose : Generate POS Sales Detail Data
============================================================
"""

import random
from pathlib import Path

import pandas as pd

# Weighted basket size
ITEMS_PER_TRANSACTION = [1, 2, 3, 4, 5]
ITEM_WEIGHTS = [35, 30, 20, 10, 5]

GST_RATE = 0.18


def generate_sales_detail(raw_data_dir: Path):

    """
    Generate sales line items.
    """

    # ==========================================================
    # Read Sales Header
    # ==========================================================

    headers = pd.read_csv(
        raw_data_dir / "pos" / "sales_header.csv"
    )

    # ==========================================================
    # Read Product Master
    # ==========================================================

    products = pd.read_csv(
        raw_data_dir / "product" / "products.csv"
    )

    product_records = products[
        [
            "product_id",
            "selling_price"
        ]
    ].to_dict("records")

    details = []

    # ==========================================================
    # Generate Line Items
    # ==========================================================

    for _, header in headers.iterrows():

        basket_size = random.choices(
            ITEMS_PER_TRANSACTION,
            weights=ITEM_WEIGHTS,
            k=1
        )[0]

        selected_products = random.sample(
            product_records,
            basket_size
        )

        line_number = 1

        for product in selected_products:

            quantity = random.randint(1, 5)

            unit_price = float(product["selling_price"])

            subtotal = quantity * unit_price

            discount = round(
                subtotal * random.uniform(0, 0.20),
                2
            )

            taxable_amount = subtotal - discount

            tax = round(
                taxable_amount * GST_RATE,
                2
            )

            total = round(
                taxable_amount + tax,
                2
            )

            details.append(
                {
                    "transaction_id": header["transaction_id"],
                    "line_number": line_number,
                    "product_id": product["product_id"],
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "discount_amount": discount,
                    "tax_amount": tax,
                    "total_amount": total,
                }
            )

            line_number += 1

    return details