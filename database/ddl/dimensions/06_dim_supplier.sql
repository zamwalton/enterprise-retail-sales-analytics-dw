/*
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : 06_dim_supplier.sql
Author  : Zam Walton P M
Purpose : Create Supplier Dimension (SCD Type 2)
Version : 1.0
============================================================
*/

BEGIN;

-- =========================================================
-- Supplier Dimension Table
-- =========================================================

CREATE TABLE IF NOT EXISTS retail_dw.dim_supplier (

    -- Surrogate Key
    supplier_key BIGSERIAL PRIMARY KEY,

    -- Business Key
    supplier_id VARCHAR(20) NOT NULL,

    -- Supplier Information
    supplier_name VARCHAR(150) NOT NULL,
    supplier_category VARCHAR(20) NOT NULL,
    contact_name VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(150),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    supplier_status VARCHAR(20) NOT NULL DEFAULT 'Active',

    -- SCD Type 2 Columns
    effective_start_date DATE NOT NULL,
    effective_end_date DATE NOT NULL
        DEFAULT DATE '9999-12-31',
    is_current BOOLEAN NOT NULL
        DEFAULT TRUE,

    -- Audit Columns
    created_date TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    -- Constraints

    CONSTRAINT chk_supplier_category
        CHECK (
            supplier_category IN
            ('Local', 'National', 'International')
        ),

    CONSTRAINT chk_supplier_status
        CHECK (
            supplier_status IN
            ('Active', 'Inactive')
        ),

    CONSTRAINT chk_supplier_scd_dates
        CHECK (
            effective_end_date >= effective_start_date
        )
);

-- =========================================================
-- Table Comment
-- =========================================================

COMMENT ON TABLE retail_dw.dim_supplier IS
'Supplier Dimension implementing Slowly Changing Dimension Type 2.';

-- =========================================================
-- Column Comments
-- =========================================================

COMMENT ON COLUMN retail_dw.dim_supplier.supplier_key IS
'Warehouse surrogate key';

COMMENT ON COLUMN retail_dw.dim_supplier.supplier_id IS
'Business key from supplier master system';

COMMENT ON COLUMN retail_dw.dim_supplier.supplier_name IS
'Supplier company name';

COMMENT ON COLUMN retail_dw.dim_supplier.supplier_category IS
'Supplier classification';

COMMENT ON COLUMN retail_dw.dim_supplier.contact_name IS
'Primary supplier contact';

COMMENT ON COLUMN retail_dw.dim_supplier.phone IS
'Supplier contact phone number';

COMMENT ON COLUMN retail_dw.dim_supplier.email IS
'Supplier contact email address';

COMMENT ON COLUMN retail_dw.dim_supplier.city IS
'Supplier city';

COMMENT ON COLUMN retail_dw.dim_supplier.state IS
'Supplier state';

COMMENT ON COLUMN retail_dw.dim_supplier.country IS
'Supplier country';

COMMENT ON COLUMN retail_dw.dim_supplier.supplier_status IS
'Current supplier status';

COMMENT ON COLUMN retail_dw.dim_supplier.effective_start_date IS
'SCD Type 2 start date';

COMMENT ON COLUMN retail_dw.dim_supplier.effective_end_date IS
'SCD Type 2 end date';

COMMENT ON COLUMN retail_dw.dim_supplier.is_current IS
'Current active supplier record';

COMMIT;