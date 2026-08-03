"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : crm_generator.py
Purpose : Generate CRM Customer Source Data
============================================================
"""

import random

from faker import Faker

fake = Faker("en_IN")


def generate_customers(num_customers: int):
    """
    Generate customer master records.

    Returns
    -------
    list[dict]
    """

    customers = []

    genders = ["Male", "Female"]

    for customer_id in range(1, num_customers + 1):

        customers.append(
            {
                "customer_id": f"CUST{customer_id:05d}",
                "customer_name": fake.name(),
                "gender": random.choice(genders),
                "email": fake.email(),
                "phone": fake.msisdn()[:10],
                "city": fake.city(),
                "state": fake.state(),
                "country": "India",
                "registration_date": fake.date_between(
                    start_date="-5y",
                    end_date="today"
                ),
            }
        )

    return customers