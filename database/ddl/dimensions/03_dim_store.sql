/*
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : 03_dim_store.sql
Author  : Zam Walton P M
Purpose : Create Store Dimension (SCD Type 2)
Version : 1.0
============================================================
*/

BEGIN;

-- =========================================================
-- Store Dimension Table
-- =========================================================

CREATE TABLE IF NOT EXISTS retail_dw.dim_store (

    -- Surrogate Key
    store_key BIGSERIAL PRIMARY KEY,

    -- Business Key
    store_id VARCHAR(20) NOT NULL,

    -- Store Information
    store_name VARCHAR(100) NOT NULL,
    store_type VARCHAR(20) NOT NULL,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    opening_date DATE,
    store_status VARCHAR(20) NOT NULL DEFAULT 'Active',

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

    CONSTRAINT chk_store_type
        CHECK (
            store_type IN
            ('Retail', 'Outlet', 'Warehouse')
        ),

    CONSTRAINT chk_store_status
        CHECK (
            store_status IN
            ('Active', 'Closed')
        ),

    CONSTRAINT chk_store_scd_dates
        CHECK (
            effective_end_date >= effective_start_date
        )
);

-- =========================================================
-- Table Comment
-- =========================================================

COMMENT ON TABLE retail_dw.dim_store IS
'Store Dimension implementing Slowly Changing Dimension Type 2.';

-- =========================================================
-- Column Comments
-- =========================================================

COMMENT ON COLUMN retail_dw.dim_store.store_key IS
'Warehouse surrogate key';

COMMENT ON COLUMN retail_dw.dim_store.store_id IS
'Business key from Store Master';

COMMENT ON COLUMN retail_dw.dim_store.store_name IS
'Store name';

COMMENT ON COLUMN retail_dw.dim_store.store_type IS
'Type of store: Retail, Outlet, or Warehouse';

COMMENT ON COLUMN retail_dw.dim_store.city IS
'Store city';

COMMENT ON COLUMN retail_dw.dim_store.state IS
'Store state';

COMMENT ON COLUMN retail_dw.dim_store.country IS
'Store country';

COMMENT ON COLUMN retail_dw.dim_store.store_status IS
'Current operational status of the store';

COMMENT ON COLUMN retail_dw.dim_store.effective_start_date IS
'SCD Type 2 start date';

COMMENT ON COLUMN retail_dw.dim_store.effective_end_date IS
'SCD Type 2 end date';

COMMENT ON COLUMN retail_dw.dim_store.is_current IS
'Current active record indicator';

COMMIT;