/*
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : 04_dim_employee.sql
Author  : Zam Walton P M
Purpose : Create Employee Dimension (SCD Type 2)
Version : 1.0
============================================================
*/

BEGIN;

-- =========================================================
-- Employee Dimension Table
-- =========================================================

CREATE TABLE IF NOT EXISTS retail_dw.dim_employee (

    -- Surrogate Key
    employee_key BIGSERIAL PRIMARY KEY,

    -- Business Key
    employee_id VARCHAR(20) NOT NULL,

    -- Employee Information
    employee_name VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    job_title VARCHAR(100) NOT NULL,
    manager_id VARCHAR(20),
    hire_date DATE,
    employment_status VARCHAR(20) NOT NULL DEFAULT 'Active',

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
    CONSTRAINT chk_employee_status
        CHECK (
            employment_status IN
            ('Active', 'On Leave', 'Terminated')
        ),

    CONSTRAINT chk_employee_scd_dates
        CHECK (
            effective_end_date >= effective_start_date
        )
);

-- =========================================================
-- Table Comment
-- =========================================================

COMMENT ON TABLE retail_dw.dim_employee IS
'Employee Dimension implementing Slowly Changing Dimension Type 2.';

-- =========================================================
-- Column Comments
-- =========================================================

COMMENT ON COLUMN retail_dw.dim_employee.employee_key IS
'Warehouse surrogate key';

COMMENT ON COLUMN retail_dw.dim_employee.employee_id IS
'Business key from HR system';

COMMENT ON COLUMN retail_dw.dim_employee.employee_name IS
'Employee full name';

COMMENT ON COLUMN retail_dw.dim_employee.department IS
'Department name';

COMMENT ON COLUMN retail_dw.dim_employee.job_title IS
'Employee job title';

COMMENT ON COLUMN retail_dw.dim_employee.manager_id IS
'Business identifier of the employee manager';

COMMENT ON COLUMN retail_dw.dim_employee.employment_status IS
'Current employment status';

COMMENT ON COLUMN retail_dw.dim_employee.effective_start_date IS
'SCD Type 2 start date';

COMMENT ON COLUMN retail_dw.dim_employee.effective_end_date IS
'SCD Type 2 end date';

COMMENT ON COLUMN retail_dw.dim_employee.is_current IS
'Current active employee record';

COMMIT;