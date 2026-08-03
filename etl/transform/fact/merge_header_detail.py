"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : merge_header_detail.py
Purpose : Merge Sales Header and Sales Detail
============================================================
"""

import pandas as pd

from etl.utils import logger


def merge_header_detail(
    sales_header: pd.DataFrame,
    sales_detail: pd.DataFrame,
) -> pd.DataFrame:
    """
    Merge sales header and sales detail datasets.
    """

    logger.info("Merging Sales Header and Sales Detail...")

    fact = sales_detail.merge(
        sales_header,
        on="transaction_id",
        how="inner",
        validate="many_to_one",
    )

    logger.info(
        "Merged Sales Records : %s",
        f"{len(fact):,}",
    )

    return fact