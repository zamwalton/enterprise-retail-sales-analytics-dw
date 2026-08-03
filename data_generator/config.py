"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : config.py
Purpose : Configuration for source data generation
============================================================
"""

from pathlib import Path

# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

CRM_DIR = RAW_DATA_DIR / "crm"
HR_DIR = RAW_DATA_DIR / "hr"
PRODUCT_DIR = RAW_DATA_DIR / "product"
STORE_DIR = RAW_DATA_DIR / "store"
SUPPLIER_DIR = RAW_DATA_DIR / "supplier"
PROMOTION_DIR = RAW_DATA_DIR / "promotion"
POS_DIR = RAW_DATA_DIR / "pos"
INVENTORY_DIR = RAW_DATA_DIR / "inventory"
ONLINE_DIR = RAW_DATA_DIR / "online"

# ==========================================================
# Dataset Sizes
# ==========================================================

NUM_CUSTOMERS = 10000
NUM_EMPLOYEES = 500
NUM_PRODUCTS = 1000
NUM_STORES = 100
NUM_SUPPLIERS = 200
NUM_PROMOTIONS = 100

NUM_POS_TRANSACTIONS = 250000
NUM_ONLINE_TRANSACTIONS = 100000
NUM_INVENTORY_RECORDS = 50000


# ==========================================================
# Transaction Dataset Sizes
# ==========================================================

NUM_SALES_TRANSACTIONS = 100000
MAX_ITEMS_PER_TRANSACTION = 5

GST_RATE = 0.18