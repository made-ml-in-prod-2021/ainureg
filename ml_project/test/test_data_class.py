from . import read_pipeline_params, setup_logging
from .test_model import datagenerate
import pandas as pd
import os

params = read_pipeline_params()


def test_data_class():
    for param in ["seed", "train_size"]:
        assert param in params.__dataclass_fields__.keys()
    assert params.seed == 42


def test_fake_data(tmpdir_factory):
    temp_folder = tmpdir_factory.mktemp("fake_data")
    fake_data_path = os.path.join(temp_folder, "faked_data.csv")
    n = 100
    datagenerate(n, fake_data_path=fake_data_path)
    fake_data = pd.read_csv(fake_data_path)
    assert fake_data.shape[0] == n
