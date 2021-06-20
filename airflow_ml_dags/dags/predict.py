import json
import os
import pathlib
import sys
import pickle
from datetime import timedelta
import requests
import requests.exceptions as requests_exceptions

import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow import DAG
from airflow.models import TaskInstance
from airflow.models import Variable
import pandas as pd

DATA_FOLDER = "/opt/airflow/data/"


def get_data():
    """Function to gather all data"""
    time_folders = os.listdir(os.path.join(DATA_FOLDER, "raw"))
    F = pd.DataFrame()
    for case in time_folders:
        file = os.path.join(DATA_FOLDER, "raw", case, "data.csv")
        data = pd.read_csv(file)
        features = data.loc[:, data.columns != "target"]
        F = pd.concat([F, features])
    return F


def _model_predict(save_path):
    """Function to fit random forest

    Args:
        save_path: path of the model

    """
    data = get_data()
    path = Variable.get("model_name")
    path = os.path.join(DATA_FOLDER, "models", path, "model.pkl")
    with open(path, "rb") as f:
        classifier = pickle.load(f)
    predicts = classifier.predict(data)
    os.makedirs(save_path, exist_ok=True)
    save_path = os.path.join(save_path, "predictions.csv")
    pd.DataFrame(predicts).to_csv(save_path)


with DAG(
    dag_id="predict",
    start_date=airflow.utils.dates.days_ago(14),
    schedule_interval=timedelta(weeks=1),
) as dag:

    predict = PythonOperator(
        task_id="pred",
        python_callable=_model_predict,
        op_kwargs={
            "save_path": os.path.join(
                DATA_FOLDER,
                "predictions",
                "{{ execution_date.year }}_{{ execution_date.month }}_{{ execution_date.day }}_{{ execution_date.hour }}",
            )
        },
    )

    predict
