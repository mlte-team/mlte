"""
test/backend/test_user.py

Test the HTTP interface for user operations.
"""
from __future__ import annotations

from typing import Any

from mlte.backend.api import codes
from mlte.backend.core.config import settings
from mlte.user.model import BasicUser, UserCreate
from test.backend.fixture.http import FastAPITestHttpClient

USER_ENDPOINT = "/user"


def get_test_user() -> UserCreate:
    """Creates a simple test user."""
    username = "user1"
    email = "user1@test.com"
    password = "pass1"
    return UserCreate(username=username, email=email, password=password)


def create_user(test_client: FastAPITestHttpClient, user: UserCreate):
    # Create test user.
    res = test_client.post(
        f"{settings.API_PREFIX}{USER_ENDPOINT}", json=user.model_dump()
    )
    assert res.status_code == codes.OK


def test_create(test_client: FastAPITestHttpClient) -> None:  # noqa
    """Users can be created."""
    user = get_test_user()

    res = test_client.post(
        f"{settings.API_PREFIX}{USER_ENDPOINT}", json=user.model_dump()
    )
    assert res.status_code == codes.OK
    _ = BasicUser(**res.json())


def test_edit_no_pass(test_client: FastAPITestHttpClient) -> None:  # noqa
    """Users can be edited."""
    user = get_test_user()
    email2 = "user2@test.com"

    # Create test user.
    create_user(test_client, user)

    # Edit user.
    user_w_pass = BasicUser(**user.model_dump())
    user_w_pass.email = email2
    res = test_client.put(
        f"{settings.API_PREFIX}{USER_ENDPOINT}", json=user_w_pass.model_dump()
    )
    assert res.status_code == codes.OK

    # Read it back.
    res = test_client.get(
        f"{settings.API_PREFIX}{USER_ENDPOINT}/{user.username}"
    )
    assert res.status_code == codes.OK
    edited_user = BasicUser(**res.json())

    assert edited_user.email == email2


def test_edit_pass(test_client: FastAPITestHttpClient) -> None:  # noqa
    """Users can be edited."""
    user = get_test_user()
    email2 = "user2@test.com"

    # Create test user.
    create_user(test_client, user)

    # Edit user.
    user.email = email2
    res = test_client.put(
        f"{settings.API_PREFIX}{USER_ENDPOINT}", json=user.model_dump()
    )
    assert res.status_code == codes.OK

    # Read it back.
    res = test_client.get(
        f"{settings.API_PREFIX}{USER_ENDPOINT}/{user.username}"
    )
    assert res.status_code == codes.OK
    edited_user = BasicUser(**res.json())

    assert edited_user.email == email2


def test_read(test_client: FastAPITestHttpClient) -> None:  # noqa
    """Users can be read."""
    user = get_test_user()

    create_user(test_client, user)

    res = test_client.get(
        f"{settings.API_PREFIX}{USER_ENDPOINT}/{user.username}"
    )
    assert res.status_code == codes.OK
    read = BasicUser(**res.json())
    assert read == BasicUser(**user.model_dump())


def test_list(test_client: FastAPITestHttpClient) -> None:  # noqa
    """Users can be listed."""
    user = get_test_user()
    original_users = test_client.get(f"{settings.API_PREFIX}{USER_ENDPOINT}")

    create_user(test_client, user)

    res = test_client.get(f"{settings.API_PREFIX}{USER_ENDPOINT}")
    assert res.status_code == codes.OK
    assert len(res.json()) == len(original_users.json()) + 1


def test_list_detailed(test_client: FastAPITestHttpClient) -> None:  # noqa
    """Users can be listed in detail."""
    user = get_test_user()
    create_user(test_client, user)

    res = test_client.get(f"{settings.API_PREFIX}{USER_ENDPOINT}s/details")
    assert res.status_code == codes.OK

    users: list[dict[str, Any]] = res.json()
    print(users)
    for curr_user in users:
        _ = BasicUser(**curr_user)


def test_delete(test_client: FastAPITestHttpClient) -> None:  # noqa
    """Users can be deleted."""
    user = get_test_user()
    original_users = test_client.get(f"{settings.API_PREFIX}{USER_ENDPOINT}")

    create_user(test_client, user)

    res = test_client.get(f"{settings.API_PREFIX}{USER_ENDPOINT}")
    assert res.status_code == codes.OK
    assert len(res.json()) == len(original_users.json()) + 1

    res = test_client.delete(
        f"{settings.API_PREFIX}{USER_ENDPOINT}/{user.username}"
    )
    assert res.status_code == codes.OK

    res = test_client.get(f"{settings.API_PREFIX}{USER_ENDPOINT}")
    assert res.status_code == codes.OK
    assert len(res.json()) == len(original_users.json())
