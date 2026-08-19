"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : dimension_reader.py
Purpose : Read warehouse dimensions for incremental ETL
============================================================
"""

import pandas as pd

from database.connection import get_connection


def read_dimension(table_name: str) -> pd.DataFrame:
    """
    Read a warehouse dimension table into a DataFrame.
    """

    conn = get_connection()

    try:
        query = f"""
        SELECT *
        FROM retail_dw.{table_name}
        """

        df = pd.read_sql(
            query,
            conn,
        )

        # ==================================================
        # Normalize SCD2 date columns
        # ==================================================

        if "effective_start_date" in df.columns:

            df["effective_start_date"] = pd.to_datetime(
                df["effective_start_date"],
                errors="coerce",
            )

        if "effective_end_date" in df.columns:

            df["effective_end_date"] = pd.to_datetime(
                df["effective_end_date"],
                errors="coerce",
            )

            # PostgreSQL 9999-12-31 becomes NaT in pandas.
            # Replace it with pandas' maximum supported date
            # for in-memory SCD2 comparisons.

            df["effective_end_date"] = df[
                "effective_end_date"
            ].fillna(
                pd.Timestamp.max.normalize()
            )

        return df

    finally:
        conn.close()

def read_incremental_dimensions():
    """
    Read all dimensions required by the incremental pipeline.
    """

    return {
        "customer": read_dimension("dim_customer"),
        "employee": read_dimension("dim_employee"),
        "store": read_dimension("dim_store"),
        "product": read_dimension("dim_product"),
        "promotion": read_dimension("dim_promotion"),
        "date": read_dimension("dim_date"),
    }