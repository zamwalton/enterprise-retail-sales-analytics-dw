/*
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : 01_dim_customer.sql
Author  : Zam Walton P M
Purpose : Create Customer Dimension (SCD Type 2)
Version : 1.0
============================================================
*/

BEGIN;

-- =========================================================
-- Customer Dimension Table
-- =========================================================

CREATE TABLE IF NOT EXISTS retail_dw.dim_customer (

    -- Surrogate Key
    customer_key BIGSERIAL PRIMARY KEY,

    -- Business Key
    customer_id VARCHAR(20) NOT NULL,

    -- Customer Details
    customer_name VARCHAR(100) NOT NULL,
    gender VARCHAR(10),
    date_of_birth DATE,
    email VARCHAR(150),
    phone VARCHAR(20),

    -- Location
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),

    -- Loyalty Information
    loyalty_tier VARCHAR(20),

    -- SCD Type 2 Columns
    effective_start_date DATE NOT NULL,
    effective_end_date DATE NOT NULL DEFAULT DATE '9999-12-31',
    is_current BOOLEAN NOT NULL DEFAULT TRUE,

    -- Audit Columns
    created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT chk_customer_gender
        CHECK (gender IN ('Male', 'Female', 'Other') OR gender IS NULL),

    CONSTRAINT chk_loyalty_tier
        CHECK (
            loyalty_tier IN
            ('Bronze', 'Silver', 'Gold', 'Platinum')
            OR loyalty_tier IS NULL
        ),

    CONSTRAINT chk_scd_dates
        CHECK (effective_end_date >= effective_start_date)
);

-- =========================================================
-- Unique Constraint for SCD Type 2
-- =========================================================

ALTER TABLE retail_dw.dim_customer
ADD CONSTRAINT uq_customer_version
UNIQUE (
    customer_id,
    effective_start_date
);

-- =========================================================
-- Table Comment
-- =========================================================

COMMENT ON TABLE retail_dw.dim_customer IS
'Customer dimension implementing SCD Type 2 for historical tracking.';

-- =========================================================
-- Column Comments
-- =========================================================

COMMENT ON COLUMN retail_dw.dim_customer.customer_key IS
'Warehouse surrogate key';

COMMENT ON COLUMN retail_dw.dim_customer.customer_id IS
'Business customer identifier from CRM';

COMMENT ON COLUMN retail_dw.dim_customer.is_current IS
'Indicates active customer record';

COMMENT ON COLUMN retail_dw.dim_customer.effective_start_date IS
'SCD Type 2 start date';

COMMENT ON COLUMN retail_dw.dim_customer.effective_end_date IS
'SCD Type 2 end date';

COMMIT;