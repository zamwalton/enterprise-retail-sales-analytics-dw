/*
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : 07_dim_date.sql
Author  : Zam Walton P M
Purpose : Create Date Dimension
Version : 1.0
============================================================
*/

BEGIN;

-- =========================================================
-- Date Dimension Table
-- =========================================================

CREATE TABLE IF NOT EXISTS retail_dw.dim_date (

    -- Date Key
    date_key INTEGER PRIMARY KEY,

    -- Calendar Date
    full_date DATE NOT NULL UNIQUE,

    -- Date Attributes
    day INTEGER NOT NULL,
    day_name VARCHAR(15) NOT NULL,

    week_of_year INTEGER NOT NULL,

    month INTEGER NOT NULL,
    month_name VARCHAR(15) NOT NULL,

    quarter INTEGER NOT NULL,

    year INTEGER NOT NULL,

    -- Business Calendar Flags
    is_weekend BOOLEAN NOT NULL,
    is_month_end BOOLEAN NOT NULL,
    is_quarter_end BOOLEAN NOT NULL,
    is_year_end BOOLEAN NOT NULL
);

-- =========================================================
-- Comments
-- =========================================================

COMMENT ON TABLE retail_dw.dim_date IS
'Date Dimension generated programmatically for reporting.';

COMMENT ON COLUMN retail_dw.dim_date.date_key IS
'Integer key in YYYYMMDD format';

COMMENT ON COLUMN retail_dw.dim_date.full_date IS
'Calendar date';

COMMENT ON COLUMN retail_dw.dim_date.day_name IS
'Name of the weekday';

COMMENT ON COLUMN retail_dw.dim_date.week_of_year IS
'ISO week number';

COMMENT ON COLUMN retail_dw.dim_date.month_name IS
'Month name';

COMMENT ON COLUMN retail_dw.dim_date.quarter IS
'Calendar quarter';

COMMENT ON COLUMN retail_dw.dim_date.is_weekend IS
'Weekend indicator';

COMMENT ON COLUMN retail_dw.dim_date.is_month_end IS
'Month-end indicator';

COMMENT ON COLUMN retail_dw.dim_date.is_quarter_end IS
'Quarter-end indicator';

COMMENT ON COLUMN retail_dw.dim_date.is_year_end IS
'Year-end indicator';

COMMIT;