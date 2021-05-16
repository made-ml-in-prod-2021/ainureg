#!/usr/bin/env python3
"""TOOL TO BUILD AND EVALUATE MODEL
"""
# -*- coding: utf-8 -*-
import os
import logging
import argparse
from datetime import datetime
import pickle

from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from IPython import embed
from .data.configs import read_pipeline_params
from .utils import setup_logging

params = read_pipeline_params()

# DEFAULT_DATA_PATH = os.path.join("data", "heart.csv")
DEFAULT_MODEL_SAVE_PATH = os.path.join(
    "model", datetime.now().strftime("%y-%m-%d-%H-%m-%s") + ".pickle"
)
random_seed = 42

APP_NAME = "homework1"
logger = logging.getLogger(APP_NAME)


def model_fit(data_path: str) -> RandomForestClassifier:
    """Function to fit random forest

        Args:
        data_path: path to data

    Returns:
        fitted model

    """
    data = pd.read_csv(data_path)
    X = data.loc[:, data.columns != "target"]
    y = data.loc[:, "target"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=random_seed)
    classifier = RandomForestClassifier()
    classifier.fit(X_train, y_train)
    logger.info("Model fit!")
    return classifier


def callback_fit(arguments):
    logger.info("good job")
    return 0


def build_processing(data_path, save_path):
    model = model_fit(data_path)
    with open(save_path, "wb") as f:
        pickle.dump(model, f)
    logger.info("Model saved as %s", save_path)


def callback_build(arguments):
    logger.info("building model is started")
    return build_processing(arguments.data_path, arguments.output)


def callback_predict(arguments):
    # print("123")
    for query in arguments.query_file:
        query = query.strip()


def setup_parser(parser):

    subparsers = parser.add_subparsers(help="choose command")

    build_parser = subparsers.add_parser(
        "build",
        help="build model and save it",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    build_parser.add_argument(
        "-d",
        "--data",
        dest="data_path",
        default=params.DEFAULT_DATA_PATH,
        help="path to data to load, def is %(default)s",
    )

    build_parser.add_argument(
        "-o",
        "--output",
        default=DEFAULT_MODEL_SAVE_PATH,
        help="path to save model",
    )
    build_parser.set_defaults(callback=callback_build)

    predict_parser = subparsers.add_parser(
        "apply",
        help="apply",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    predict_parser.set_defaults(callback=callback_predict)

    fit_parser = subparsers.add_parser(
        "fit",
        help="fitting",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    fit_parser.set_defaults(callback=callback_fit)

    # parser.add_argument(
    #     "-d", "--dataset", dest='dataset_path',
    #     metavar='FANCY_PATH', default='/hz/hz.txt',
    #     help="path to dataset to load, def is %(default)s",
    #     required=True,
    # )
    #
    # parser.add_argument(
    #     "-q", "--query", dest='dataset_path',
    #     metavar='FANCY_PATH', nargs="+",
    #     help="path to dataset to load",
    # )


if __name__ == "__main__":
    setup_logging()
    parser = argparse.ArgumentParser(
        prog="homework1",
        description="tool to build, load model or get information",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    setup_parser(parser)
    arguments = parser.parse_args()
    arguments.callback(arguments)
