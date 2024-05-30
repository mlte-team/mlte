"""
test/backend/api/endpoints/test_user.py

Test the API for user operations.
"""
from __future__ import annotations

from typing import Any

import pytest

from mlte.backend.api import codes
from mlte.backend.core.config import settings
from mlte.store.user.policy import Policy
from mlte.user.model import BasicUser, ResourceType, RoleType, UserCreate
from test.backend.fixture import api as api_helper
from test.backend.fixture.http import (
    FastAPITestHttpClient,
    get_client_for_admin,
)

USER_ENDPOINT = "/user"
USER_URI = f"{settings.API_PREFIX}{USER_ENDPOINT}"


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def get_sample_user() -> UserCreate:
    """Creates a simple test user."""
    username = "user1"
    email = "user1@test.com"
    password = "pass1"
    return UserCreate(username=username, email=email, password=password)


def create_sample_user(test_client: FastAPITestHttpClient) -> None:
    """Create sample user."""
    admin_client = get_client_for_admin(test_client)

    sample_user = get_sample_user()
    res = admin_client.post(f"{USER_URI}", json=sample_user.model_dump())
    assert res.status_code == codes.OK


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "api_user",
    [
        api_helper.build_test_user(role=RoleType.ADMIN),
        api_helper.build_test_user(
            groups=Policy.build_groups(ResourceType.USER)
        ),
        api_helper.build_test_user(
            groups=Policy.build_groups(
                ResourceType.USER, build_read_group=False
            )
        ),
    ],
)
def test_create(test_client_fix, api_user: UserCreate) -> None:
    """Users can be created."""
    test_client: FastAPITestHttpClient = test_client_fix(api_user)
    user = get_sample_user()

    res = test_client.post(f"{USER_URI}", json=user.model_dump())
    assert res.status_code == codes.OK
    _ = BasicUser(**res.json())


@pytest.mark.parametrize(
    "api_user",
    [
        api_helper.build_test_user(),
        api_helper.build_test_user(
            groups=Policy.build_groups(
                ResourceType.USER, build_write_group=False
            )
        ),
    ],
)
def test_create_no_permission(test_client_fix, api_user: UserCreate) -> None:
    """No permissions to create users."""
    test_client: FastAPITestHttpClient = test_client_fix(api_user)
    user = get_sample_user()

    res = test_client.post(f"{USER_URI}", json=user.model_dump())
    assert res.status_code == codes.FORBIDDEN


@pytest.mark.parametrize(
    "api_user",
    [
        api_helper.build_test_user(role=RoleType.ADMIN),
        api_helper.build_test_user(
            groups=Policy.build_groups(ResourceType.USER)
        ),
    ],
)
def test_edit_no_pass(test_client_fix, api_user: UserCreate) -> None:
    """Users can be edited."""
    test_client: FastAPITestHttpClient = test_client_fix(api_user)

    user = get_sample_user()
    email2 = "user2@test.com"
    create_sample_user(test_client)

    # Edit user.
    user_w_pass = BasicUser(**user.model_dump())
    user_w_pass.email = email2
    res = test_client.put(f"{USER_URI}", json=user_w_pass.model_dump())
    assert res.status_code == codes.OK

    # Read it back.
    res = test_client.get(f"{USER_URI}/{user.username}")
    assert res.status_code == codes.OK
    edited_user = BasicUser(**res.json())

    assert edited_user.email == email2


@pytest.mark.parametrize(
    "api_user",
    [
        api_helper.build_test_user(role=RoleType.ADMIN),
        api_helper.build_test_user(
            groups=Policy.build_groups(ResourceType.USER)
        ),
    ],
)
def test_edit_pass(test_client_fix, api_user: UserCreate) -> None:
    """Users can be edited."""
    test_client: FastAPITestHttpClient = test_client_fix(api_user)

    user = get_sample_user()
    email2 = "user2@test.com"
    create_sample_user(test_client)

    # Edit user.
    user.email = email2
    res = test_client.put(f"{USER_URI}", json=user.model_dump())
    assert res.status_code == codes.OK

    # Read it back.
    res = test_client.get(f"{USER_URI}/{user.username}")
    assert res.status_code == codes.OK
    edited_user = BasicUser(**res.json())

    assert edited_user.email == email2


@pytest.mark.parametrize(
    "api_user",
    [
        api_helper.build_test_user(
            groups=Policy.build_groups(
                ResourceType.USER, build_write_group=False
            )
        ),
    ],
)
def test_edit_pass_no_permission(test_client_fix, api_user: UserCreate) -> None:
    """Users can be edited."""
    test_client: FastAPITestHttpClient = test_client_fix(api_user)

    user = get_sample_user()
    email2 = "user2@test.com"
    create_sample_user(test_client)

    # Edit user.
    user.email = email2
    res = test_client.put(f"{USER_URI}", json=user.model_dump())
    assert res.status_code == codes.FORBIDDEN


