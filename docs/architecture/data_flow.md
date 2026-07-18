# Data Flow

---

## Project Information

| Property     | Value                                            |
|--------------|--------------------------------------------------|
| Project      | Enterprise Retail Sales Analytics Data Warehouse |
| Version      | 1.0                                              |
| Author       | Zam Walton P M                                   |
| Last Updated | July 2026                                        |

---

# Overview

The Enterprise Retail Sales Analytics Data Warehouse follows a layered data flow architecture. Data is extracted from multiple operational systems, validated, standardized, transformed into a dimensional model, and loaded into a PostgreSQL Data Warehouse. Business users consume the curated data through SQL queries and Power BI dashboards.

---

# End-to-End Data Flow

```text
                Operational Source Systems
 ┌─────────────────────────────────────────────────────┐
 │ POS │ Online │ CRM │ Product │ HR │ Inventory │ ... │
 └─────────────────────────────────────────────────────┘
                        │
                        ▼
                 Extract Layer (Python)
                        │
                        ▼
              Validation & Quality Checks
                        │
                        ▼
                  Staging Layer (CSV)
                        │
                        ▼
              Transformation Layer (Pandas)
                        │
                        ▼
      Incremental Load & SCD Type 2 Processing
                        │
                        ▼
          PostgreSQL Enterprise Data Warehouse
                        │
            ┌───────────┴───────────┐
            ▼                       ▼
      SQL Analytics          Power BI Dashboards
                        │
                        ▼
                  Business Users
```

---

# Data Flow Stages

## 1. Extract

Read data from all operational source systems.

### Sources

- POS
- Online Store
- CRM
- Product Master
- Store Master
- HR
- Inventory
- Promotions
- Suppliers

---

## 2. Validation

Perform data quality checks before transformation.

Examples:

- Required fields
- Duplicate records
- Invalid dates
- Negative quantities
- Invalid foreign keys
- Invalid prices

Invalid records will be logged for investigation.

---

## 3. Staging

Store validated data in a standardized format before business transformations.

Purpose:

- Simplify debugging
- Preserve raw extracts
- Support incremental processing

---

## 4. Transformation

Apply business logic including:

- Data cleansing
- Standardization
- Derived columns
- Business calculations
- Surrogate key lookups
- Dimension building
- Fact table creation

---

## 5. Incremental Processing

Only new or modified records are processed.

Benefits:

- Faster ETL execution
- Reduced database load
- Improved scalability

---

## 6. SCD Type 2 Processing

Historical changes to selected dimensions are preserved by:

- Closing existing records
- Creating new current records
- Updating effective dates

Applicable dimensions:

- Customer
- Product
- Store
- Employee
- Promotion
- Supplier

---

## 7. Warehouse Loading

Load transformed data into:

### Fact Tables

- fact_sales
- fact_inventory_snapshot

### Dimension Tables

- dim_customer
- dim_product
- dim_store
- dim_employee
- dim_date
- dim_promotion
- dim_supplier

---

## 8. Reporting

The warehouse supports:

- SQL analytics
- Reporting views
- Power BI dashboards
- Executive reporting

---

# Logging & Auditing

Each ETL execution captures:

- Pipeline start time
- Pipeline end time
- Execution status
- Records extracted
- Records loaded
- Records rejected
- Execution duration

This information supports monitoring and troubleshooting.

---

# Error Handling

The ETL process will:

- Log validation failures
- Continue processing valid records where appropriate
- Record detailed error messages
- Generate execution summaries

---

# Future Enhancements

Future improvements include:

- Apache Airflow scheduling
- Docker deployment
- Cloud storage integration
- Real-time streaming
- Metadata-driven ETL
- Automated monitoring and alerts

---

# Summary

The layered data flow architecture separates extraction, validation, transformation, loading, and reporting responsibilities. This modular design improves maintainability, scalability, and reliability while following enterprise Data Engineering best practices.