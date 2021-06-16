import os
import sys
import requests
import requests.exceptions as requests_exceptions
import pickle
from datetime import timedelta

import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import airflow.utils.dates
from airflow import DAG
from airflow.models import TaskInstance

data_folder = "/opt/airflow/data/"


def _preprocessing():
    print(os.listdir(data_folder))
    print(os.getcwd())
    print(sys.path)
    time_folders = os.listdir(os.path.join(data_folder, "raw"))
    for case in time_folders:
        file = os.path.join(data_folder, "raw", case, "data.csv")
        data = pd.read_csv(file)
        target = data["target"].astype(int)
        features = data.loc[:, data.columns != "target"]
        new_folder = os.path.join(data_folder, "processed", case)
        os.makedirs(new_folder, exist_ok=True)
        target.to_csv(os.path.join(new_folder, "target.csv"), index=False)
        features.to_csv(os.path.join(new_folder, "train_data.csv"), index=False)


def _split_data():

    time_folders = os.listdir(os.path.join(data_folder, "processed"))
    F = pd.DataFrame()
    T = pd.DataFrame()
    for case in time_folders:
        feat = os.path.join(data_folder, "processed", case, "train_data.csv")
        F = pd.concat([F, pd.read_csv(feat)])

        target = os.path.join(data_folder, "processed", case, "target.csv")
        T = pd.concat([T, pd.read_csv(target)])
    os.makedirs(os.path.join(data_folder, "split"), exist_ok=True)
    f_train, f_val = train_test_split(F)
    t_train, t_val = train_test_split(T)

    t_train.to_csv(
        os.path.join(data_folder, "split", "target_train.csv"), index_label=False
    )
    t_val.to_csv(
        os.path.join(data_folder, "split", "target_val.csv"), index_label=False
    )
    f_train.to_csv(
        os.path.join(data_folder, "split", "features_train.csv"), index_label=False
    )
    f_val.to_csv(
        os.path.join(data_folder, "split", "features_val.csv"), index_label=False
    )


def model_fit(
    data_path: str, target_path: str, save_path: str
) -> RandomForestClassifier:
    """Function to fit random forest

        Args:
        data_path: path to data

    Returns:
        fitted model

    """
    X_train, y_train = pd.read_csv(data_path), pd.read_csv(target_path)
    y_train = y_train.astype(int)

    classifier = RandomForestClassifier()
    classifier.fit(X_train, y_train)
    folder = os.path.join(data_folder, "model", save_path)
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "model.pkl")
    with open(path, "wb") as f:
        pickle.dump(classifier, f)
    return classifier


def model_validate(
    data_path: str, target_path: str, save_path: str, model: RandomForestClassifier
) -> RandomForestClassifier:
    """Function to fit random forest

    Args:
        data_path: path to feature
        target_path: path to targets
        save_path: the path of the model we validate


    """
    X_val, y_val = pd.read_csv(data_path), pd.read_csv(target_path)
    y_val = y_val.astype(int)
    score = model.score(X_val, y_val)
    file = os.path.join(data_folder, "model", save_path, "score.txt")
    with open(file, "w") as f:
        print("score: ", score, file=f)


def _model_fit(save_path: str) -> RandomForestClassifier:
    """Function to fit random forest

        Args:
        save_path: path to data

    Returns:
        fitted model

    """
    t_train = os.path.join(data_folder, "split", "target_train.csv")
    f_train = os.path.join(data_folder, "split", "features_train.csv")
    t_val = os.path.join(data_folder, "split", "target_val.csv")
    f_val = os.path.join(data_folder, "split", "features_val.csv")

    model = model_fit(f_train, t_train, save_path)
    model_validate(f_val, t_val, save_path, model)


with DAG(
    dag_id="pipeline",
    start_date=airflow.utils.dates.days_ago(14),
    schedule_interval=timedelta(weeks=1),
) as dag:

    preprocessing = PythonOperator(
        task_id="preprocessing",
        python_callable=_preprocessing,
    )
    split = PythonOperator(
        task_id="split",
        python_callable=_split_data,
    )

    fit = PythonOperator(
        task_id="fit_model",
        python_callable=_model_fit,
        op_kwargs={
            "save_path": "/opt/airflow/data/models/"
            + "{{ execution_date.year }}_{{ execution_date.month }}_{{ execution_date.day }}_{{ execution_date.hour }}",
        },
    )

    preprocessing >> split >> fit
