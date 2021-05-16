from marshmallow_dataclass import class_schema
from dataclasses import dataclass
CONFIG_PATH = "/home/ainur/Desktop/made/prod/hw/ainureg/ml_project/config/default.conf.yml"
import yaml


@dataclass()
class PipeParams:
    seed: int
    train_size: float
    DEFAULT_DATA_PATH: str
    FAKE_DATA_PATH: str

PipeParamsSchema = class_schema(PipeParams)

def read_pipeline_params(path=CONFIG_PATH):
    with open(path, "r") as input_schema:
        schema = PipeParamsSchema()
        return schema.load(yaml.safe_load(input_schema))
