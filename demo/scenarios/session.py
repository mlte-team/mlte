import os
from pathlib import Path

from mlte.session import set_context, set_store

# Suppress TensorFlow logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["XLA_FLAGS"] = "--xla_gpu_cuda_data_dir=/dev/null"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"

# This script sets up the session context used for all steps of this demo, as well as
# global constants about folders and model to use.

store_path = Path.cwd() / ".." / "store"

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
MODEL_FILE_PATH = MODELS_DIR / "oxford_flower_model.keras"

# This is the external script that will load and run the model for inference/prediction.
MODEL_COMMAND = [
    "python3",
    Path.cwd() / "model_predict.py",
    "--images",
    SAMPLE_DATASET_DIR,
    "--model",
    MODEL_FILE_PATH,
]
