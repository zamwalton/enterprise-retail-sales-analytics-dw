/*
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : 01_create_schema.sql
Author  : Zam Walton P M
Purpose : Create the PostgreSQL schema for the Enterprise
          Retail Sales Analytics Data Warehouse.
Version : 1.0
============================================================
*/

-- =========================================================
-- Create Data Warehouse Schema
-- =========================================================

CREATE SCHEMA IF NOT EXISTS retail_dw;

COMMENT ON SCHEMA retail_dw IS
'Enterprise Retail Sales Analytics Data Warehouse Schema';