@pytest.mark.parametrize(
    "api_user",
    [
        api_helper.build_test_user(role=RoleType.ADMIN),
        api_helper.build_test_user(
            groups=Policy.build_groups(ResourceType.USER)
        ),
        api_helper.build_test_user(
            groups=Policy.build_groups(
                ResourceType.USER, build_write_group=False
            )
        ),
    ],
)
def test_read(test_client_fix, api_user: UserCreate) -> None:
    """Users can be read."""
    test_client: FastAPITestHttpClient = test_client_fix(api_user)

    user = get_sample_user()
    create_sample_user(test_client)

    res = test_client.get(f"{USER_URI}/{user.username}")
    assert res.status_code == codes.OK
    read = BasicUser(**res.json())
    assert read == BasicUser(**user.model_dump())


@pytest.mark.parametrize(
    "api_user",
    [
        api_helper.build_test_user(),
        api_helper.build_test_user(
            groups=Policy.build_groups(
                ResourceType.USER, build_read_group=False
            )
        ),
    ],
)
def test_read_no_permission(test_client_fix, api_user: UserCreate) -> None:
    """No permission to read users."""
    test_client: FastAPITestHttpClient = test_client_fix(api_user)

    user = get_sample_user()
    create_sample_user(test_client)

    res = test_client.get(f"{USER_URI}/{user.username}")
    assert res.status_code == codes.FORBIDDEN


@pytest.mark.parametrize(
    "api_user",
    [
        api_helper.build_test_user(role=RoleType.ADMIN),
        api_helper.build_test_user(
            groups=Policy.build_groups(ResourceType.USER)
        ),
        api_helper.build_test_user(
            groups=Policy.build_groups(
                ResourceType.USER, build_write_group=False
            )
        ),
    ],
)
def test_list(test_client_fix, api_user: UserCreate) -> None:
    """Users can be listed."""
    test_client: FastAPITestHttpClient = test_client_fix(api_user)

    create_sample_user(test_client)

    all_users = test_client.get(f"{USER_URI}")
    assert all_users.status_code == codes.OK
    assert len(all_users.json()) > 1


@pytest.mark.parametrize(
    "api_user",
    [
        api_helper.build_test_user(),
        api_helper.build_test_user(
            groups=Policy.build_groups(
                ResourceType.USER, build_read_group=False
            )
        ),
    ],
)
def test_list_no_permission(test_client_fix, api_user: UserCreate) -> None:
    """No permission to list users."""
    test_client: FastAPITestHttpClient = test_client_fix(api_user)

    create_sample_user(test_client)

    res = test_client.get(f"{USER_URI}")
    assert res.status_code == codes.FORBIDDEN


@pytest.mark.parametrize(
    "api_user",
    [
        api_helper.build_test_user(role=RoleType.ADMIN),
        api_helper.build_test_user(
            groups=Policy.build_groups(ResourceType.USER)
        ),
        api_helper.build_test_user(
            groups=Policy.build_groups(
                ResourceType.USER, build_write_group=False
            )
        ),
    ],
)
def test_list_detailed(test_client_fix, api_user: UserCreate) -> None:
    """Users can be listed in detail."""
    test_client: FastAPITestHttpClient = test_client_fix(api_user)

    create_sample_user(test_client)

    res = test_client.get(f"{USER_URI}s/details")
    assert res.status_code == codes.OK

    users: list[dict[str, Any]] = res.json()
    print(users)
    for curr_user in users:
        _ = BasicUser(**curr_user)


@pytest.mark.parametrize(
    "api_user",
    [
        api_helper.build_test_user(),
        api_helper.build_test_user(
            groups=Policy.build_groups(
                ResourceType.USER, build_read_group=False
            )
        ),
    ],
)
def test_list_detailed_no_permission(
    test_client_fix, api_user: UserCreate
) -> None:
    """No permission to list details."""
    test_client: FastAPITestHttpClient = test_client_fix(api_user)

    create_sample_user(test_client)

    res = test_client.get(f"{USER_URI}s/details")
    assert res.status_code == codes.FORBIDDEN


@pytest.mark.parametrize(
    "api_user",
    [
        api_helper.build_test_user(role=RoleType.ADMIN),
        api_helper.build_test_user(
            groups=Policy.build_groups(ResourceType.USER)
        ),
    ],
)
def test_delete(test_client_fix, api_user: UserCreate) -> None:
    """Users can be deleted."""
    test_client: FastAPITestHttpClient = test_client_fix(api_user)

    user = get_sample_user()
    create_sample_user(test_client)

    res = test_client.delete(f"{USER_URI}/{user.username}")
    assert res.status_code == codes.OK

    res = test_client.get(f"{USER_URI}/{user.username}")
    assert res.status_code == codes.NOT_FOUND


@pytest.mark.parametrize(
    "api_user",
    [
        api_helper.build_test_user(),
        api_helper.build_test_user(
            groups=Policy.build_groups(
                ResourceType.USER, build_write_group=False
            )
        ),
    ],
)
def test_delete_no_permission(test_client_fix, api_user: UserCreate) -> None:
    """No permission to delete."""
    test_client: FastAPITestHttpClient = test_client_fix(api_user)

    user = get_sample_user()
    create_sample_user(test_client)

    res = test_client.delete(f"{USER_URI}/{user.username}")
    assert res.status_code == codes.FORBIDDEN
