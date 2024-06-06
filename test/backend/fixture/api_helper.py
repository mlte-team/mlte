"""
test/backend/fixture/api.py

Set up for store fixtures in API state.
"""

from __future__ import annotations

import typing
from typing import List, Optional

import pytest
from fastapi import FastAPI

import mlte.backend.app_factory as app_factory
import test.store.user.fixture as user_store_fixture
from mlte.backend.state import state
from mlte.store.user.policy import Policy
from mlte.store.user.store import UserStore
from mlte.store.user.underlying.memory import InMemoryUserMapper
from mlte.user import passwords
from mlte.user.model import Group, ResourceType, RoleType, User, UserWithPassword
from test.store.artifact import artifact_store_creators

TEST_ADMIN_USERNAME = "admin_user"
TEST_API_USERNAME = "api_user"
TEST_API_PASS = "api_pass"
TEST_API_HASHED_PASS = passwords.hash_password(TEST_API_PASS)
"""User and passwords added to test the API."""

TEST_JWT_TOKEN_SECRET = "asdahsjh23423974hdasd"
"""JWT token secret used for signing tokens."""


def build_admin_user() -> UserWithPassword:
    """The default admin user."""
    return build_test_user(username=TEST_ADMIN_USERNAME, role=RoleType.ADMIN)


def build_test_user(
    username: str = TEST_API_USERNAME,
    password: str = TEST_API_PASS,
    role: Optional[RoleType] = None,
    groups: Optional[List[Group]] = None,
) -> UserWithPassword:
    """Creaters a test user."""
    test_user = UserWithPassword(username=username, password=password)
    if role:
        test_user.role = role
    if groups:
        test_user.groups = groups
    return test_user


def setup_api_with_mem_stores(user: UserWithPassword) -> FastAPI:
    """Setup API, configure to use memory artifact store and create app itself."""
    # Set up user store with test user.
    user_store = user_store_fixture.create_memory_store()
    # NOTE: Totally ignores interface and does this directly to avoid hashing password each time, to speed up tests.
    # This assumes the user received will have the default API password.
    typing.cast(
        InMemoryUserMapper, user_store.session().user_mapper
    ).storage.users[user.username] = User(
        hashed_password=TEST_API_HASHED_PASS, **user.model_dump()
    )

    # Always add an internal admin user.
    admin_user = build_admin_user()
    # NOTE: same as above.
    typing.cast(
        InMemoryUserMapper, user_store.session().user_mapper
    ).storage.users[admin_user.username] = User(
        hashed_password=TEST_API_HASHED_PASS, **admin_user.model_dump()
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


def get_test_users_with_read_permissions(
    resource_type: ResourceType, resource_id: Optional[str] = None
) -> List[UserWithPassword]:
    """Get a list of users that have permissions to read from different sources."""
    users = [
        build_test_user(role=RoleType.ADMIN),
        build_test_user(groups=Policy.build_groups(resource_type)),
        build_test_user(
            groups=Policy.build_groups(resource_type, build_write_group=False)
        ),
    ]

    # Add user with all permissions for this type/id, and one with only read permissions.
    if resource_id is not None:
        users.append(
            build_test_user(
                groups=Policy.build_groups(resource_type, resource_id)
            )
        )
        users.append(
            build_test_user(
                groups=Policy.build_groups(
                    resource_type, resource_id, build_write_group=False
                )
            )
        )

    return users


def get_test_users_with_write_permissions(
    resource_type: ResourceType, resource_id: Optional[str] = None
) -> List[UserWithPassword]:
    """Get a list of users that have permissions to write from different sources."""
    users = [
        build_test_user(role=RoleType.ADMIN),
        build_test_user(groups=Policy.build_groups(resource_type)),
        build_test_user(
            groups=Policy.build_groups(resource_type, build_read_group=False)
        ),
    ]

    if resource_id is not None:
        users.append(
            build_test_user(
                groups=Policy.build_groups(resource_type, resource_id)
            )
        )
        users.append(
            build_test_user(
                groups=Policy.build_groups(
                    resource_type, resource_id, build_read_group=False
                )
            )
        )

    return users


def get_test_users_with_no_read_permissions(
    resource_type: ResourceType, resource_id: Optional[str] = None
) -> List[UserWithPassword]:
    """Get a list of users that do not have permissions to read from different sources."""
    users = [
        build_test_user(),
        build_test_user(
            groups=Policy.build_groups(resource_type, build_read_group=False)
        ),
    ]

    # Add user with the opposite permission, and with appropriate ones but for wrong id.
    fake_id = "fake_id"
    if resource_id is not None:
        users.append(
            build_test_user(
                groups=Policy.build_groups(
                    resource_type, resource_id, build_read_group=False
                )
            )
        )
        users.append(
            build_test_user(
                groups=Policy.build_groups(resource_type, resource_id=fake_id)
            )
        )

    return users


def get_test_users_with_no_write_permissions(
    resource_type: ResourceType, resource_id: Optional[str] = None
) -> List[UserWithPassword]:
    """Get a list of users that do not have permissions to write from different sources."""
    users = [
        build_test_user(),
        build_test_user(
            groups=Policy.build_groups(resource_type, build_write_group=False)
        ),
    ]

    fake_id = "fake_id"
    if resource_id is not None:
        users.append(
            build_test_user(
                groups=Policy.build_groups(
                    resource_type, resource_id, build_write_group=False
                )
            )
        )
        users.append(
            build_test_user(
                groups=Policy.build_groups(resource_type, resource_id=fake_id)
            )
        )

    return users
