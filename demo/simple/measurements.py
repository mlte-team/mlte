import os
import pickle
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn import datasets as sk_datasets
from sklearn import model_selection as sk_model_selection
from sklearn import tree as sk_tree

# The path at which datasets are stored
DATASETS_DIR = Path(os.getcwd()) / "data"
os.makedirs(DATASETS_DIR, exist_ok=True)

# The path at which models are stored
MODELS_DIR = Path(os.getcwd()) / "models"
os.makedirs(MODELS_DIR, exist_ok=True)

MODEL_PATH = MODELS_DIR / "model_demo.pkl"

# The path at which media is stored
MEDIA_DIR = Path(os.getcwd()) / "media"
os.makedirs(MEDIA_DIR, exist_ok=True)

IMAGE_PATH = MEDIA_DIR / "classes.png"

TRAIN_CMD = [
    "python3",
    Path.cwd() / "train.py",
    "--dataset-dir",
    str(DATASETS_DIR.absolute()),
    "--models-dir",
    str(MODELS_DIR.absolute()),
]

# ------------------------------------------------------------------------------
# Data and Model generic functions.
# ------------------------------------------------------------------------------


def load_data() -> tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    """
    Load machine learning dataset.
    :return (X_train, X_test, y_train, y_test)
    """
    iris = sk_datasets.load_iris(as_frame=True)
    X, y = iris.data, iris.target
    return sk_model_selection.train_test_split(X, y, test_size=0.2)


def train_model(X_train, y_train, model_path: str):
    """Train a classifier and save."""
    clf = sk_tree.DecisionTreeClassifier()
    clf.fit(X_train.to_numpy(), y_train.to_numpy())
    with open(model_path, "wb") as f:
        pickle.dump(clf, f)


def load_model(model_path: str):
    """Load a trained model."""
    with open(model_path, "rb") as f:
        return pickle.load(f)


# ------------------------------------------------------------------------------
# Data and Model generic functions.
# ------------------------------------------------------------------------------


def create_model() -> str:
    """Loads default data and saves it as csv, and trains and saves model."""
    # Save the training dataset for use by training procedure
    X_train, _, y_train, _ = load_data()
    X_train.to_csv(DATASETS_DIR / "data.csv")
    y_train.to_csv(DATASETS_DIR / "target.csv")

    # Train and save the model.
    train_model(X_train, y_train, MODEL_PATH)

    return MODEL_PATH


def create_image(y_pred):
    x = ["Setosa", "Versicolour", "Virginica"]
    y = [sum(1 for value in y_pred if value == target) for target in [0, 1, 2]]

    plt.bar(x, y)
    plt.title("Distribution of Predicted Classes")
    plt.xlabel("Class Label")
    plt.xticks([0, 1, 2])
    plt.ylabel("Occurrences")
    plt.savefig(IMAGE_PATH)

    return IMAGE_PATH


def predict(model_path: str):
    # Load the test dataset
    _, X_test, _, y_test = load_data()

    # Load the model
    model = load_model(model_path)

    # Make predictions
    y_pred = model.predict(X_test.to_numpy())

    return y_test, y_pred
