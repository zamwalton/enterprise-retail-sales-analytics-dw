# Source-to-Target Mapping (STM)

---

## Project Information

| Property | Value |
|----------|--------|
| Project | Enterprise Retail Sales Analytics Data Warehouse |
| Version | 1.0 |
| Author | Zam Walton P M |
| Last Updated | July 2026 |

---

# Purpose

This document defines how data is extracted from operational source systems, transformed according to business rules, and loaded into the PostgreSQL Enterprise Data Warehouse.

It serves as the implementation blueprint for the ETL pipeline.

---

# Source Systems

| Source System  | Description             |
|----------------|-------------------------|
| POS            | Physical store sales    |
| Online Store   | E-commerce transactions |
| CRM            | Customer master         |
| Product Master | Product catalog         |
| Store Master   | Store information       |
| HR             | Employee information    |
| Promotions     | Marketing campaigns     |
| Suppliers      | Supplier information    |
| Inventory      | Inventory levels        |

---

# Target Warehouse

## Fact Tables

- fact_sales
- fact_inventory_snapshot

## Dimension Tables

- dim_customer
- dim_product
- dim_store
- dim_employee
- dim_date
- dim_promotion
- dim_supplier

---

# Transformation Standards

| Rule              | Description                                            |
|-------------------|--------------------------------------------------------|
| Trim whitespace   | Remove leading and trailing spaces                     |
| Standardize text  | Convert names to proper case                           |
| Null handling     | Replace nulls with business defaults where appropriate |
| Date format       | ISO 8601 (YYYY-MM-DD)                                  |
| Numeric precision | Currency rounded to 2 decimal places                   |
| Surrogate keys    | Generated during ETL                                   |
| Business keys     | Preserved from source systems                          |

---

# Business Rules

| Rule ID | Business Rule                              |
|---------|--------------------------------------------|
| BR001   | Sales Amount = Quantity × Unit Price       |
| BR002   | Profit Amount = Sales Amount − Cost Amount |
| BR003   | Discount cannot exceed Sales Amount        |
| BR004   | Quantity Sold must be greater than zero    |
| BR005   | Invalid foreign keys are rejected          |
| BR006   | Duplicate transactions are ignored         |
| BR007   | Customer email addresses must be unique    |

---

# Incremental Loading Strategy

The ETL pipeline uses **High Watermark Loading**.

Each ETL execution records the most recent processed transaction timestamp.

Future executions load only records newer than the stored watermark.

Benefits:

- Faster processing
- Reduced database load
- Scalable ETL execution

---

# Slowly Changing Dimensions (SCD Type 2)

The following dimensions preserve historical changes:

- dim_customer
- dim_product
- dim_store
- dim_employee
- dim_promotion
- dim_supplier

Additional columns:

- effective_start_date
- effective_end_date
- is_current

---

# Mapping - dim_customer

| Source | Source Column | Target Table | Target Column | Transformation |
|--------|---------------|--------------|---------------|----------------|
| CRM    | customer_id   | dim_customer | customer_id   | Direct         |
| CRM    | first_name    | dim_customer | first_name    | Trim           |
| CRM    | last_name     | dim_customer | last_name     | Trim           |
| CRM    | gender        | dim_customer | gender        | Standardize    |
| CRM    | city          | dim_customer | city          | Proper Case    |
| CRM    | state         | dim_customer | state         | Proper Case    |
| CRM    | loyalty_tier  | dim_customer | loyalty_tier  | Direct         |

---

# Mapping - dim_product

| Source  | Source Column | Target Table | Target Column | Transformation |
|---------|---------------|--------------|---------------|----------------|
| Product | product_id    | dim_product  | product_id    | Direct         |
| Product | product_name  | dim_product  | product_name  | Trim           |
| Product | brand         | dim_product  | brand         | Proper Case    |
| Product | category      | dim_product  | category      | Proper Case    |
| Product | supplier_id   | dim_product  | supplier_id   | Lookup         |

---

# Mapping - dim_store

| Source | Source Column | Target Table | Target Column | Transformation |
|--------|---------------|--------------|---------------|----------------|
| Store  | store_id      | dim_store    | store_id      | Direct         |
| Store  | store_name    | dim_store    | store_name    | Trim           |
| Store  | city          | dim_store    | city          | Proper Case    |
| Store  | state         | dim_store    | state         | Proper Case    |
| Store  | region        | dim_store    | region        | Standardize    |

---

# Mapping - dim_employee

| Source | Source Column | Target Table | Target Column | Transformation |
|--------|---------------|--------------|---------------|----------------|
| HR     | employee_id   | dim_employee | employee_id   | Direct         |
| HR     | employee_name | dim_employee | employee_name | Trim           |
| HR     | department    | dim_employee | department    | Proper Case    |
| HR     | job_title     | dim_employee | job_title     | Proper Case    |

---

# Mapping - dim_promotion

| Source     | Source Column       | Target Table  | Target Column       | Transformation |
|------------|---------------------|---------------|---------------------|----------------|
| Promotions | promotion_id        | dim_promotion | promotion_id        | Direct         |
| Promotions | promotion_name      | dim_promotion | promotion_name      | Trim           |
| Promotions | discount_percentage | dim_promotion | discount_percentage | Direct         |

---

# Mapping - dim_supplier

| Source    | Source Column | Target Table | Target Column | Transformation |
|-----------|---------------|--------------|---------------|----------------|
| Suppliers | supplier_id   | dim_supplier | supplier_id   | Direct         |
| Suppliers | supplier_name | dim_supplier | supplier_name | Trim           |
| Suppliers | country       | dim_supplier | country       | Proper Case    |

---

# Mapping - fact_sales

| Source       | Source Column  | Target Column  | Transformation        |
|--------------|----------------|----------------|-----------------------|
| POS / Online | transaction_id | transaction_id | Direct                |
| POS / Online | customer_id    | customer_key   | Lookup                |
| POS / Online | product_id     | product_key    | Lookup                |
| POS / Online | store_id       | store_key      | Lookup                |
| POS / Online | employee_id    | employee_key   | Lookup                |
| POS / Online | promotion_id   | promotion_key  | Lookup                |
| POS / Online | quantity       | quantity_sold  | Direct                |
| POS / Online | unit_price     | unit_price     | Direct                |
| POS / Online | sales_amount   | sales_amount   | Quantity × Unit Price |
| POS / Online | cost_amount    | cost_amount    | Direct                |
| POS / Online | profit_amount  | profit_amount  | Sales − Cost          |

---

# Mapping - fact_inventory_snapshot

| Source    | Source Column  | Target Column  | Transformation |
|-----------|----------------|----------------|----------------|
| Inventory | product_id     | product_key    | Lookup         |
| Inventory | supplier_id    | supplier_key   | Lookup         |
| Inventory | store_id       | store_key      | Lookup         |
| Inventory | current_stock  | current_stock  | Direct         |
| Inventory | reserved_stock | reserved_stock | Direct         |
| Inventory | reorder_level  | reorder_level  | Direct         |

---

# ETL Audit

Every ETL execution records:

- Pipeline Name
- Start Time
- End Time
- Execution Status
- Records Extracted
- Records Loaded
- Records Rejected
- High Watermark Value
- Error Message (if any)

---

# Summary

This Source-to-Target Mapping document defines the data movement, transformation rules, business logic, and loading strategy for the Enterprise Retail Sales Analytics Data Warehouse. It provides the implementation blueprint for the ETL pipeline and ensures consistency across development, testing, and reporting.