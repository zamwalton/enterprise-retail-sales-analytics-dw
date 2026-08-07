
-- ============================================================
-- Project : Enterprise Retail Sales Analytics Data Warehouse
-- File    : 01_etl_metadata.sql
-- Purpose : ETL Pipeline Metadata Table
-- ============================================================

DROP TABLE IF EXISTS retail_dw.etl_metadata;

CREATE TABLE retail_dw.etl_metadata
(
    metadata_id            BIGSERIAL PRIMARY KEY,

    pipeline_name          VARCHAR(100) NOT NULL,

    pipeline_run_id        UUID NOT NULL,

    load_type              VARCHAR(20) NOT NULL,

    start_time             TIMESTAMP NOT NULL,

    end_time               TIMESTAMP,

    duration_seconds       NUMERIC(10,2),

    rows_processed         INTEGER DEFAULT 0,

    status                 VARCHAR(20) NOT NULL,

    error_message          TEXT,

    last_successful_run    TIMESTAMP,

    created_date           TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE retail_dw.etl_metadata IS
'Stores ETL execution history, pipeline metadata and high-watermark information.';