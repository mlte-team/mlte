"""
demo/train.py

Simple model training script.
"""

import argparse
import logging
import pickle
import sys
from pathlib import Path
from typing import Tuple

import pandas as pd
from sklearn import tree

# Job exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# The name of the file in which training data is stored
DATA_FILENAME = "data.csv"
# The name of the file in which target classes are stored
TARGET_FILENAME = "target.csv"

# The name of the model file
MODEL_FILENAME = "model.pkl"


def parse_arguments() -> Tuple[Path, Path]:
    """
    Parse commandline arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset-dir",
        type=str,
        required=True,
        help="The path to the training dataset.",
    )
    parser.add_argument(
        "--models-dir",
        type=str,
        required=True,
        help="The path to which the model is saved.",
    )
    args = parser.parse_args()
    return Path(args.dataset_dir), Path(args.models_dir)


def load_dataset(path: Path) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Load a training dataset from `path`.
    :param path The path to the training dataset
    :return (X_train, y_train)
    """
    data_path = path / DATA_FILENAME
    if not data_path.is_file():
        raise RuntimeError(f"Not found: {data_path}.")
    X_train = pd.read_csv(data_path)

    target_path = path / TARGET_FILENAME
    if not target_path.is_file():
        raise RuntimeError(f"Not found: {target_path}.")
    y_train = pd.read_csv(target_path)

    return X_train, y_train


def train_model(X_train: pd.DataFrame, y_train: pd.Series):
    """
    Train a model on `X_train` and `y_train`.
    :param X_train The training data
    :param y_train The training target classes
    :return The fit classifier
    """
    # Simulate expensive training...
    for _ in range(1000):
        clf = tree.DecisionTreeClassifier()
        clf.fit(X_train.to_numpy(), y_train.to_numpy())
    return clf


def save_model(model, path: Path):
    """
    Save model `model` to `path`.
    :param model The model
    :param path The output path
    """
    with path.open("wb") as f:
        pickle.dump(model, f)


def main() -> int:
    dataset_dir, models_dir = parse_arguments()
    if not dataset_dir.is_dir():
        logging.error(f"Dataset directory {dataset_dir} not found.")
        return EXIT_FAILURE
    if not models_dir.is_dir():
        logging.error(f"Models directory {models_dir} not found.")
        return EXIT_FAILURE

    X_train, y_train = load_dataset(dataset_dir)

    model = train_model(X_train, y_train)
    save_model(model, models_dir / MODEL_FILENAME)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
