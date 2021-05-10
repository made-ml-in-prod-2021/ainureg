import pandas as pd
import os
import argparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

DEFAUlT_DATA_PATH = os.path.join("..", "data", "heart.csv")
random_seed = 42


def model_dit():
    data = pd.read_csv(DEFAUlT_DATA_PATH)
    X = data.loc[:, data.columns != 'target']
    y = data.loc[:, 'target']

    X_train, X_test, y_train, y_test = train_test_split( X,y, random_state = 42)
    classifier = RandomForestClassifier()
    classifier.fit(X_train, y_train)
    return classifier



def callback_build(arguments):
    return 0


def callback_predict(arguments):
    for query in arguments.query_file:
        query = query.strip()


def setup_parser(parser):
    subparsers = parser.add_subparsers(help='choose command')
    build_parser = subparsers.add_parser(
        "build", help='build model and save it',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    build_parser.add_argument(
        "-d", "--dataset",
        dest='dataset_path',
        default=DEFAUlT_DATA_PATH,
        help="path to dataset to load, def is %(default)s",
    )

    build_parser.add_argument(
        "-o", "--output",
        default=DEFAUlT_DATA_PATH,
        help="path to dataset to load",
    )
    build_parser.set_defaults(callback=callback_build)

    predict_parser = subparsers.add_parser(
        "apply", help='apply',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    predict_parser.set_defaults(callback=callback_predict)

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
    parser = argparse.ArgumentParser(
        prog='homework1',
        description='tool to build, load model or get information',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    setup_parser(parser)
    arguments = parser.parse_args()
    arguments.callback()
