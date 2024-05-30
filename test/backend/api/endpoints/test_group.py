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
from mlte.store.user.policy import Policy
from mlte.store.user.store_session import ManagedUserSession, UserStoreSession
from mlte.user.model import (
    Group,
    MethodType,
    Permission,
    ResourceType,
    RoleType,
    UserCreate,
)
from test.backend.fixture import api as api_helper
from test.backend.fixture.http import (
    FastAPITestHttpClient,
    get_client_for_admin,
)

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


def create_group(test_client: FastAPITestHttpClient):
    """Create test group."""
    group = get_test_group()
    with ManagedUserSession(state.user_store.session()) as user_store:
        setup_group_permisisons(group, user_store)

    admin_client = get_client_for_admin(test_client)

    res = admin_client.post(f"{GROUP_URI}", json=group.model_dump())
    assert res.status_code == codes.OK


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "api_user",
    [
        api_helper.build_test_user(role=RoleType.ADMIN),
        api_helper.build_test_user(
            groups=Policy.build_groups(ResourceType.GROUP)
        ),
        api_helper.build_test_user(
            groups=Policy.build_groups(
                ResourceType.GROUP, build_read_group=False
            )
        ),
    ],
)
def test_create(test_client_fix, api_user: UserCreate) -> None:  # noqa
    """Groups can be created."""
    test_client: FastAPITestHttpClient = test_client_fix(api_user)
    group = get_test_group()

    res = test_client.post(f"{GROUP_URI}", json=group.model_dump())
    assert res.status_code == codes.OK
    _ = Group(**res.json())


@pytest.mark.parametrize(
    "api_user",
    [
        api_helper.build_test_user(role=RoleType.ADMIN),
        api_helper.build_test_user(
            groups=Policy.build_groups(ResourceType.GROUP)
        ),
    ],
)
def test_edit(test_client_fix, api_user: UserCreate) -> None:  # noqa
    """Groups can be edited."""
    test_client: FastAPITestHttpClient = test_client_fix(api_user)
    group = get_test_group()
    p3 = Permission(
        resource_type=ResourceType.MODEL,
        resource_id="mod1",
        method=MethodType.DELETE,
    )
    with ManagedUserSession(state.user_store.session()) as user_store:
        user_store.permission_mapper.create(p3)

    # Create test group.
    create_group(test_client)

    # Edit group.
    group.permissions.append(p3)
    res = test_client.put(f"{GROUP_URI}", json=group.model_dump())
    assert res.status_code == codes.OK

    # Read it back.
    res = test_client.get(f"{GROUP_URI}/{group.name}")
    assert res.status_code == codes.OK
    edited_group = Group(**res.json())

    assert edited_group.permissions == group.permissions


@pytest.mark.parametrize(
    "api_user",
    [
        api_helper.build_test_user(role=RoleType.ADMIN),
        api_helper.build_test_user(
            groups=Policy.build_groups(ResourceType.GROUP)
        ),
        api_helper.build_test_user(
            groups=Policy.build_groups(
                ResourceType.GROUP, build_write_group=False
            )
        ),
    ],
)
def test_read(test_client_fix, api_user: UserCreate) -> None:  # noqa
    """Groups can be read."""
    test_client: FastAPITestHttpClient = test_client_fix(api_user)
    group = get_test_group()

    create_group(test_client)

    res = test_client.get(f"{GROUP_URI}/{group.name}")
    assert res.status_code == codes.OK
    read = Group(**res.json())
    assert read == group


@pytest.mark.parametrize(
    "api_user",
    [
        api_helper.build_test_user(role=RoleType.ADMIN),
        api_helper.build_test_user(
            groups=Policy.build_groups(ResourceType.GROUP)
        ),
        api_helper.build_test_user(
            groups=Policy.build_groups(
                ResourceType.GROUP, build_write_group=False
            )
        ),
    ],
)
def test_list(test_client_fix, api_user: UserCreate) -> None:  # noqa
    """Groups can be listed."""
    test_client: FastAPITestHttpClient = test_client_fix(api_user)
    group = get_test_group()
    original_groups = test_client.get(f"{GROUP_URI}")

    create_group(test_client)

    res = test_client.get(f"{GROUP_URI}")
    assert res.status_code == codes.OK
    assert len(res.json()) == len(original_groups.json()) + 1


@pytest.mark.parametrize(
    "api_user",
    [
        api_helper.build_test_user(role=RoleType.ADMIN),
        api_helper.build_test_user(
            groups=Policy.build_groups(ResourceType.GROUP)
        ),
        api_helper.build_test_user(
            groups=Policy.build_groups(
                ResourceType.GROUP, build_write_group=False
            )
        ),
    ],
)
def test_list_detailed(test_client_fix, api_user: UserCreate) -> None:  # noqa
    """Groups can be listed in detail."""
    test_client: FastAPITestHttpClient = test_client_fix(api_user)
    group = get_test_group()
    create_group(test_client)

    res = test_client.get(f"{GROUP_URI}s/details")
    assert res.status_code == codes.OK

    groups: list[dict[str, Any]] = res.json()
    print(groups)
    for curr_group in groups:
        _ = Group(**curr_group)


@pytest.mark.parametrize(
    "api_user",
    [
        api_helper.build_test_user(role=RoleType.ADMIN),
        api_helper.build_test_user(
            groups=Policy.build_groups(ResourceType.GROUP)
        ),
    ],
)
def test_delete(test_client_fix, api_user: UserCreate) -> None:  # noqa
    """Groups can be deleted."""
    test_client: FastAPITestHttpClient = test_client_fix(api_user)
    group = get_test_group()

    create_group(test_client)

    res = test_client.delete(f"{GROUP_URI}/{group.name}")
    assert res.status_code == codes.OK

    res = test_client.get(f"{GROUP_URI}/{group.name}")
    assert res.status_code == codes.NOT_FOUND


@pytest.mark.parametrize(
    "api_user",
    [
        api_helper.build_test_user(),
        api_helper.build_test_user(
            groups=Policy.build_groups(
                ResourceType.GROUP, build_write_group=False
            )
        ),
    ],
)
def test_delete_no_permission(test_client_fix, api_user: UserCreate) -> None:
    """No permission to delete."""
    test_client: FastAPITestHttpClient = test_client_fix(api_user)

    group = get_test_group()
    create_group(test_client)

    print(state.user_store.session().group_mapper.list())

    res = test_client.delete(
        f"{settings.API_PREFIX}{GROUP_URI}/{group.name}"
    )
    assert res.status_code == codes.FORBIDDEN
