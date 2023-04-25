"""
test/store/fixture/http.py

Fixtures for HTTP unit tests.
"""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import mlte.store.app_factory as app_factory
from mlte.store.api.api import api_router
from mlte.store.core.config import settings
from mlte.store.backend import BackendEngine
from mlte.store.state import state
from mlte.store.backend.engine import create_engine

# -----------------------------------------------------------------------------
# Filesystem Backend Fixtures
# -----------------------------------------------------------------------------


@pytest.fixture(scope="function")
def fs_engine(tmp_path: Path) -> BackendEngine:
    """
    Get engine for filesystem backend.
    :param tmp_path: Temporary path
    :type path: Path
    :return: The engine
    :rtype: BackendEngine
    """
    return create_engine(f"fs://{tmp_path}")


@pytest.fixture(scope="function")
def fs_client(fs_engine: BackendEngine) -> TestClient:
    """
    Get a TestClient instance configured for filesystem backend.
    :param fs_engine: The engine
    :type fs_engine: BackendEngine
    :return: The configured client
    :rtype: TestClient
    """
    # Configure the engine
    state.set_engine(fs_engine)

    # Configure the application
    app = app_factory.create()
    app.include_router(api_router, prefix=settings.API_PREFIX)

    return TestClient(app)
