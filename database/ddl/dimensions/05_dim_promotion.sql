/*
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : 05_dim_promotion.sql
Author  : Zam Walton P M
Purpose : Create Promotion Dimension (SCD Type 2)
Version : 1.0
============================================================
*/

BEGIN;

-- =========================================================
-- Promotion Dimension Table
-- =========================================================

CREATE TABLE IF NOT EXISTS retail_dw.dim_promotion (

    -- Surrogate Key
    promotion_key BIGSERIAL PRIMARY KEY,

    -- Business Key
    promotion_id VARCHAR(20) NOT NULL,

    -- Promotion Information
    promotion_name VARCHAR(150) NOT NULL,
    promotion_type VARCHAR(30) NOT NULL,
    discount_percentage NUMERIC(5,2) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    promotion_status VARCHAR(20) NOT NULL DEFAULT 'Scheduled',

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

    CONSTRAINT chk_promotion_type
        CHECK (
            promotion_type IN
            ('Percentage', 'Fixed Amount', 'Buy One Get One')
        ),

    CONSTRAINT chk_discount_percentage
        CHECK (
            discount_percentage >= 0
            AND discount_percentage <= 100
        ),

    CONSTRAINT chk_promotion_status
        CHECK (
            promotion_status IN
            ('Scheduled', 'Active', 'Expired')
        ),

    CONSTRAINT chk_promotion_dates
        CHECK (
            end_date >= start_date
        ),

    CONSTRAINT chk_promotion_scd_dates
        CHECK (
            effective_end_date >= effective_start_date
        )
);

-- =========================================================
-- Table Comment
-- =========================================================

COMMENT ON TABLE retail_dw.dim_promotion IS
'Promotion Dimension implementing Slowly Changing Dimension Type 2.';

-- =========================================================
-- Column Comments
-- =========================================================

COMMENT ON COLUMN retail_dw.dim_promotion.promotion_key IS
'Warehouse surrogate key';

COMMENT ON COLUMN retail_dw.dim_promotion.promotion_id IS
'Business key from promotion management system';

COMMENT ON COLUMN retail_dw.dim_promotion.promotion_name IS
'Promotion or campaign name';

COMMENT ON COLUMN retail_dw.dim_promotion.promotion_type IS
'Promotion type';

COMMENT ON COLUMN retail_dw.dim_promotion.discount_percentage IS
'Discount percentage offered';

COMMENT ON COLUMN retail_dw.dim_promotion.start_date IS
'Promotion start date';

COMMENT ON COLUMN retail_dw.dim_promotion.end_date IS
'Promotion end date';

COMMENT ON COLUMN retail_dw.dim_promotion.promotion_status IS
'Current promotion status';

COMMENT ON COLUMN retail_dw.dim_promotion.effective_start_date IS
'SCD Type 2 start date';

COMMENT ON COLUMN retail_dw.dim_promotion.effective_end_date IS
'SCD Type 2 end date';

COMMENT ON COLUMN retail_dw.dim_promotion.is_current IS
'Current active promotion record';

COMMIT;