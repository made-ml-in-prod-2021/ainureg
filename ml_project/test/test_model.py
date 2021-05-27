import pytest
from sklearn.ensemble import RandomForestClassifier
import os

from . import datagenerate, app, read_pipeline_params, setup_logging


@pytest.fixture(scope="session")
def fake_params(tmpdir_factory):
    temp_folder = tmpdir_factory.mktemp("fake_data")
    fake_data_path = os.path.join(temp_folder, "faked_data.csv")
    params = read_pipeline_params()
    params.FAKE_DATA_PATH = fake_data_path
    return params


def test__test(fake_test_data):
    fake_model = app.model_fit(fake_test_data.FAKE_DATA_PATH)
    assert type(fake_model) == RandomForestClassifier


@pytest.fixture(scope="session")
def fake_test_data(fake_params):
    faked_data_path = fake_params.FAKE_DATA_PATH
    datagenerate(100, fake_data_path=faked_data_path)
    assert os.path.isfile(faked_data_path)
    return fake_params
