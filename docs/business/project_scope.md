# Project Scope

---

## Document Information

| Property | Value |
|----------|--------|
| Project | Enterprise Retail Sales Analytics Data Warehouse |
| Version | 1.0 |
| Author | Zam Walton P M |
| Last Updated | July 2026 |
| Document Type | Project Scope |

---

# 1. Purpose

This document defines the boundaries of the Enterprise Retail Sales Analytics Data Warehouse project. It identifies what is included, what is excluded, the project deliverables, assumptions, and constraints to ensure the project remains focused and manageable.

---

# 2. Project Goal

Design and implement a production-style Data Engineering solution that consolidates retail data from multiple operational systems into a centralized PostgreSQL Data Warehouse for reporting and analytics.

---

# 3. In Scope

The following features are included in this project:

## Source Systems

- Point of Sale (POS)
- Online Store
- CRM
- Product Master
- Store Master
- HR
- Promotions
- Suppliers
- Inventory

## Data Engineering

- Python ETL Pipeline
- Modular ETL Architecture
- Data Validation Framework
- Staging Layer
- Transformation Layer
- Incremental ETL
- High Watermark Loading
- SCD Type 2
- ETL Audit Framework

## Data Warehouse

- PostgreSQL Data Warehouse
- Star Schema
- Fact Tables
- Dimension Tables
- Reporting Views
- Query Optimization

## Analytics

- SQL Analytics
- Window Functions
- Common Table Expressions (CTEs)
- Ranking Functions
- Execution Plan Analysis

## Reporting

- Executive Dashboard
- Sales Dashboard
- Product Dashboard
- Customer Dashboard
- Store Dashboard
- Inventory Dashboard

## DevOps

- Docker
- Apache Airflow
- Git & GitHub
- Environment Variables
- Logging

---

# 4. Out of Scope

The following items are intentionally excluded from this version of the project:

- Real-time streaming
- Apache Kafka
- Spark
- Snowflake
- Azure Data Factory
- AWS Glue
- Google BigQuery
- Machine Learning
- REST APIs
- Mobile applications
- ERP integrations
- Change Data Capture (CDC)

These technologies may be considered in future versions.

---

# 5. Project Deliverables

The completed project will include:

- Enterprise Data Warehouse
- Python ETL Pipeline
- Data Quality Framework
- Incremental Loading
- SCD Type 2 Implementation
- SQL Analytics Scripts
- Six Power BI Dashboards
- Docker Configuration
- Apache Airflow DAGs
- Professional Documentation
- GitHub Repository

---

# 6. Assumptions

- Source data is generated as CSV files.
- PostgreSQL is the target warehouse.
- Daily batch processing is sufficient.
- Source systems provide valid business keys.
- Power BI connects directly to PostgreSQL.

---

# 7. Constraints

- Single developer project.
- Local development environment.
- Open-source technologies only.
- Batch processing architecture.
- Python 3.10 environment.

---

# 8. Success Criteria

The project will be considered complete when:

- All source systems are integrated.
- ETL pipeline executes successfully.
- Incremental loading functions correctly.
- SCD Type 2 is implemented.
- Star Schema is fully populated.
- SQL analytics queries execute successfully.
- Six Power BI dashboards are completed.
- Docker deployment is operational.
- Airflow orchestration is functional.
- Documentation is complete.

---

# Summary

This document defines the scope, deliverables, assumptions, and constraints for the Enterprise Retail Sales Analytics Data Warehouse project. It provides clear boundaries for the project and helps prevent unnecessary expansion beyond the planned objectives.