-- =========================================================
-- Enterprise Retail Sales Analytics Data Warehouse
-- Master Deployment Script
-- =========================================================

-- Create Schema
\i 01_create_schema.sql

-- Dimensions
\i dimensions/01_dim_customer.sql
\i dimensions/02_dim_product.sql
\i dimensions/03_dim_store.sql
\i dimensions/04_dim_employee.sql
\i dimensions/05_dim_promotion.sql
\i dimensions/06_dim_supplier.sql
\i dimensions/07_dim_date.sql

-- Facts
\i facts/01_fact_sales.sql

-- Constraints
-- \i constraints/01_primary_keys.sql
-- \i constraints/02_foreign_keys.sql

-- Indexes
-- \i indexes/01_indexes.sql