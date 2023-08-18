"""
test/web/store/fixture/http.py

Fixtures for artifact store HTTP unit tests.
"""

from __future__ import annotations

from typing import Generator, Tuple

import pytest
from fastapi.testclient import TestClient

import mlte.web.store.app_factory as app_factory
from mlte.artifact.type import ArtifactType
from mlte.store.factory import create_store
from mlte.web.store.api.api import api_router
from mlte.web.store.core.config import settings
from mlte.web.store.state import state

"""
This list contains the global collection of test clients.
However, because we cannot directly parametrize a test with
a fixture function, we specify via strings and then use the
`request` fixture to translate this into the actual fixture.
"""
_CLIENTS = ["mem_client"]

# -----------------------------------------------------------------------------
# Store Backend Fixtures
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


def clients() -> Generator[str, None, None]:
    """
    Yield test clients.
    :return: A test client configured for backend
    """
    for client in _CLIENTS:
        yield client


def clients_and_types() -> Generator[Tuple[str, ArtifactType], None, None]:
    """
    Yield test clients and artifact types to produce all combinations.
    :return: (test client configured for backend, artifact type)
    """
    for client in _CLIENTS:
        for type in ArtifactType:
            yield client, type
