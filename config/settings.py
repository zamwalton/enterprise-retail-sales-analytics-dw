"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : settings.py
Purpose : Project Configuration
============================================================
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ==========================================================
# PostgreSQL
# ==========================================================

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# ==========================================================
# Paths
# ==========================================================

RAW_DATA_PATH = os.getenv("RAW_DATA_PATH")
STAGING_DATA_PATH = os.getenv("STAGING_DATA_PATH")
PROCESSED_DATA_PATH = os.getenv("PROCESSED_DATA_PATH")

# ==========================================================
# Logging
# ==========================================================

LOG_LEVEL = os.getenv("LOG_LEVEL")

# ==========================================================
# Warehouse
# ==========================================================

WAREHOUSE_SCHEMA = os.getenv("WAREHOUSE_SCHEMA")

# ==========================================================
# Incremental ETL
# ==========================================================

HIGH_WATERMARK_TABLE = os.getenv("HIGH_WATERMARK_TABLE")