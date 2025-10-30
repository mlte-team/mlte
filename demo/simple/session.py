import os
from pathlib import Path

from mlte.session import set_context, set_store

# This script sets up the session context used for all steps of this demo, as well as
# global constants about folders and model to use.

store_path = Path.cwd() / ".." / "store"

set_context("IrisClassifier", "0.0.1")
set_store(f"local://{store_path}")

# Constants to be used in this demo.
BASE_FOLDER = Path(os.getcwd()) / "temp"

# The path at which datasets are stored
DATASETS_DIR = BASE_FOLDER / "data"
INPUT_PATH = DATASETS_DIR / "data.csv"
OUTPUT_PATH = DATASETS_DIR / "target.csv"

# The path at which models are stored
MODELS_DIR = BASE_FOLDER / "models"
MODEL_PATH = MODELS_DIR / "model_demo.pkl"

# The path at which media is stored
MEDIA_DIR = BASE_FOLDER / "media"
IMAGE_PATH = MEDIA_DIR / "classes.png"

# Command to be used to train the model.
TRAIN_CMD = [
    "python3",
    Path.cwd() / "train.py",
    "--dataset-dir",
    str(DATASETS_DIR.absolute()),
    "--models-dir",
    str(MODELS_DIR.absolute()),
]
