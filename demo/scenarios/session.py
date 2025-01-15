import os
from pathlib import Path

from mlte.session import set_context, set_store

# This script sets up the session context used for all steps of this demo, as well as
# global constants about folders and model to use.

store_path = Path.cwd() / "store"
os.makedirs(store_path, exist_ok=True)

set_context("OxfordFlower", "0.0.1")
set_store(f"local://{store_path}")

# The path at which datasets are stored
DATASETS_DIR = Path.cwd() / "data"

# Path for the data set of known good samples
SAMPLE_DATASET_DIR = DATASETS_DIR / "sample"

# Path for the data set of out of distribution samples
OOD_DATASET_DIR = DATASETS_DIR / "ood"

# Path where the model files are stored.
MODELS_DIR = Path.cwd() / "model"

# The path at which media is stored
MEDIA_DIR = Path.cwd() / "media"
os.makedirs(MEDIA_DIR, exist_ok=True)

# The json file of the model to load
MODEL_FILE_PATH = MODELS_DIR / "model_f3_a.json"

# The weights file for the model
MODEL_WEIGHTS_PATH = MODELS_DIR / "oxford_flower_model_v6.testing.keras"

# This is the external script that will load and run the model for inference/prediction.
MODEL_SCRIPT = Path.cwd() / "model_predict.py"
MODEL_ARGS = [
    "--images",
    SAMPLE_DATASET_DIR,
    "--model",
    MODEL_FILE_PATH,
    "--weights",
    MODEL_WEIGHTS_PATH,
]
