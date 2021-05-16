import csv
from random import random, randint
from pathlib import Path
from .configs import read_pipeline_params
import logging

params = read_pipeline_params()
fake_data_path = params.FAKE_DATA_PATH

this = Path(__file__).resolve()
fake_data_path = str((this.parent.parent.parent / fake_data_path).resolve())

columns = [
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


logger = logging.getLogger("homework1")

def datagenerate(records: int, headers=columns):
    with open(fake_data_path, "wt") as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=headers)
        writer.writeheader()
        for i in range(records):
            writer.writerow(
                {
                    "age": randint(20, 100),
                    "sex": randint(0, 1),
                    "cp": randint(0, 4),
                    "trestbps": randint(0, 1000),
                    "chol": randint(0, 1000),
                    "fbs": randint(0, 1),
                    "restecg": randint(0, 2),
                    "thalach": randint(0, 1000),
                    "exang": randint(0, 1),
                    "oldpeak": randint(0, 10) / 10,
                    "slope": randint(0, 2),
                    "ca": randint(0, 4),
                    "thal": randint(0, 3),
                    "target": randint(0, 1)
                }
            )

        logger.info("fake data saved as %s", str(Path(fake_data_path).resolve()))
