"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : connection.py
Purpose : PostgreSQL Database Connection
============================================================
"""

import psycopg2

from config.settings import (
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
)

from etl.utils import logger


def get_connection():
    """
    Create PostgreSQL database connection.
    """

    try:

        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )

        
        return connection

    except Exception as e:

        logger.error(e)
        raise