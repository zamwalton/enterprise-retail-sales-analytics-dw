"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : promotion_generator.py
Purpose : Generate Promotion Master Data
============================================================
"""

import random
from datetime import timedelta
from faker import Faker

fake = Faker("en_IN")

PROMOTION_TYPES = [
    "Percentage",
    "Fixed Amount",
    "Buy One Get One",
]

PROMOTION_STATUS = [
    "Scheduled",
    "Active",
    "Expired",
]


def generate_promotions(num_promotions: int):

    promotions = []

    for promotion_id in range(1, num_promotions + 1):

        start_date = fake.date_between(
            start_date="-2y",
            end_date="+6m"
        )

        end_date = start_date + timedelta(
            days=random.randint(7, 60)
        )

        promotion_type = random.choice(PROMOTION_TYPES)

        if promotion_type == "Percentage":
            discount = random.choice(
                [5, 10, 15, 20, 25, 30, 40, 50]
            )
        elif promotion_type == "Fixed Amount":
            discount = random.choice(
                [100, 250, 500, 1000]
            )
        else:
            discount = 0

        promotions.append(
            {
                "promotion_id": f"PROMO{promotion_id:03d}",
                "promotion_name": f"Campaign {promotion_id}",
                "promotion_type": promotion_type,
                "discount_value": discount,
                "start_date": start_date,
                "end_date": end_date,
                "promotion_status": random.choice(
                    PROMOTION_STATUS
                ),
            }
        )

    return promotions