from pathlib import Path
from .configs import read_pipeline_params

params = read_pipeline_params()
fake_data_path = params.FAKE_DATA_PATH

this = Path(__file__).resolve()
fake_data_path = str((this.parent.parent.parent / fake_data_path).resolve())

from IPython import embed

embed()
