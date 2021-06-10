import logging
import os
import pickle
from typing import List, Union, Optional

import numpy as np
import pandas as pd
import uvicorn
from pydantic import BaseModel, conlist
from sklearn.ensemble import RandomForestClassifier

from fastapi import FastAPI

logger = logging.getLogger(__name__)

app = FastAPI()


class DataClass(BaseModel):
    data: List[conlist(Union[float, str, None], min_items=14, max_items=14)]
    features: List[str]


class TargetResponse(BaseModel):
    id: str
    target: int


model: Optional[RandomForestClassifier] = None


def make_predict(data: List, features: List[str], model: model) -> List[TargetResponse]:
    data = pd.DataFrame(data, columns=features)
    ids = [int(x) for x in data["Id"]]
    data=data.drop(["Id"], axis = 1)
    predicts = np.exp(model.predict(data))

    return [
        TargetResponse(id=id_, target=int(target)) for id_, target in zip(ids, predicts)
    ]


def load_object(path: str) -> model:
    with open(path, "rb") as f:
        return pickle.load(f)


@app.get("/")
async def root():
    return {"message": "Hello world, my homework is here"}


@app.on_event("startup")
def load_model():
    global model

    # model_path = os.getenv("PATH_TO_MODEL")
    model_path = "ml_project/model/21-05-14-23-05-1621024492.pickle"
    if model_path is None:
        err = f"serialization_path {model_path} is None"
        logger.error(err)
        raise RuntimeError(err)
    model = load_object(model_path)


@app.get("/predict/", response_model=List[TargetResponse])
def predict(request: DataClass):
    return make_predict(request.data, request.features, model)


if __name__ == "__main__":
    uvicorn.run("app:app", host="0,0,0,0", port=os.getenv("PORT", 8000))
