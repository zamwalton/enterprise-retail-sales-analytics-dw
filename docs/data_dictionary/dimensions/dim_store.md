# Store Dimension

## Purpose

Stores retail store information for analytical reporting.

Implements Slowly Changing Dimension (SCD Type 2) to preserve historical changes to store attributes.

---

## Primary Key

store_key

---

## Business Key

store_id

---

## Columns

| Column               | Description                     |
|----------------------|---------------------------------|
| store_key            | Warehouse surrogate primary key |
| store_id             | Business store identifier       |
| store_name           | Store name                      |
| store_type           | Retail, Outlet, Warehouse       |
| city                 | Store city                      |
| state                | Store state                     |
| country              | Store country                   |
| opening_date         | Store opening date              |
| store_status         | Active or Closed                |
| effective_start_date | Record effective start date     |
| effective_end_date   | Record effective end date       |
| is_current           | Current record indicator        |
| created_date         | ETL creation timestamp          |
| updated_date         | ETL update timestamp            |

---

## Business Rules

- Store ID is required.
- Store Name is required.
- Store Type must be one of:
  - Retail
  - Outlet
  - Warehouse
- Store Status must be:
  - Active
  - Closed
- Implements SCD Type 2 for historical tracking.