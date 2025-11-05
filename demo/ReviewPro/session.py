from dotenv import load_dotenv
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
# store_path = Path.cwd() / ".." / "store/models"

set_context("ReviewPro", "0.0.1")
set_store(f"local://{store_path}")

# The path at which datasets are stored
DATASETS_DIR = Path.cwd() / "data"

load_dotenv()
api_key = os.getenv("API_KEY")