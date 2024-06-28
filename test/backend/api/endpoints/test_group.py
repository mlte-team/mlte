"""
test/backend/api/endpoints/test_group.py

Test the API for group operations.
"""
from __future__ import annotations

from typing import Any, List

import pytest

from mlte.backend.api import codes
from mlte.backend.core.config import settings
from mlte.backend.state import state
from mlte.store.user.store_session import ManagedUserSession, UserStoreSession
from mlte.user.model import (
    Group,
    MethodType,
    Permission,
    ResourceType,
    UserWithPassword,
)
from test.backend.fixture import user_generator
from test.backend.fixture.test_api import TestAPI

GROUP_ENDPOINT = "/group"
GROUP_URI = f"{settings.API_PREFIX}{GROUP_ENDPOINT}"


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def setup_group_permisisons(test_group: Group, user_store: UserStoreSession):
    """Helper to set up permissions."""
    for permission in test_group.permissions:
        user_store.permission_mapper.create(permission)


def get_test_permissions() -> List[Permission]:
    """Helper to get a group structure."""
    p1 = Permission(
        resource_type=ResourceType.MODEL,
        resource_id="mod1",
        method=MethodType.GET,
    )
    p2 = Permission(
        resource_type=ResourceType.MODEL,
        resource_id="mod1",
        method=MethodType.POST,
    )
    return [p1, p2]


def get_test_group() -> Group:
    """Helper to get a group structure."""
    group_name = "g1"
    test_group = Group(name=group_name, permissions=get_test_permissions())
    return test_group


def create_group_using_admin(api: TestAPI):
    """Create test group."""
    group = get_test_group()
    with ManagedUserSession(state.user_store.session()) as user_store:
        setup_group_permisisons(group, user_store)

    api.admin_create_entity(get_test_group(), GROUP_URI)


def get_group_using_admin(group_id: str, api: TestAPI) -> dict[str, Any]:
    """Gets a user using admin."""
    return api.admin_read_entity(group_id, GROUP_URI)


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_write_permissions(ResourceType.GROUP),
)
def test_create(test_api_fixture, api_user: UserWithPassword) -> None:  # noqa
    """Groups can be created."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()
    group = get_test_group()

    res = test_client.post(f"{GROUP_URI}", json=group.model_dump())
    assert res.status_code == codes.OK
    _ = Group(**res.json())

    _ = Group(**get_group_using_admin(group.name, test_api))


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_write_permissions(ResourceType.GROUP),
)
def test_create_no_permissions(
    test_api_fixture, api_user: UserWithPassword
) -> None:  # noqa
    """No permissions to create."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()
    group = get_test_group()

    res = test_client.post(f"{GROUP_URI}", json=group.model_dump())
    assert res.status_code == codes.FORBIDDEN


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_write_permissions(ResourceType.GROUP),
)
def test_edit(test_api_fixture, api_user: UserWithPassword) -> None:  # noqa
    """Groups can be edited."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()
    group = get_test_group()
    p3 = Permission(
        resource_type=ResourceType.MODEL,
        resource_id="mod1",
        method=MethodType.DELETE,
    )
    with ManagedUserSession(state.user_store.session()) as user_store:
        user_store.permission_mapper.create(p3)

    # Create test group.
    create_group_using_admin(test_api)

    # Edit group.
    group.permissions.append(p3)
    res = test_client.put(f"{GROUP_URI}", json=group.model_dump())
    assert res.status_code == codes.OK

    # Read it back.
    edited_group = Group(**get_group_using_admin(group.name, test_api))
    assert edited_group.permissions == group.permissions


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_write_permissions(ResourceType.GROUP),
)
def test_edit_no_permission(
    test_api_fixture, api_user: UserWithPassword
) -> None:  # noqa
    """No permissions to edit."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()
    group = get_test_group()
    p3 = Permission(
        resource_type=ResourceType.MODEL,
        resource_id="mod1",
        method=MethodType.DELETE,
    )
    with ManagedUserSession(state.user_store.session()) as user_store:
        user_store.permission_mapper.create(p3)

    # Create test group.
    create_group_using_admin(test_api)

    # Edit group.
    group.permissions.append(p3)
    res = test_client.put(f"{GROUP_URI}", json=group.model_dump())
    assert res.status_code == codes.FORBIDDEN


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_read_permissions(ResourceType.GROUP),
)
def test_read(test_api_fixture, api_user: UserWithPassword) -> None:  # noqa
    """Groups can be read."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()
    group = get_test_group()

    create_group_using_admin(test_api)

    res = test_client.get(f"{GROUP_URI}/{group.name}")
    assert res.status_code == codes.OK
    read = Group(**res.json())
    assert read == group


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_read_permissions(ResourceType.GROUP),
)
def test_read_no_permission(
    test_api_fixture, api_user: UserWithPassword
) -> None:  # noqa
    """No permission to read group"""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()
    group = get_test_group()

    create_group_using_admin(test_api)

    res = test_client.get(f"{GROUP_URI}/{group.name}")
    assert res.status_code == codes.FORBIDDEN


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_read_permissions(ResourceType.GROUP),
)
def test_list(test_api_fixture, api_user: UserWithPassword) -> None:  # noqa
    """Groups can be listed."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()
    original_groups = test_client.get(f"{GROUP_URI}")

    create_group_using_admin(test_api)

    res = test_client.get(f"{GROUP_URI}")
    assert res.status_code == codes.OK
    assert len(res.json()) == len(original_groups.json()) + 1


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_read_permissions(ResourceType.GROUP),
)
def test_list_no_permission(
    test_api_fixture, api_user: UserWithPassword
) -> None:  # noqa
    """No permission to list."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    create_group_using_admin(test_api)

    res = test_client.get(f"{GROUP_URI}")
    assert res.status_code == codes.FORBIDDEN


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_read_permissions(ResourceType.GROUP),
)
def test_list_detailed(
    test_api_fixture, api_user: UserWithPassword
) -> None:  # noqa
    """Groups can be listed in detail."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()
    create_group_using_admin(test_api)

    res = test_client.get(f"{GROUP_URI}s/details")
    assert res.status_code == codes.OK

    groups: list[dict[str, Any]] = res.json()
    print(groups)
    for curr_group in groups:
        _ = Group(**curr_group)


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_read_permissions(ResourceType.GROUP),
)
def test_list_detailed_no_permission(
    test_api_fixture, api_user: UserWithPassword
) -> None:  # noqa
    """No permissions to list details."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()
    create_group_using_admin(test_api)

    res = test_client.get(f"{GROUP_URI}s/details")
    assert res.status_code == codes.FORBIDDEN


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_write_permissions(ResourceType.GROUP),
)
def test_delete(test_api_fixture, api_user: UserWithPassword) -> None:  # noqa
    """Groups can be deleted."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()
    group = get_test_group()

    create_group_using_admin(test_api)

    res = test_client.delete(f"{GROUP_URI}/{group.name}")
    assert res.status_code == codes.OK

    admin_client = test_api.get_test_client_for_admin()
    res = admin_client.get(f"{GROUP_URI}/{group.name}")
    assert res.status_code == codes.NOT_FOUND


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_write_permissions(ResourceType.GROUP),
)
def test_delete_no_permission(
    test_api_fixture, api_user: UserWithPassword
) -> None:
    """No permission to delete."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    group = get_test_group()
    create_group_using_admin(test_api)

    res = test_client.delete(f"{GROUP_URI}/{group.name}")
    assert res.status_code == codes.FORBIDDEN
