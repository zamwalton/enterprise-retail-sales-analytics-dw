-- =========================================================
-- Enterprise Retail Sales Analytics Data Warehouse
-- Table   : fact_sales
-- Purpose : Retail sales transaction fact table
-- =========================================================

CREATE TABLE IF NOT EXISTS retail_dw.fact_sales
(
    sales_key           BIGINT          NOT NULL,
    transaction_id      VARCHAR(30)     NOT NULL,
    line_number         INTEGER         NOT NULL,

    date_key            INTEGER         NOT NULL,
    customer_key        BIGINT          NOT NULL,
    employee_key        BIGINT          NOT NULL,
    store_key           BIGINT          NOT NULL,
    product_key         BIGINT          NOT NULL,
    promotion_key       BIGINT          NOT NULL,

    quantity            INTEGER         NOT NULL,
    unit_price          NUMERIC(12,2)    NOT NULL,
    discount_amount     NUMERIC(12,2)    NOT NULL,
    tax_amount          NUMERIC(12,2)    NOT NULL,
    total_amount        NUMERIC(14,2)    NOT NULL,

    payment_method      VARCHAR(30)     NOT NULL,
    transaction_status  VARCHAR(30)     NOT NULL,

    created_date        TIMESTAMP       NOT NULL,
    updated_date        TIMESTAMP       NULL,
    is_active           BOOLEAN         NOT NULL DEFAULT TRUE,

    CONSTRAINT pk_fact_sales
        PRIMARY KEY (sales_key),
    CONSTRAINT uq_fact_sales_transaction_line
        UNIQUE (transaction_id, line_number)
);