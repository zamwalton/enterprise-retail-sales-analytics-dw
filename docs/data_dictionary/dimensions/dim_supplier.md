# Supplier Dimension

## Purpose

Stores supplier information for analytical reporting.

Implements Slowly Changing Dimension (SCD Type 2) to preserve historical changes to supplier attributes.

---

## Primary Key

supplier_key

---

## Business Key

supplier_id

---

## Columns

| Column               | Description                     |
|----------------------|---------------------------------|
| supplier_key         | Warehouse surrogate primary key |
| supplier_id          | Business supplier identifier    |
| supplier_name        | Supplier company name           |
| supplier_category    | Local, National, International  |
| contact_name         | Primary contact person          |
| phone                | Contact phone number            |
| email                | Contact email address           |
| city                 | Supplier city                   |
| state                | Supplier state                  |
| country              | Supplier country                |
| supplier_status      | Active, Inactive                |
| effective_start_date | Record effective start date     |
| effective_end_date   | Record effective end date       |
| is_current           | Current record indicator        |
| created_date         | ETL creation timestamp          |
| updated_date         | ETL update timestamp            |

---

## Business Rules

- Supplier ID is required.
- Supplier Name is required.
- Supplier Category must be one of:
  - Local
  - National
  - International
- Supplier Status must be:
  - Active
  - Inactive
- Implements SCD Type 2.