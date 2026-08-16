/*
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : 02_etl_control.sql
Purpose : Incremental ETL High-Watermark Control
============================================================
*/

CREATE TABLE IF NOT EXISTS retail_dw.etl_control
(
    control_id BIGSERIAL PRIMARY KEY,

    pipeline_name VARCHAR(100) NOT NULL,

    source_system VARCHAR(100) NOT NULL,

    watermark_column VARCHAR(100) NOT NULL,

    last_watermark_date TIMESTAMP,

    last_watermark_id VARCHAR(100),

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_etl_control_pipeline_source
        UNIQUE (
            pipeline_name,
            source_system
        )
);