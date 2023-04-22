"""
test/store/fixture/http.py

Fixtures for HTTP unit tests.
"""

from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient

import mlte.store.app_factory as app_factory
from mlte.store.api.api import api_router
from mlte.store.api.dependencies import get_handle
from mlte.store.core.config import settings
from mlte.store.backend import SessionHandle
from mlte.store.backend.engine import create_engine

# -----------------------------------------------------------------------------
# Filesystem Backend Fixtures
# -----------------------------------------------------------------------------


@pytest.fixture(scope="function")
def fs_handle(tmp_path: Path) -> SessionHandle:
    """
    Get a session handle for filesystem backend.
    :param tmp_path: Temporary path
    :type path: Path
    :return: The session handle
    :rtype: SessionHandle
    """
    engine = create_engine(f"fs://{tmp_path}")
    engine.initialize()
    return engine.handle()


@pytest.fixture(scope="function")
def fs_client(fs_handle: SessionHandle) -> TestClient:
    """
    Get a TestClient instance configured for filesystem backend.
    :param fs_handle: T session handle
    :type fs_handle: SessionHandle
    :return: The configured client
    :rtype: TestClient
    """

    def _get_handle_override() -> Generator[SessionHandle, None, None]:
        try:
            yield fs_handle
        finally:
            fs_handle.close()

    app = app_factory.create()
    app.include_router(api_router, prefix=settings.API_PREFIX)
    app.dependency_overrides[get_handle] = _get_handle_override

    return TestClient(app)
