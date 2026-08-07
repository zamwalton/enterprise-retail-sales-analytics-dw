
"""
============================================================
Project : Enterprise Retail Sales Analytics Data Warehouse
File    : metadata.py
Purpose : ETL Metadata Management
============================================================
"""

import uuid
from datetime import datetime

from database.connection import get_connection
from etl.utils import logger


# ============================================================
# PIPELINE RUN IDENTIFIER
# ============================================================

def generate_pipeline_run_id() -> str:
    """
    Generate a unique identifier for an ETL pipeline execution.

    Returns
    -------
    str
        UUID string representing the current pipeline run.
    """

    return str(uuid.uuid4())


# ============================================================
# START PIPELINE RUN
# ============================================================

def start_pipeline_run(
    pipeline_name: str,
    load_type: str = "FULL",
) -> tuple[str, datetime]:
    """
    Register the start of an ETL pipeline execution.

    Parameters
    ----------
    pipeline_name : str
        Name of the ETL pipeline.

    load_type : str
        FULL or INCREMENTAL.

    Returns
    -------
    tuple[str, datetime]
        Pipeline run ID and pipeline start time.
    """

    pipeline_run_id = generate_pipeline_run_id()

    start_time = datetime.now()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO retail_dw.etl_metadata
        (
            pipeline_name,
            pipeline_run_id,
            load_type,
            start_time,
            status
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            'RUNNING'
        )
        """,
        (
            pipeline_name,
            pipeline_run_id,
            load_type,
            start_time,
        ),
    )

    connection.commit()

    cursor.close()
    connection.close()

    logger.info(
        "Pipeline execution registered (%s).",
        pipeline_run_id,
    )

    # --------------------------------------------------------
    # Return pipeline execution information
    # --------------------------------------------------------

    return (
        pipeline_run_id,
        start_time,
    )


# ============================================================
# END PIPELINE RUN
# ============================================================

def end_pipeline_run(
    pipeline_run_id: str,
    start_time: datetime,
    rows_processed: int,
    status: str = "SUCCESS",
    error_message: str | None = None,
) -> None:
    """
    Complete an ETL pipeline execution and update metadata.

    Parameters
    ----------
    pipeline_run_id : str
        Unique pipeline execution identifier.

    start_time : datetime
        Pipeline start timestamp.

    rows_processed : int
        Total number of rows processed during the run.

    status : str
        Pipeline execution status.
        Expected values: SUCCESS or FAILED.

    error_message : str | None
        Error message when the pipeline fails.
    """

    end_time = datetime.now()

    duration_seconds = (
        end_time - start_time
    ).total_seconds()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE retail_dw.etl_metadata
        SET
            end_time = %s,
            duration_seconds = %s,
            rows_processed = %s,
            status = %s,
            error_message = %s,
            last_successful_run = CASE
                WHEN %s = 'SUCCESS'
                THEN %s
                ELSE last_successful_run
            END
        WHERE pipeline_run_id = %s
        """,
        (
            end_time,
            round(duration_seconds, 2),
            rows_processed,
            status,
            error_message,
            status,
            end_time,
            pipeline_run_id,
        ),
    )

    connection.commit()

    cursor.close()
    connection.close()

    if status == "SUCCESS":

        logger.info(
            "Pipeline execution completed successfully (%s).",
            pipeline_run_id,
        )

    else:

        logger.error(
            "Pipeline execution failed (%s).",
            pipeline_run_id,
        )

