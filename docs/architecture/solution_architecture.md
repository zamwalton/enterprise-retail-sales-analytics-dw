# Solution Architecture

---

## Project Information

| Property | Value |
|----------|--------|
| Project | Enterprise Retail Sales Analytics Data Warehouse |
| Version | 1.0 |
| Author | Zam Walton P M |
| Last Updated | July 2026 |

---

# 1. Project Overview

The Enterprise Retail Sales Analytics Data Warehouse is a production-style Data Engineering project designed to simulate a real-world enterprise retail environment. The project integrates data from multiple operational systems into a centralized PostgreSQL Data Warehouse using a modular Python ETL framework.

The primary objective is to provide reliable, scalable, and analytics-ready data for business intelligence and executive reporting through Power BI dashboards.

---

# 2. Business Problem

Retail organizations generate data from multiple operational systems, including:

- Point of Sale (POS)
- Online Store
- Customer Relationship Management (CRM)
- Product Management
- Human Resources (HR)
- Inventory Management
- Supplier Management
- Promotion Management

These systems are optimized for day-to-day business operations but are not designed for analytical reporting. As data grows, reporting directly from operational databases becomes slow, inconsistent, and difficult to maintain.

The organization requires a centralized Enterprise Data Warehouse that consolidates data from all source systems and provides accurate, consistent, and high-performance reporting for business users.

---

# 3. Solution Overview

The solution uses a modular ETL architecture that extracts data from multiple operational source systems, validates and transforms the data according to business rules, and loads it into a PostgreSQL Star Schema Data Warehouse.

The warehouse serves as the single source of truth for reporting and analytics.

Key features include:

- Modular Python ETL Pipeline
- Incremental Data Loading
- High Watermark Processing
- Slowly Changing Dimensions (SCD Type 2)
- Data Validation Framework
- Production Logging
- SQL Analytics
- Reporting Views
- Power BI Dashboards
- Docker Deployment
- Apache Airflow Orchestration

---

# 4. Enterprise Solution Architecture

```text
                     Enterprise Retail Company

      ┌────────────────────────────────────────────┐
      │           Operational Source Systems       │
      │--------------------------------------------│
      │ POS │ Online │ CRM │ HR │ Inventory        │
      │ Product │ Supplier │ Promotion │ Store     │
      └────────────────────────────────────────────┘
                          │
                          ▼
             ┌─────────────────────────────┐
             │      Python ETL Pipeline    │
             │-----------------------------│
             │ Extract                     │
             │ Validation                  │
             │ Staging                     │
             │ Transformation              │
             │ Incremental Loading         │
             │ SCD Type 2                  │
             │ Load                        │
             │ Audit Logging               │
             └─────────────────────────────┘
                          │
                          ▼
             ┌─────────────────────────────┐
             │ PostgreSQL Data Warehouse   │
             │-----------------------------│
             │ Fact Tables                 │
             │ Dimension Tables            │
             │ Reporting Views             │
             └─────────────────────────────┘
                          │
               ┌──────────┴──────────┐
               ▼                     ▼
        SQL Analytics        Power BI Dashboards
                          │
                          ▼
                    Business Users
```

---

# 5. Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | ETL development and orchestration |
| Pandas | Data extraction and transformation |
| PostgreSQL | Enterprise Data Warehouse |
| SQL | Analytics, views, optimization, reporting |
| Power BI | Business Intelligence dashboards |
| Apache Airflow | Workflow scheduling and orchestration |
| Docker | Application containerization |
| Git & GitHub | Version control |
| python-dotenv | Environment variable management |
| Logging | ETL monitoring and troubleshooting |

---

# 6. ETL Architecture

The ETL pipeline follows a layered architecture.

## Extract Layer

Reads data from multiple operational source systems.

## Validation Layer

Performs data quality checks including:

- Null value validation
- Duplicate detection
- Data type validation
- Business rule validation
- Referential integrity validation

## Staging Layer

Stores standardized intermediate datasets before transformation.

## Transformation Layer

Builds dimension tables and fact tables according to the Star Schema design.

Transformations include:

- Business calculations
- Surrogate key generation
- Data cleansing
- SCD Type 2 processing

## Incremental Load Layer

Processes only new or modified records using High Watermark Loading to improve ETL performance.

## Load Layer

Loads transformed data into the PostgreSQL Enterprise Data Warehouse.

## Audit Layer

Captures ETL execution details including:

- Start Time
- End Time
- Rows Processed
- Rows Loaded
- Failed Records
- Execution Status

---

# 7. Data Warehouse Architecture

The warehouse follows a Star Schema.

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

# 8. Project Folder Responsibilities

| Folder | Responsibility |
|----------|---------------|
| config | Configuration files |
| data | Raw, staging, processed, and warehouse export data |
| etl | ETL modules |
| database | Database scripts and schema objects |
| sql | Analytics, reporting, optimization, and SQL scripts |
| docs | Project documentation |
| airflow | Workflow orchestration |
| docker | Docker configuration |
| powerbi | Dashboards and datasets |
| tests | Unit and integration tests |
| logs | ETL execution logs |

---

# 9. Expected Business Outcomes

The Enterprise Retail Sales Analytics Data Warehouse provides:

- Centralized reporting
- Improved decision-making
- Faster analytical queries
- Consistent business metrics
- Historical trend analysis
- Inventory visibility
- Sales performance insights
- Customer behavior analysis
- Executive dashboards
- Scalable enterprise architecture

---

# 10. Future Enhancements

Future improvements may include:

- Real-time streaming using Apache Kafka
- Cloud deployment (Azure, AWS, GCP)
- CI/CD pipeline integration
- Data quality monitoring dashboards
- Automated testing pipeline
- Machine Learning integration
- Data catalog and lineage
- Metadata-driven ETL framework

---

## Document Summary

This document describes the overall architecture of the Enterprise Retail Sales Analytics Data Warehouse, including the business problem, solution architecture, technology stack, ETL workflow, and expected business outcomes. It serves as the primary architectural reference for the project.