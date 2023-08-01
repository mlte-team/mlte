"""
test/store/support/backend/fs.py

Support functionality for filesystem-based backend tests.
"""

import shutil
import tempfile
from typing import Any, Dict


def create_temporary_directory(artifacts: Dict[str, Any]) -> None:
    """Create a temporary directory."""
    artifacts["tmp_path"] = tempfile.mkdtemp()


def construct_uri(artifacts: Dict[str, Any]) -> None:
    """Construct the filesystem URI."""
    assert "tmp_path" in artifacts, "Broken precondition."
    artifacts["uri"] = f"fs://{artifacts['tmp_path']}"


def delete_temporary_directory(artifacts: Dict[str, Any]) -> None:
    """Delete a temporary directory."""
    shutil.rmtree(artifacts["tmp_path"])
