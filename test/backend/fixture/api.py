"""
test/backend/fixture/api.py

Set up for store fixtures in API state.
"""

from __future__ import annotations

import pytest
from fastapi import FastAPI

import mlte.backend.app_factory as app_factory
import test.store.user.fixture as user_store_fixture
from mlte.backend.state import state
from mlte.store.user.store import UserStore
from mlte.user.model import UserCreate
from test.store.artifact import artifact_store_creators

TEST_API_USER = "api_user"
TEST_API_PASS = "api_pass"
"""User and passwords added to test the API."""

TEST_JWT_TOKEN_SECRET = "asdahsjh23423974hdasd"
"""JWT token secret used for signing tokens."""


def setup_api_with_mem_stores() -> FastAPI:
    """Setup API, configure to use memory artifact store and create app itself."""
    # Set up user store with test user.
    user_store = user_store_fixture.create_memory_store()
    user_store.session().create_user(
        UserCreate(username=TEST_API_USER, password=TEST_API_PASS)
    )

    # Set the API state and app.
    state.set_user_store(user_store)
    state.set_artifact_store(artifact_store_creators.create_memory_store())
    state.set_token_key(TEST_JWT_TOKEN_SECRET)
    app = app_factory.create()
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
