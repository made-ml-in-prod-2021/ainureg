from marshmallow_dataclass import class_schema
from dataclasses import dataclass, field
from typing import List


from pathlib import Path

# CONFIG_PATH = (
#             "/home/ainur/Desktop/made/prod/hw/ainureg/ml_project/config/default.conf.yml"
#         )
CONFIG_PATH = (Path(__file__).parent.parent.parent / "config" / 'default.conf.yml').resolve()

import yaml


@dataclass()
class PipeParams:
    seed: int
    train_size: float
    DEFAULT_DATA_PATH: str
    FAKE_DATA_PATH: str
    DEFAULT_PREDICTS_SAVE_PATH: str
    COLUMNS: List[str] = field(
        default_factory=[
            "age",
            "sex",
            "cp",
            "trestbps",
            "chol",
            "fbs",
            "restecg",
            "thalach",
            "exang",
            "oldpeak",
            "slope",
            "ca",
            "thal",
            "target",
        ]
    )


PipeParamsSchema = class_schema(PipeParams)


def read_pipeline_params(path=CONFIG_PATH):
    with open(path, "r") as input_schema:
        schema = PipeParamsSchema()
        return schema.load(yaml.safe_load(input_schema))
