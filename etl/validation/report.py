"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : report.py
Purpose : Enterprise Data Quality Reporting Framework
============================================================
"""

from collections import defaultdict
from etl.utils import logger


class DataQualityReport:
    """
    Collects successful data quality validation checks and
    prints a consolidated report after validation completes.
    """

    def __init__(self) -> None:
        self._results = defaultdict(list)

    def add_check(
        self,
        dataset: str,
        check: str,
    ) -> None:
        """
        Register a successful validation check.
        """

        self._results[dataset].append(check)

    def print_report(self) -> None:
        """
        Print the consolidated data quality report.
        """

        logger.info("=" * 55)
        logger.info("DATA QUALITY REPORT")
        logger.info("=" * 55)

        for dataset, checks in self._results.items():

            logger.info("%s", dataset)

            for check in checks:
                logger.info("  [PASSED] %s", check)

            logger.info("")

        logger.info("=" * 55)
        logger.info("ALL DATA QUALITY CHECKS PASSED")
        logger.info("=" * 55)