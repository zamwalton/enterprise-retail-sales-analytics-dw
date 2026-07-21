-- =========================================================
-- Enterprise Retail Sales Analytics Data Warehouse
-- Master Deployment Script
-- =========================================================

\i 01_create_schema.sql
\i dimensions/01_dim_customer.sql
\i dimensions/02_dim_product.sql
\i dimensions/03_dim_store.sql
\i dimensions/04_dim_employee.sql
\i dimensions/05_dim_promotion.sql