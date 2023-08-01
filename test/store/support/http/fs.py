"""
test/store/support/http/fs.py

Support functions for filesystem backend tests.
"""

import shutil
import tempfile
from typing import Any, Dict


def create_temporary_directory(artifacts: Dict[str, Any]) -> None:
    """Create a temporary directory."""
    artifacts["tmp_path"] = tempfile.mkdtemp()


def create_store_uri(artifacts: Dict[str, Any]) -> None:
    """Creates the key for the backend store URI."""
    artifacts["uri"] = f"file://{artifacts['tmp_path']}"


def delete_temporary_directory(artifacts: Dict[str, Any]) -> None:
    """Delete a temporary directory."""
    shutil.rmtree(artifacts["tmp_path"])
