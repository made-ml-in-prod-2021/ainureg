import os
from datetime import timedelta
import pathlib
import sys

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

system_path = pathlib.Path(__file__).parent.parent.resolve()
sys.path.append(str(system_path))
from ml_project.test.test_model import datagenerate

DATA_FODLER = "/opt/airflow/data"


def _get_data(
    year: str,
    month: str,
    day: str,
    hour: str,
    output_dir: str,
):
    full_data_folder = os.path.join(
        output_dir,
        "raw",
        f"{year}_{month}_{day}_{hour}",
    )
    pathlib.Path(full_data_folder).mkdir(parents=True, exist_ok=True)
    datagenerate(100, os.path.join(full_data_folder, "data.csv"))


with DAG(
    dag_id="data_generate",
    start_date=days_ago(2),
    description="new data generating dag",
    schedule_interval=timedelta(hours=1),
) as dag:

    get_data = PythonOperator(
        task_id="get_data",
        python_callable=_get_data,
        op_kwargs={
            "year": "{{ execution_date.year }}",
            "month": "{{ execution_date.month }}",
            "day": "{{ execution_date.day }}",
            "hour": "{{ execution_date.hour }}",
            "output_dir": DATA_FODLER,
        },
    )

    get_data