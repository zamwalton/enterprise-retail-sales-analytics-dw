
/*
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : 05_dim_promotion.sql
Author  : Zam Walton P M
Purpose : Create Promotion Dimension (SCD Type 2)
Version : 1.1
============================================================
*/

BEGIN;

-- =========================================================
-- Promotion Dimension Table
-- =========================================================

CREATE TABLE IF NOT EXISTS retail_dw.dim_promotion (

    -- =====================================================
    -- Surrogate Key
    -- =====================================================

    promotion_key BIGSERIAL PRIMARY KEY,

    -- =====================================================
    -- Business Key
    -- =====================================================

    promotion_id VARCHAR(20) NOT NULL,

    -- =====================================================
    -- Promotion Information
    -- =====================================================

    promotion_name VARCHAR(150) NOT NULL,

    promotion_type VARCHAR(30) NOT NULL,

    -- =====================================================
    -- Discount Measures
    -- =====================================================

    discount_percentage NUMERIC(5,2),

    discount_amount NUMERIC(12,2),

    -- =====================================================
    -- Promotion Validity Dates
    -- =====================================================

    start_date DATE NOT NULL,

    end_date DATE NOT NULL,

    -- =====================================================
    -- Promotion Status
    -- =====================================================

    promotion_status VARCHAR(20) NOT NULL
        DEFAULT 'Scheduled',

    -- =====================================================
    -- SCD Type 2 Columns
    -- =====================================================

    effective_start_date DATE NOT NULL,

    effective_end_date DATE NOT NULL
        DEFAULT DATE '9999-12-31',

    is_current BOOLEAN NOT NULL
        DEFAULT TRUE,

    -- =====================================================
    -- Audit Columns
    -- =====================================================

    created_date TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_date TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    -- =====================================================
    -- Promotion Type Constraint
    -- =====================================================
    -- Allows:
    --   Percentage
    --   Fixed Amount
    --   Buy One Get One
    --   None -> Default "No Promotion" row
    -- =====================================================

    CONSTRAINT chk_promotion_type
        CHECK (
            promotion_type IN (
                'Percentage',
                'Fixed Amount',
                'Buy One Get One',
                'None'
            )
        ),

    -- =====================================================
    -- Discount Percentage Constraint
    -- =====================================================

    CONSTRAINT chk_discount_percentage
        CHECK (
            discount_percentage IS NULL
            OR (
                discount_percentage >= 0
                AND discount_percentage <= 100
            )
        ),

    -- =====================================================
    -- Discount Amount Constraint
    -- =====================================================

    CONSTRAINT chk_discount_amount
        CHECK (
            discount_amount IS NULL
            OR discount_amount >= 0
        ),

    -- =====================================================
    -- Promotion Discount Business Rule
    -- =====================================================
    -- Allows:
    --
    --   1. Default "No Promotion" row
    --   2. Percentage promotions
    --   3. Fixed Amount promotions
    --   4. Buy One Get One promotions
    -- =====================================================

    CONSTRAINT chk_promotion_discount
        CHECK (

            -- ------------------------------------------------
            -- Default / Unknown Promotion
            -- ------------------------------------------------

            promotion_key = 0

            OR

            -- ------------------------------------------------
            -- Percentage Promotion
            -- ------------------------------------------------

            (
                promotion_type = 'Percentage'
                AND discount_percentage BETWEEN 0 AND 100
                AND discount_amount IS NULL
            )

            OR

            -- ------------------------------------------------
            -- Fixed Amount Promotion
            -- ------------------------------------------------

            (
                promotion_type = 'Fixed Amount'
                AND discount_amount >= 0
                AND discount_percentage IS NULL
            )

            OR

            -- ------------------------------------------------
            -- Buy One Get One Promotion
            -- ------------------------------------------------

            (
                promotion_type = 'Buy One Get One'
                AND discount_percentage IS NULL
                AND discount_amount IS NULL
            )

            OR

            -- ------------------------------------------------
            -- Default "No Promotion" Row
            -- ------------------------------------------------

            (
                promotion_type = 'None'
                AND discount_percentage IS NULL
                AND discount_amount IS NULL
            )
        ),

    -- =====================================================
    -- Promotion Status Constraint
    -- =====================================================
    -- Allows:
    --   Scheduled
    --   Active
    --   Expired
    --   Not Applicable -> Default "No Promotion" row
    -- =====================================================

    CONSTRAINT chk_promotion_status
        CHECK (
            promotion_status IN (
                'Scheduled',
                'Active',
                'Expired',
                'Not Applicable'
            )
        ),

    -- =====================================================
    -- Promotion Date Constraint
    -- =====================================================

    CONSTRAINT chk_promotion_dates
        CHECK (
            end_date >= start_date
        ),

    -- =====================================================
    -- SCD Type 2 Date Constraint
    -- =====================================================

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
'Percentage discount offered for Percentage promotions';

COMMENT ON COLUMN retail_dw.dim_promotion.discount_amount IS
'Fixed monetary discount offered for Fixed Amount promotions';

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

COMMENT ON COLUMN retail_dw.dim_promotion.created_date IS
'Timestamp when the warehouse record was created';

COMMENT ON COLUMN retail_dw.dim_promotion.updated_date IS
'Timestamp when the warehouse record was last updated';

-- =========================================================
-- Commit Transaction
-- =========================================================

COMMIT;

