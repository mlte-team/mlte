"""
test/backend/api/endpoints/test_user.py

Test the API for user operations.
"""
from __future__ import annotations

from typing import Any, List

import pytest

from mlte.backend.api import codes
from mlte.backend.core.config import settings
from mlte.backend.state import state
from mlte.context.model import ModelCreate
from mlte.store.user.policy import Policy
from mlte.user.model import BasicUser, ResourceType, RoleType, UserWithPassword
from test.backend.api.endpoints.artifact.test_model import MODEL_URI
from test.backend.fixture import user_generator
from test.backend.fixture.test_api import TestAPI

USER_ENDPOINT = "/user"
USER_URI = f"{settings.API_PREFIX}{USER_ENDPOINT}"


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def get_sample_user() -> UserWithPassword:
    """Creates a simple test user."""
    username = "user1"
    email = "user1@test.com"
    password = "pass1"
    return UserWithPassword(username=username, email=email, password=password)


def create_sample_user_using_admin(test_api: TestAPI) -> None:
    """Create sample user."""
    test_api.admin_create_entity(get_sample_user(), USER_URI)


def get_user_using_admin(user_id: str, test_api: TestAPI) -> BasicUser:
    """Gets a user using admin."""
    return BasicUser(**test_api.admin_read_entity(user_id, USER_URI))


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_write_permissions(ResourceType.USER),
)
def test_create(test_api_fixture, api_user: UserWithPassword) -> None:
    """Users can be created."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()
    user = get_sample_user()

    res = test_client.post(f"{USER_URI}", json=user.model_dump())
    assert res.status_code == codes.OK
    _ = BasicUser(**res.json())

    # Update user with the groups that are automatically created.
    user.groups = Policy.build_groups(ResourceType.USER, user.username)

    # Read it back.
    assert user.is_equal_to(get_user_using_admin(user.username, test_api))


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_write_permissions(ResourceType.USER),
)
def test_create_no_permission(
    test_api_fixture, api_user: UserWithPassword
) -> None:
    """No permissions to create users."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()
    user = get_sample_user()

    res = test_client.post(f"{USER_URI}", json=user.model_dump())
    assert res.status_code == codes.FORBIDDEN


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_write_permissions(ResourceType.USER),
)
def test_edit_no_pass(test_api_fixture, api_user: UserWithPassword) -> None:
    """Users can be edited."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    user = get_sample_user()
    email2 = "user2@test.com"
    create_sample_user_using_admin(test_api)

    # Edit user.
    user_w_pass = BasicUser(**user.model_dump())
    user_w_pass.email = email2
    res = test_client.put(f"{USER_URI}", json=user_w_pass.model_dump())
    assert res.status_code == codes.OK

    # Read it back.
    edited_user = get_user_using_admin(user.username, test_api)
    assert edited_user.email == email2


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_write_permissions(ResourceType.USER),
)
def test_edit_pass(test_api_fixture, api_user: UserWithPassword) -> None:
    """Users can be edited."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    user = get_sample_user()
    email2 = "user2@test.com"
    create_sample_user_using_admin(test_api)

    # Edit user.
    user.email = email2
    res = test_client.put(f"{USER_URI}", json=user.model_dump())
    assert res.status_code == codes.OK

    # Read it back.
    edited_user = get_user_using_admin(user.username, test_api)
    assert edited_user.email == email2


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_write_permissions(ResourceType.USER),
)
def test_edit_pass_no_permission(
    test_api_fixture, api_user: UserWithPassword
) -> None:
    """Users can be edited."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    user = get_sample_user()
    email2 = "user2@test.com"
    create_sample_user_using_admin(test_api)

    # Edit user.
    user.email = email2
    res = test_client.put(f"{USER_URI}", json=user.model_dump())
    assert res.status_code == codes.FORBIDDEN


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_read_permissions(ResourceType.USER),
)
def test_read(test_api_fixture, api_user: UserWithPassword) -> None:
    """Users can be read."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    user = get_sample_user()
    create_sample_user_using_admin(test_api)

    res = test_client.get(f"{USER_URI}/{user.username}")
    assert res.status_code == codes.OK
    read = BasicUser(**res.json())

    # Update user with the groups that are automatically created.
    user.groups = Policy.build_groups(ResourceType.USER, user.username)

    assert read.is_equal_to(user)


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_read_permissions(ResourceType.USER),
)
def test_read_me(test_api_fixture, api_user: UserWithPassword) -> None:
    """Users can read its own info."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    res = test_client.get(f"{USER_URI}/me")
    assert res.status_code == codes.OK
    read = BasicUser(**res.json())

    assert read.is_equal_to(api_user)


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_read_permissions(ResourceType.USER),
)
def test_read_no_permission(
    test_api_fixture, api_user: UserWithPassword
) -> None:
    """No permission to read users."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    user = get_sample_user()
    create_sample_user_using_admin(test_api)

    res = test_client.get(f"{USER_URI}/{user.username}")
    assert res.status_code == codes.FORBIDDEN


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_read_permissions(ResourceType.USER),
)
def test_list(test_api_fixture, api_user: UserWithPassword) -> None:
    """Users can be listed."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    create_sample_user_using_admin(test_api)

    all_users = test_client.get(f"{USER_URI}")
    assert all_users.status_code == codes.OK
    assert len(all_users.json()) > 1


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_read_permissions(ResourceType.USER),
)
def test_list_no_permission(
    test_api_fixture, api_user: UserWithPassword
) -> None:
    """No permission to list users."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    create_sample_user_using_admin(test_api)

    res = test_client.get(f"{USER_URI}")
    assert res.status_code == codes.FORBIDDEN


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_read_permissions(ResourceType.USER),
)
def test_list_detailed(test_api_fixture, api_user: UserWithPassword) -> None:
    """Users can be listed in detail."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    create_sample_user_using_admin(test_api)

    res = test_client.get(f"{USER_URI}s/details")
    assert res.status_code == codes.OK

    users: list[dict[str, Any]] = res.json()
    print(users)
    for curr_user in users:
        _ = BasicUser(**curr_user)


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_read_permissions(ResourceType.USER),
)
def test_list_detailed_no_permission(
    test_api_fixture, api_user: UserWithPassword
) -> None:
    """No permission to list details."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    create_sample_user_using_admin(test_api)

    res = test_client.get(f"{USER_URI}s/details")
    assert res.status_code == codes.FORBIDDEN


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_write_permissions(ResourceType.USER),
)
def test_delete(test_api_fixture, api_user: UserWithPassword) -> None:
    """Users can be deleted."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    user = get_sample_user()
    create_sample_user_using_admin(test_api)

    res = test_client.delete(f"{USER_URI}/{user.username}")
    assert res.status_code == codes.OK

    admin_client = test_api.get_test_client_for_admin()
    res = admin_client.get(f"{USER_URI}/{user.username}")
    assert res.status_code == codes.NOT_FOUND

    assert not Policy.is_stored(
        ResourceType.USER, user.username, state.user_store.session()
    )


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_write_permissions(ResourceType.USER),
)
def test_delete_no_permission(
    test_api_fixture, api_user: UserWithPassword
) -> None:
    """No permission to delete."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    user = get_sample_user()
    create_sample_user_using_admin(test_api)

    res = test_client.delete(f"{USER_URI}/{user.username}")
    assert res.status_code == codes.FORBIDDEN


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_read_permissions(ResourceType.USER),
)
def test_list_user_groups(test_api_fixture, api_user: UserWithPassword) -> None:
    """Properly get models the user has permission to read."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    user = get_sample_user()
    create_sample_user_using_admin(test_api)

    # Create test models.
    m1_id = "m1"
    test_api.admin_create_entity(ModelCreate(identifier=m1_id), MODEL_URI)
    m2_id = "m2"
    test_api.admin_create_entity(ModelCreate(identifier=m2_id), MODEL_URI)
    m3_id = "m3"
    test_api.admin_create_entity(ModelCreate(identifier=m3_id), MODEL_URI)

    # Give user permissions to some models.
    user.groups.extend(
        Policy.build_groups(ResourceType.MODEL, resource_id=m1_id)
    )
    user.groups.extend(
        Policy.build_groups(ResourceType.MODEL, resource_id=m2_id)
    )
    user_store = state.user_store.session()
    user_store.user_mapper.edit(user)

    res = test_client.get(f"{USER_URI}/{user.username}/models")
    assert res.status_code == codes.OK

    model_list: List[str] = res.json()
    assert m1_id in model_list
    assert m2_id in model_list
    assert m3_id not in model_list


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_read_permissions(ResourceType.USER),
)
def test_list_user_groups_me(
    test_api_fixture, api_user: UserWithPassword
) -> None:
    """Properly get models the api user has permission to read."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    # Create test models.
    m1_id = "m1"
    test_api.admin_create_entity(ModelCreate(identifier=m1_id), MODEL_URI)
    m2_id = "m2"
    test_api.admin_create_entity(ModelCreate(identifier=m2_id), MODEL_URI)
    m3_id = "m3"
    test_api.admin_create_entity(ModelCreate(identifier=m3_id), MODEL_URI)

    # Give user permissions to some models.
    api_user.groups.extend(
        Policy.build_groups(ResourceType.MODEL, resource_id=m1_id)
    )
    api_user.groups.extend(
        Policy.build_groups(ResourceType.MODEL, resource_id=m2_id)
    )
    user_store = state.user_store.session()
    user_store.user_mapper.edit(BasicUser(**api_user.model_dump()))

    res = test_client.get(f"{USER_URI}/me/models")
    assert res.status_code == codes.OK

    model_list: List[str] = res.json()
    assert m1_id in model_list
    assert m2_id in model_list
    assert api_user.role == RoleType.ADMIN or m3_id not in model_list
