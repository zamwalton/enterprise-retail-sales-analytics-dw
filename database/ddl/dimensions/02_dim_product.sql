/*
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : 02_dim_product.sql
Author  : Zam Walton P M
Purpose : Create Product Dimension (SCD Type 2)
Version : 1.0
============================================================
*/

BEGIN;

-- =========================================================
-- Product Dimension Table
-- =========================================================

CREATE TABLE IF NOT EXISTS retail_dw.dim_product (

    -- Surrogate Key
    product_key BIGSERIAL PRIMARY KEY,

    -- Business Key
    product_id VARCHAR(20) NOT NULL,

    -- Product Information
    product_name VARCHAR(150) NOT NULL,
    brand VARCHAR(100),
    category VARCHAR(100),
    subcategory VARCHAR(100),

    -- Supplier
    supplier_id VARCHAR(20),

    -- Pricing
    standard_cost NUMERIC(10,2) NOT NULL,
    selling_price NUMERIC(10,2) NOT NULL,

    -- Status
    product_status VARCHAR(20) NOT NULL DEFAULT 'Active',

    -- SCD Type 2
    effective_start_date DATE NOT NULL,
    effective_end_date DATE NOT NULL
        DEFAULT DATE '9999-12-31',
    is_current BOOLEAN NOT NULL
        DEFAULT TRUE,

    -- Audit
    created_date TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    -- Constraints

    CONSTRAINT chk_product_status
        CHECK (
            product_status IN
            ('Active','Discontinued','Out of Stock')
        ),

    CONSTRAINT chk_price
        CHECK (
            selling_price >= standard_cost
        ),

    CONSTRAINT chk_product_scd_dates
        CHECK (
            effective_end_date >= effective_start_date
        )
);

-- =========================================================
-- Comments
-- =========================================================

COMMENT ON TABLE retail_dw.dim_product IS
'Product Dimension implementing Slowly Changing Dimension Type 2.';

COMMENT ON COLUMN retail_dw.dim_product.product_key IS
'Warehouse surrogate key';

COMMENT ON COLUMN retail_dw.dim_product.product_id IS
'Business key from Product Master';

COMMENT ON COLUMN retail_dw.dim_product.standard_cost IS
'Cost price of the product';

COMMENT ON COLUMN retail_dw.dim_product.selling_price IS
'Selling price of the product';

COMMENT ON COLUMN retail_dw.dim_product.product_status IS
'Current lifecycle status of the product';

COMMIT;