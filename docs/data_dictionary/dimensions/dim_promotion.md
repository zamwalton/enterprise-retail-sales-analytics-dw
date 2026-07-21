# Promotion Dimension

## Purpose

Stores promotion and marketing campaign information for analytical reporting.

Implements Slowly Changing Dimension (SCD Type 2) to preserve historical changes to promotion attributes.

---

## Primary Key

promotion_key

---

## Business Key

promotion_id

---

## Columns

| Column               | Description                     |
|----------------------|---------------------------------|
| promotion_key        | Warehouse surrogate primary key |
| promotion_id         | Business promotion identifier   |
| promotion_name       | Promotion or campaign name      |
| promotion_type       | Discount type                   |
| discount_percentage  | Discount percentage             |
| start_date           | Promotion start date            |
| end_date             | Promotion end date              |
| promotion_status     | Active, Expired, Scheduled      |
| effective_start_date | Record effective start date     |
| effective_end_date   | Record effective end date       |
| is_current           | Current record indicator        |
| created_date         | ETL creation timestamp          |
| updated_date         | ETL update timestamp            |

---

## Business Rules

- Promotion ID is required.
- Promotion Name is required.
- Promotion Type must be one of:
  - Percentage
  - Fixed Amount
  - Buy One Get One
- Discount Percentage must be between 0 and 100.
- Promotion Status must be one of:
  - Active
  - Scheduled
  - Expired
- End Date must be greater than or equal to Start Date.
- Implements SCD Type 2.