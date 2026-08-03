"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : product_generator.py
Purpose : Generate Product Master Data
============================================================
"""

import random
from faker import Faker

fake = Faker("en_IN")

PRODUCT_CATEGORIES = [
    "Electronics",
    "Groceries",
    "Clothing",
    "Home & Kitchen",
    "Beauty",
    "Sports",
]

BRANDS = [
    "Samsung",
    "LG",
    "Nike",
    "Adidas",
    "Puma",
    "Sony",
    "Philips",
    "Nestle",
    "Amul",
    "Dove",
]

PRODUCT_STATUS = [
    "Active",
    "Discontinued"
]


def generate_products(num_products: int, num_suppliers: int):

    products = []

    for product_id in range(1, num_products + 1):

        category = random.choice(PRODUCT_CATEGORIES)

        cost_price = round(random.uniform(50, 5000), 2)

        selling_price = round(
            cost_price * random.uniform(1.10, 1.60),
            2
        )

        products.append(
            {
                "product_id": f"PROD{product_id:05d}",
                "product_name": fake.word().title() + " " + category,
                "category": category,
                "brand": random.choice(BRANDS),

                # Relationship
                "supplier_id": f"SUP{random.randint(1, num_suppliers):03d}",

                "cost_price": cost_price,
                "selling_price": selling_price,

                "product_status": random.choices(
                    PRODUCT_STATUS,
                    weights=[95, 5],
                    k=1
                )[0],
            }
        )

    return products