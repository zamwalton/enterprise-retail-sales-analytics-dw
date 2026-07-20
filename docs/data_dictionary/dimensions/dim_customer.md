# Customer Dimension

## Purpose

Stores customer information for analytical reporting.

Implements Slowly Changing Dimension (SCD Type 2) to preserve historical customer changes.

---

## Primary Key

customer_key

---

## Business Key

customer_id

---

## Columns

| Column               | Description                  |
|----------------------|------------------------------|
| customer_key         | Surrogate primary key        |
| customer_id          | Business customer identifier |
| customer_name        | Customer full name           |
| gender               | Gender                       |
| date_of_birth        | Date of birth                |
| email                | Email address                |
| phone                | Contact number               |
| city                 | Customer city                |
| state                | Customer state               |
| country              | Customer country             |
| loyalty_tier         | Loyalty membership level     |
| effective_start_date | Record effective start date  |
| effective_end_date   | Record effective end date    |
| is_current           | Current record indicator     |
| created_date         | ETL creation timestamp       |
| updated_date         | ETL update timestamp         |