"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : supplier_generator.py
Purpose : Generate Supplier Master Data
============================================================
"""

import random
from faker import Faker

fake = Faker("en_IN")

SUPPLIER_CATEGORIES = [
    "Local",
    "National",
    "International"
]

SUPPLIER_STATUS = [
    "Active",
    "Inactive"
]


def generate_suppliers(num_suppliers: int):

    suppliers = []

    for supplier_id in range(1, num_suppliers + 1):

        suppliers.append(
            {
                "supplier_id": f"SUP{supplier_id:03d}",
                "supplier_name": fake.company(),
                "supplier_category": random.choice(SUPPLIER_CATEGORIES),
                "contact_name": fake.name(),
                "phone": fake.msisdn()[:10],
                "email": fake.company_email(),
                "city": fake.city(),
                "state": fake.state(),
                "country": "India",
                "supplier_status": random.choices(
                    SUPPLIER_STATUS,
                    weights=[95, 5],
                    k=1,
                )[0],
            }
        )

    return suppliers