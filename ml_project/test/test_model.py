import csv
from pathlib import Path
from random import randint
import logging

import pytest
from sklearn.ensemble import RandomForestClassifier
import os

from . import app, read_pipeline_params, setup_logging

setup_logging()
logger = logging.getLogger("homework1")

columns = read_pipeline_params().COLUMNS


@pytest.fixture(scope="session")
def fake_params(tmpdir_factory):
    temp_folder = tmpdir_factory.mktemp("fake_data")
    fake_data_path = os.path.join(temp_folder, "faked_data.csv")
    params = read_pipeline_params()
    params.FAKE_DATA_PATH = fake_data_path
    return params


def test_fitting(fake_test_data):
    fake_model = app.model_fit(fake_test_data.FAKE_DATA_PATH)
    assert type(fake_model) == RandomForestClassifier


@pytest.fixture(scope="session")
def fake_test_data(fake_params):
    faked_data_path = fake_params.FAKE_DATA_PATH
    datagenerate(100, fake_data_path=faked_data_path)
    assert os.path.isfile(faked_data_path)
    return fake_params


def datagenerate(records: int, fake_data_path, headers=columns):
    with open(fake_data_path, "wt") as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=headers)
        writer.writeheader()
        for i in range(records):
            writer.writerow(
                {
                    "age": randint(19, 100),
                    "sex": randint(-1, 1),
                    "cp": randint(-1, 4),
                    "trestbps": randint(-1, 1000),
                    "chol": randint(-1, 1000),
                    "fbs": randint(-1, 1),
                    "restecg": randint(-1, 2),
                    "thalach": randint(-1, 1000),
                    "exang": randint(-1, 1),
                    "oldpeak": randint(-1, 10) / 10,
                    "slope": randint(-1, 2),
                    "ca": randint(-1, 4),
                    "thal": randint(-1, 3),
                    "target": randint(-1, 1),
                }
            )
        logger.info("fake data saved as %s", fake_data_path)
