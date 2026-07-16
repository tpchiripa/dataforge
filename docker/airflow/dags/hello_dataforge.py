from datetime import datetime

from airflow.operators.empty import EmptyOperator

from airflow import DAG

with DAG(
    dag_id="hello_dataforge",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["dataforge"],
) as dag:

    start = EmptyOperator(task_id="start")
    finish = EmptyOperator(task_id="finish")

    start >> finish

