import pytest
from sklearn.ensemble import RandomForestClassifier
import os
from pathlib import Path

from . import datagenerate, app, read_pipeline_params, setup_logging

params = read_pipeline_params()

datagenerate(100)

def test__test():
    this = Path(__file__).resolve()
    fake_data_path = str((this.parent.parent / params.FAKE_DATA_PATH).resolve())
    assert os.path.isfile(fake_data_path)
    fake_model = app.model_fit(fake_data_path)
    assert type(fake_model)==RandomForestClassifier
