"""
test/backend/test_user.py

Test the HTTP interface for user operations.
"""

import pytest

from mlte.backend.api import codes
from mlte.backend.core.config import settings
from mlte.user.model import BasicUser, UserCreate

from .fixture.http import (  # noqa
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
    res = client.post(
        f"{settings.API_PREFIX}{USER_ENDPOINT}", json=user.model_dump()
    )
    assert res.status_code == codes.OK

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
    res = client.post(
        f"{settings.API_PREFIX}{USER_ENDPOINT}", json=user.model_dump()
    )
    assert res.status_code == codes.OK

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

    res = client.post(
        f"{settings.API_PREFIX}{USER_ENDPOINT}", json=user.model_dump()
    )
    assert res.status_code == codes.OK

    created = BasicUser(**res.json())

    res = client.get(f"{settings.API_PREFIX}{USER_ENDPOINT}/{user.username}")
    assert res.status_code == codes.OK
    read = BasicUser(**res.json())
    assert read == created


@pytest.mark.parametrize("client_fixture", clients())
def test_list(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Users can be listed."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    user = get_test_user()
    original_users = client.get(f"{settings.API_PREFIX}{USER_ENDPOINT}")

    res = client.post(
        f"{settings.API_PREFIX}{USER_ENDPOINT}", json=user.model_dump()
    )
    assert res.status_code == codes.OK

    res = client.get(f"{settings.API_PREFIX}{USER_ENDPOINT}")
    assert res.status_code == codes.OK
    assert len(res.json()) == len(original_users.json()) + 1


@pytest.mark.parametrize("client_fixture", clients())
def test_delete(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Users can be deleted."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    user = get_test_user()
    original_users = client.get(f"{settings.API_PREFIX}{USER_ENDPOINT}")

    res = client.post(
        f"{settings.API_PREFIX}{USER_ENDPOINT}", json=user.model_dump()
    )
    assert res.status_code == codes.OK

    res = client.get(f"{settings.API_PREFIX}{USER_ENDPOINT}")
    assert res.status_code == codes.OK
    assert len(res.json()) == len(original_users.json()) + 1

    res = client.delete(f"{settings.API_PREFIX}{USER_ENDPOINT}/{user.username}")
    assert res.status_code == codes.OK

    res = client.get(f"{settings.API_PREFIX}{USER_ENDPOINT}")
    assert res.status_code == codes.OK
    assert len(res.json()) == len(original_users.json())
