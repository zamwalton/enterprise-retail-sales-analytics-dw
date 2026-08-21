"""
Enterprise Retail Sales Analytics Data Warehouse
Airflow DAG: Full ETL Pipeline
"""

from datetime import datetime

from airflow.sdk import DAG, task


with DAG(
    dag_id="retail_full_etl",
    description="Runs the Enterprise Retail Sales Full ETL pipeline",
    start_date=datetime(2026, 8, 20),
    schedule=None,
    catchup=False,
    tags=["retail", "etl", "full"],
) as dag:

    @task
    def run_full_etl():
        from etl.pipeline import run_pipeline

        run_pipeline()

    run_full_etl()