# Product Dimension

## Purpose

Stores product information for analytical reporting.

Implements Slowly Changing Dimension (SCD Type 2) to preserve historical changes to product attributes.

---

## Primary Key

product_key

---

## Business Key

product_id

---

## Columns

| Column               | Description                     |
|----------------------|---------------------------------|
| product_key          | Warehouse surrogate primary key |
| product_id           | Business product identifier     |
| product_name         | Product name                    |
| brand                | Product brand                   |
| category             | Product category                |
| subcategory          | Product subcategory             |
| supplier_id          | Supplier business identifier    |
| standard_cost        | Product acquisition cost        |
| selling_price        | Product selling price           |
| product_status       | Product lifecycle status        |
| effective_start_date | Record effective start date     |
| effective_end_date   | Record effective end date       |
| is_current           | Current record indicator        |
| created_date         | ETL creation timestamp          |
| updated_date         | ETL update timestamp            |

---

## Business Rules

- Product ID is required.
- Product Name is required.
- Product Status must be one of:
  - Active
  - Discontinued
  - Out of Stock
- Selling Price must be greater than or equal to Standard Cost.
- Implements SCD Type 2 for historical tracking.