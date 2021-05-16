import pytest
from IPython import embed
from . import datagenerate, read_pipeline_params, setup_logging
import pandas as pd
from pathlib import Path
import os

params = read_pipeline_params()

setup_logging()

def test_data_class():
    for param in ["seed", "train_size"]:
        assert param in params.__dataclass_fields__.keys()
    assert params.seed == 42
    # embed()


def test_fake_data():
    n = 100
    datagenerate(n)
    # params = read_pipeline_params()
    this = Path(__file__).resolve()
    fake_data_path = str((this.parent.parent / params.FAKE_DATA_PATH).resolve())
    assert os.path.isfile(fake_data_path)
    fake_data = pd.read_csv(fake_data_path)
    assert fake_data.shape[0] == n

    # embed()
