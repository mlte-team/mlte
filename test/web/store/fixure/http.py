"""
test/web/store/fixture/http.py

Fixtures for artifact store HTTP unit tests.
"""

import pytest
from fastapi.testclient import TestClient

import mlte.web.store.app_factory as app_factory
from mlte.store.factory import create_store
from mlte.web.store.api.api import api_router
from mlte.web.store.core.config import settings
from mlte.web.store.state import state

# -----------------------------------------------------------------------------
# Filesystem Backend Fixtures
# -----------------------------------------------------------------------------


@pytest.fixture(scope="function")
def mem_client() -> TestClient:
    """
    Get a TestClient instance configured for an in-memory store.
    :return: The configured client
    """
    # Configure the backing store
    state.set_store(create_store("memory://"))

    # Configure the application
    app = app_factory.create()
    app.include_router(api_router, prefix=settings.API_PREFIX)
    return TestClient(app)
