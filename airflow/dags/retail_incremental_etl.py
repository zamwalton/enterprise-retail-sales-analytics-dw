"""
Enterprise Retail Sales Analytics Data Warehouse
Airflow DAG: Incremental ETL Pipeline
"""

from datetime import datetime

from airflow.sdk import DAG, task


with DAG(
    dag_id="retail_incremental_etl",
    description="Runs the Enterprise Retail Sales Incremental ETL pipeline",
    start_date=datetime(2026, 8, 20),
    schedule=None,
    catchup=False,
    tags=["retail", "etl", "incremental"],
) as dag:

    @task
    def run_incremental_etl():
        from etl.incremental.pipeline import run_incremental_pipeline

        run_incremental_pipeline()

    run_incremental_etl()