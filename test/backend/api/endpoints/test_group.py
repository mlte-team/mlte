"""
test/backend/test_group.py

Test the HTTP interface for group operations.
"""
from __future__ import annotations

from typing import Any, List

import pytest

from mlte.backend.api import codes
from mlte.backend.core.config import settings
from mlte.backend.state import state
from mlte.store.user.store import ManagedUserSession, UserStoreSession
from mlte.user.model import Group, MethodType, Permission, ResourceType
from test.backend.fixture.http import (  # noqa
    FastAPITestHttpClient,
    clients,
    mem_store_and_test_http_client,
)

GROUP_ENDPOINT = "/group"
GROUP_URI = f"{settings.API_PREFIX}{GROUP_ENDPOINT}"


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


def create_group(client: FastAPITestHttpClient, group: Group):
    """Create test group."""
    with ManagedUserSession(state.user_store.session()) as user_store:
        setup_group_permisisons(group, user_store)

    res = client.post(f"{GROUP_URI}", json=group.model_dump())
    assert res.status_code == codes.OK


@pytest.mark.parametrize("client_fixture", clients())
def test_create(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Groups can be created."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    group = get_test_group()

    res = client.post(f"{GROUP_URI}", json=group.model_dump())
    assert res.status_code == codes.OK
    _ = Group(**res.json())


@pytest.mark.parametrize("client_fixture", clients())
def test_edit(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Groups can be edited."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    group = get_test_group()
    p3 = Permission(
        resource_type=ResourceType.MODEL,
        resource_id="mod1",
        method=MethodType.DELETE,
    )
    with ManagedUserSession(state.user_store.session()) as user_store:
        user_store.permission_mapper.create(p3)

    # Create test group.
    create_group(client, group)

    # Edit group.
    group.permissions.append(p3)
    res = client.put(f"{GROUP_URI}", json=group.model_dump())
    assert res.status_code == codes.OK

    # Read it back.
    res = client.get(f"{GROUP_URI}/{group.name}")
    assert res.status_code == codes.OK
    edited_group = Group(**res.json())

    assert edited_group.permissions == group.permissions


@pytest.mark.parametrize("client_fixture", clients())
def test_read(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Groups can be read."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    group = get_test_group()

    create_group(client, group)

    res = client.get(f"{GROUP_URI}/{group.name}")
    assert res.status_code == codes.OK
    read = Group(**res.json())
    assert read == group


@pytest.mark.parametrize("client_fixture", clients())
def test_list(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Groups can be listed."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    group = get_test_group()
    original_groups = client.get(f"{GROUP_URI}")

    create_group(client, group)

    res = client.get(f"{GROUP_URI}")
    assert res.status_code == codes.OK
    assert len(res.json()) == len(original_groups.json()) + 1


@pytest.mark.parametrize("client_fixture", clients())
def test_list_detailed(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Groups can be listed in detail."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    group = get_test_group()
    create_group(client, group)

    res = client.get(f"{GROUP_URI}s/details")
    assert res.status_code == codes.OK

    groups: list[dict[str, Any]] = res.json()
    print(groups)
    for curr_group in groups:
        _ = Group(**curr_group)


@pytest.mark.parametrize("client_fixture", clients())
def test_delete(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Groups can be deleted."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    group = get_test_group()
    original_groups = client.get(f"{GROUP_URI}")

    create_group(client, group)

    res = client.get(f"{GROUP_URI}")
    assert res.status_code == codes.OK
    assert len(res.json()) == len(original_groups.json()) + 1

    res = client.delete(f"{GROUP_URI}/{group.name}")
    assert res.status_code == codes.OK

    res = client.get(f"{GROUP_URI}")
    assert res.status_code == codes.OK
    assert len(res.json()) == len(original_groups.json())
