import os
from datetime import timedelta
import pathlib

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
import airflow.utils.dates
from airflow.models import TaskInstance
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from airflow.utils.dates import days_ago

import sys
system_path  = pathlib.Path(__file__).parent.parent.resolve()
print("system path is", system_path)
sys.path.append(str(system_path))

print(sys.path)
from ml_project.test.test_model import datagenerate


# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(2),
    "email": ["airflow@example.com"],
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

def _get_data(
    year: str,
    month: str,
    day: str,
    hour: str,
    task_instance: TaskInstance,
    execution_date,
    output_dir: str = "/opt/airflow/data",
):
    data_folder = os.path.join(output_dir, "raw", f"{year}_{month}_{day}_{hour}", )
    pathlib.Path(data_folder).mkdir(parents=True, exist_ok=True)

    datagenerate(100, os.path.join(data_folder,"data.csv"))

with DAG(
    dag_id="data_generate",
    default_args=default_args,
    description="A simple tutorial DAG",
    schedule_interval=timedelta(minutes=2),
) as dag:

    get_data = PythonOperator(
        task_id="get_data",
        python_callable=_get_data,
        op_kwargs={
            "year": "{{ execution_date.year }}",
            "month": "{{ execution_date.month }}",
            "day": "{{ execution_date.day }}",
            "hour": "{{ execution_date.hour }}",
            "output_dir": "/opt/airflow/data",
        }
    )

    bash_example = BashOperator(
        task_id="bash_command", bash_command="echo {{ ds }}",
    )

    bash_example >> get_data
