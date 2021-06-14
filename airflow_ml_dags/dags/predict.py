 
import json
import os
import pathlib
import sys

import airflow
import requests
import requests.exceptions as requests_exceptions
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import pandas as pd
from datetime import timedelta
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
import airflow.utils.dates
from airflow import DAG
from airflow.models import TaskInstance

data_folder = "/opt/airflow/data/"

from airflow.models import Variable
# returns the key `test_var` from the table `variable`

def get_data():
    print(os.listdir(data_folder))
    print(os.getcwd())
    print(sys.path)
    time_folders = os.listdir(os.path.join(data_folder, "raw"))
    F = pd.DataFrame()
    for case in time_folders:
        file = os.path.join(data_folder, "raw",case,  "data.csv")
        data = pd.read_csv(file)
        target = data["target"].astype(int)
        features = data.loc[:, data.columns != "target"]
        F = pd.concat([F,features])


    return F



def _model_predict(save_path):
    """Function to fit random forest

        Args:
        data_path: path to data

    Returns:
        fitted model

    """
    data = get_data()
    path = Variable.get("model_name")
    path = os.path.join(data_folder, 'models', path, 'model.pkl')
    with open( path,  "rb") as f:
        classifier = pickle.load(f)
    predicts = classifier.predict(data)
    os.makedirs(save_path,exist_ok=True )
    save_path = os.path.join(save_path, 'predictions.csv')
    pd.DataFrame(predicts).to_csv(save_path )


with DAG(
    dag_id="predict",
    start_date=airflow.utils.dates.days_ago(14),
    schedule_interval=timedelta(weeks=1),
) as dag:


    predict = PythonOperator(
        task_id="pred",
        python_callable=_model_predict,
        op_kwargs={
            "save_path": "/opt/airflow/data/predictions/"
            + "{{ execution_date.year }}_{{ execution_date.month }}_{{ execution_date.day }}_{{ execution_date.hour }}",
        },
    )



    predict