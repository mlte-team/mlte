from pathlib import Path

from mlte.session import set_context, set_store

# This script sets up the session context used for all steps of this demo, as well as
# global constants about folders and model to use.

store_path = Path.cwd() / ".." / "store"

set_context("IrisClassifier", "0.0.1")
set_store(f"local://{store_path}")
