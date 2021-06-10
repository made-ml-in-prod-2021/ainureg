#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import requests


csv_fl = "/home/ainur/Desktop/made/prod/hw/ainureg/ml_project/data/fake_data.csv"

if __name__ == "__main__":

    data = pd.read_csv(csv_fl)
    data = data.drop(['target'], axis = 1)
    request_features = ["Id"] + list(data.columns)
    for i in range(100):
        request_data = [
            x.item() if isinstance(x, np.generic) else x for x in data.iloc[i].tolist()
        ]
        request_data = [i] + request_data
        print(request_data)
        response = requests.get(
            "http://0.0.0.0:80/predict/",
            json={"data": [request_data], "features": request_features},
        )
        print(response.status_code)
        print(response.json())
