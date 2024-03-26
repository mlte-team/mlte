"""
test/backend/fixture/api.py

Set up for store fixtures in API state.
"""

from __future__ import annotations

import pytest
from fastapi import FastAPI

import mlte.backend.app_factory as app_factory
import test.store.user.fixture as user_store_fixture
from mlte.backend.api.api import api_router
from mlte.backend.core.config import settings
from mlte.backend.state import state
from mlte.store.user.store import UserStore
from test.store.artifact import artifact_store_creators


def setup_api_with_mem_stores() -> FastAPI:
    """Setup API, configure to use memory artifact store and create app itself."""
    state.set_artifact_store(artifact_store_creators.create_memory_store())
    state.set_user_store(user_store_fixture.create_memory_store())
    app = app_factory.create()
    app.include_router(api_router, prefix=settings.API_PREFIX)
    return app


def set_user_store_in_state(
    store_fixture_name: str, request: pytest.FixtureRequest
):
    """Sets an provided fixture user store in the backend state."""
    user_store: UserStore = request.getfixturevalue(store_fixture_name)
    state.set_user_store(user_store)


def clear_state():
    """Clears the the backend state."""
    state._artifact_store = None
    state._user_store = None
