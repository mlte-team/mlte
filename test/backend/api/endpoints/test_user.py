"""
test/backend/test_user.py

Test the HTTP interface for user operations.
"""
from __future__ import annotations

from typing import Any

import pytest

from mlte.backend.api import codes
from mlte.backend.core.config import settings
from mlte.user.model import BasicUser, UserCreate
from test.backend.fixture.http import (  # noqa
    FastAPITestHttpClient,
    clients,
    mem_store_and_test_http_client,
)

USER_ENDPOINT = "/user"


def get_test_user() -> UserCreate:
    """Creates a simple test user."""
    username = "user1"
    email = "user1@test.com"
    password = "pass1"
    return UserCreate(username=username, email=email, password=password)


def create_user(client: FastAPITestHttpClient, user: UserCreate):
    # Create test user.
    res = client.post(
        f"{settings.API_PREFIX}{USER_ENDPOINT}", json=user.model_dump()
    )
    assert res.status_code == codes.OK


@pytest.mark.parametrize("client_fixture", clients())
def test_create(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Users can be created."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    user = get_test_user()

    res = client.post(
        f"{settings.API_PREFIX}{USER_ENDPOINT}", json=user.model_dump()
    )
    assert res.status_code == codes.OK
    _ = BasicUser(**res.json())


@pytest.mark.parametrize("client_fixture", clients())
def test_edit_no_pass(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Users can be edited."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    user = get_test_user()
    email2 = "user2@test.com"

    # Create test user.
    create_user(client, user)

    # Edit user.
    user_w_pass = BasicUser(**user.model_dump())
    user_w_pass.email = email2
    res = client.put(
        f"{settings.API_PREFIX}{USER_ENDPOINT}", json=user_w_pass.model_dump()
    )
    assert res.status_code == codes.OK

    # Read it back.
    res = client.get(f"{settings.API_PREFIX}{USER_ENDPOINT}/{user.username}")
    assert res.status_code == codes.OK
    edited_user = BasicUser(**res.json())

    assert edited_user.email == email2


@pytest.mark.parametrize("client_fixture", clients())
def test_edit_pass(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Users can be edited."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    user = get_test_user()
    email2 = "user2@test.com"

    # Create test user.
    create_user(client, user)

    # Edit user.
    user.email = email2
    res = client.put(
        f"{settings.API_PREFIX}{USER_ENDPOINT}", json=user.model_dump()
    )
    assert res.status_code == codes.OK

    # Read it back.
    res = client.get(f"{settings.API_PREFIX}{USER_ENDPOINT}/{user.username}")
    assert res.status_code == codes.OK
    edited_user = BasicUser(**res.json())

    assert edited_user.email == email2


@pytest.mark.parametrize("client_fixture", clients())
def test_read(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Users can be read."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    user = get_test_user()

    create_user(client, user)

    res = client.get(f"{settings.API_PREFIX}{USER_ENDPOINT}/{user.username}")
    assert res.status_code == codes.OK
    read = BasicUser(**res.json())
    assert read == BasicUser(**user.model_dump())


@pytest.mark.parametrize("client_fixture", clients())
def test_list(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Users can be listed."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    user = get_test_user()
    original_users = client.get(f"{settings.API_PREFIX}{USER_ENDPOINT}")

    create_user(client, user)

    res = client.get(f"{settings.API_PREFIX}{USER_ENDPOINT}")
    assert res.status_code == codes.OK
    assert len(res.json()) == len(original_users.json()) + 1


@pytest.mark.parametrize("client_fixture", clients())
def test_list_detailed(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Users can be listed in detail."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    user = get_test_user()
    create_user(client, user)

    res = client.get(f"{settings.API_PREFIX}{USER_ENDPOINT}s/details")
    assert res.status_code == codes.OK

    users: list[dict[str, Any]] = res.json()
    print(users)
    for curr_user in users:
        _ = BasicUser(**curr_user)


@pytest.mark.parametrize("client_fixture", clients())
def test_delete(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Users can be deleted."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    user = get_test_user()
    original_users = client.get(f"{settings.API_PREFIX}{USER_ENDPOINT}")

    create_user(client, user)

    res = client.get(f"{settings.API_PREFIX}{USER_ENDPOINT}")
    assert res.status_code == codes.OK
    assert len(res.json()) == len(original_users.json()) + 1

    res = client.delete(f"{settings.API_PREFIX}{USER_ENDPOINT}/{user.username}")
    assert res.status_code == codes.OK

    res = client.get(f"{settings.API_PREFIX}{USER_ENDPOINT}")
    assert res.status_code == codes.OK
    assert len(res.json()) == len(original_users.json())
