"""
test/backend/fixture/api.py

Set up for store fixtures in API state.
"""

from __future__ import annotations

from typing import List, Optional

import pytest
from fastapi import FastAPI

import mlte.backend.app_factory as app_factory
import test.store.user.fixture as user_store_fixture
from mlte.backend.state import state
from mlte.store.user.store import UserStore
from mlte.user.model import Group, RoleType, UserCreate
from test.store.artifact import artifact_store_creators

TEST_ADMIN_USERNAME = "admin_user"
TEST_API_USERNAME = "api_user"
TEST_API_PASS = "api_pass"
"""User and passwords added to test the API."""

TEST_JWT_TOKEN_SECRET = "asdahsjh23423974hdasd"
"""JWT token secret used for signing tokens."""


def build_admin_user() -> UserCreate:
    """The default admin user."""
    return build_test_user(username=TEST_ADMIN_USERNAME, role=RoleType.ADMIN)


def build_test_user(
    username: str = TEST_API_USERNAME,
    password: str = TEST_API_PASS,
    role: Optional[RoleType] = None,
    groups: Optional[List[Group]] = None,
) -> UserCreate:
    """Creaters a test user."""
    test_user = UserCreate(username=username, password=password)
    if role:
        test_user.role = role
    if groups:
        test_user.groups = groups
    return test_user


def setup_api_with_mem_stores(user: UserCreate) -> FastAPI:
    """Setup API, configure to use memory artifact store and create app itself."""
    # Set up user store with test user.
    user_store = user_store_fixture.create_memory_store()
    user_store.session().user_mapper.create(user)

    # Always add an internal admin user.
    admin_user = build_admin_user()
    user_store.session().user_mapper.create(admin_user)

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
