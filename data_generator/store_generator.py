"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : store_generator.py
Purpose : Generate Store Master Data
============================================================
"""

import random

STORE_TYPES = [
    "Hypermarket",
    "Supermarket",
    "Express",
]

CITIES = [
    ("Chennai", "Tamil Nadu"),
    ("Bengaluru", "Karnataka"),
    ("Hyderabad", "Telangana"),
    ("Mumbai", "Maharashtra"),
    ("Pune", "Maharashtra"),
    ("Kochi", "Kerala"),
    ("Coimbatore", "Tamil Nadu"),
    ("Mysuru", "Karnataka"),
    ("Visakhapatnam", "Andhra Pradesh"),
    ("Thiruvananthapuram", "Kerala"),
]


def generate_stores(num_stores: int):

    stores = []

    for store_id in range(1, num_stores + 1):

        city, state = random.choice(CITIES)

        stores.append(
            {
                "store_id": f"STORE{store_id:03d}",
                "store_name": f"{city} Store {store_id}",
                "store_type": random.choice(STORE_TYPES),
                "city": city,
                "state": state,
                "country": "India",
                "opening_date": f"{random.randint(2010,2024)}-01-01",
                "store_status": "Active",
            }
        )

    return stores