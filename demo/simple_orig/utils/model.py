import os
import pickle

import matplotlib.pyplot as plt
import pandas as pd
from sklearn import datasets as sk_datasets
from sklearn import model_selection as sk_model_selection
from sklearn import tree as sk_tree

from demo.simple.session import *

# ------------------------------------------------------------------------------
# Data and Model generic functions.
# ------------------------------------------------------------------------------


def _load_data_from_lib() -> (
    tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]
):
    """
    Load machine learning dataset.
    :return (X_train, X_test, y_train, y_test)
    """
    iris = sk_datasets.load_iris(as_frame=True)
    X, y = iris.data, iris.target
    return sk_model_selection.train_test_split(X, y, test_size=0.2)


def _load_model(model_path: str):
    """Load a trained model."""
    with open(model_path, "rb") as f:
        return pickle.load(f)


def _train_model(model_path: str):
    """Train a classifier and save."""
    X_train, _, y_train, _ = _load_data_from_lib()
    clf = sk_tree.DecisionTreeClassifier()
    clf.fit(X_train.to_numpy(), y_train.to_numpy())
    with open(model_path, "wb") as f:
        pickle.dump(clf, f)


# ------------------------------------------------------------------------------
# Helper functions specific for this demo.
# ------------------------------------------------------------------------------


def create_folders():
    """Creates folders needed for using the model."""
    os.makedirs(DATASETS_DIR, exist_ok=True)
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(MEDIA_DIR, exist_ok=True)


def save_training_datasets_to_csv():
    """Save the training dataset for use by this model."""
    X_train, _, y_train, _ = _load_data_from_lib()
    X_train.to_csv(INPUT_PATH)
    y_train.to_csv(OUTPUT_PATH)


def create_model() -> str:
    """Trains and saves model for this demo."""
    _train_model(MODEL_PATH)
    return MODEL_PATH


def predict(model_path: str):
    """Try out model inference with default dataset."""
    # Load data and model.
    _, X_test, _, y_test = _load_data_from_lib()
    loaded_model = _load_model(model_path)

    # Predict and return.
    y_pred = loaded_model.predict(X_test.to_numpy())
    return y_test, y_pred


def create_image(y_pred):
    """Helper function to create a plot image for this dataset."""
    x = ["Setosa", "Versicolour", "Virginica"]
    y = [sum(1 for value in y_pred if value == target) for target in [0, 1, 2]]

    plt.bar(x, y)
    plt.title("Distribution of Predicted Classes")
    plt.xlabel("Class Label")
    plt.xticks([0, 1, 2])
    plt.ylabel("Occurrences")
    plt.savefig(IMAGE_PATH)

    return IMAGE_PATH
