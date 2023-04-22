"""
test/store/fixture/backend.py

Fixtures for backend unit tests.
"""

from pathlib import Path

import pytest

from mlte.store.backend import SessionHandle
from mlte.store.backend.engine import create_engine

# -----------------------------------------------------------------------------
# Filesystem Backend Fixtures
# -----------------------------------------------------------------------------


@pytest.fixture
def fs_handle(tmp_path: Path) -> SessionHandle:
    engine = create_engine(f"fs://{tmp_path}")
    engine.initialize()
    return engine.handle()
