"""Unit tests for the underlying user store implementations."""

from typing import List

import pytest

import mlte.store.error as errors
from mlte.backend.core.state import state
from mlte.store.base import StoreType
from mlte.store.user.policy import user_policy
from mlte.store.user.store import UserStore
from mlte.store.user.store_session import ManagedUserSession, UserStoreSession
from mlte.user.model import (
    BasicUser,
    Group,
    MethodType,
    Permission,
    ResourceType,
    UserWithPassword,
)
from test.store.utils import store_types

TEST_MOD_ID = "mod1"


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def get_test_user() -> UserWithPassword:
    """Helper to get a user structure."""
    username = "user1"
    email = "email@server.com"
    password = "1234"
    test_user = UserWithPassword(
        username=username,
        email=email,
        password=password,
        groups=[get_test_group()],
    )
    return test_user


def get_test_group() -> Group:
    """Helper to get a group structure."""
    group_name = "g1"
    test_user = Group(name=group_name, permissions=get_default_permissions())
    return test_user


def setup_test_group(user_store: UserStoreSession):
    """Helper to set up groups."""
    user_store.group_mapper.create(get_test_group())


def get_default_permissions() -> list[Permission]:
    """Helper to get some of the default permissions."""
    permissions: list[Permission] = []
    for resource_type in ResourceType:
        permissions.append(
            Permission(resource_type=resource_type, method=MethodType.GET)
        )
    return permissions


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


def get_internal_store_session(
    tested_user_store: UserStoreSession, store_type: StoreType
) -> UserStoreSession:
    """Sets default user policies in the internal user store."""
    if store_type == StoreType.REMOTE_HTTP:
        return state.stores.user_store.session()
    else:
        return tested_user_store


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


@pytest.mark.parametrize("store_type", store_types())
def test_init_store(store_type: StoreType, create_test_user_store) -> None:
    """A store can be initialized."""
    _ = create_test_user_store(store_type)

    # If we get here, the fixture was called and the store was initialized.
    assert True


@pytest.mark.parametrize("store_type", store_types())
def test_user(store_type: StoreType, create_test_user_store) -> None:
    """An artifact store supports user operations."""
    user_store: UserStore = create_test_user_store(store_type)

    test_user = get_test_user()
    email2 = "email2@server.com"
    name2 = "new name"

    with ManagedUserSession(user_store.session()) as user_store_session:
        original_users = user_store_session.user_mapper.list()
        internal_store = get_internal_store_session(user_store_session, store_type)
        test_user = user_policy.set_default_user_policies(
            test_user, internal_store.policy_store
        )

        # Set up dependent groups.
        setup_test_group(user_store_session)

        # Test creating a user.
        user_store_session.user_mapper.create(test_user)
        read_user = user_store_session.user_mapper.read(test_user.username)
        assert test_user.is_equal_to(read_user)

        # Test listing users.
        users = user_store_session.user_mapper.list()
        assert len(users) == 1 + len(original_users)

        # Test editing all user info.
        test_user.email = email2
        _ = user_store_session.user_mapper.edit(test_user)
        read_user = user_store_session.user_mapper.read(test_user.username)
        assert read_user.email == email2

        # Test editing user info w/out changing password.
        hashed_password = read_user.hashed_password
        test_user.password = "password that should be ignored"
        test_user2 = BasicUser(**test_user.to_json())
        test_user2.full_name = name2
        _ = user_store_session.user_mapper.edit(test_user2)
        read_user = user_store_session.user_mapper.read(test_user2.username)
        assert read_user.full_name == name2
        assert read_user.hashed_password == hashed_password

        # Test deleting a user.
        user_store_session.user_mapper.delete(test_user.username)
        with pytest.raises(errors.ErrorNotFound):
            user_store_session.user_mapper.read(test_user.username)


@pytest.mark.parametrize("store_type", store_types())
def test_user_group_change(
    store_type: StoreType, create_test_user_store
) -> None:
    """Test proper syncchronization between users and groups."""
    store: UserStore = create_test_user_store(store_type)

    test_user = get_test_user()

    with ManagedUserSession(store.session()) as user_store:
        internal_store = get_internal_store_session(user_store, store_type)
        test_user = user_policy.set_default_user_policies(
            test_user, internal_store.policy_store
        )

        # Set up dependent groups.
        setup_test_group(user_store)

        # Create a user.
        user_store.user_mapper.create(test_user)
        read_user = user_store.user_mapper.read(test_user.username)
        assert test_user.is_equal_to(read_user)

        # Edit group info, revmoving a permission.
        group = get_test_group()
        group.permissions.pop(1)
        updated_group = user_store.group_mapper.edit(group)

        # Ensure user has updated group info.
        found_group = None
        read_user = user_store.user_mapper.read(test_user.username)
        for group in read_user.groups:
            if group.name == updated_group.name:
                found_group = group
                break

        # Check if we got the expected group.
        assert found_group == updated_group


@pytest.mark.parametrize("store_type", store_types())
def test_group(store_type: StoreType, create_test_user_store) -> None:
    """An artifact store supports group operations."""
    store: UserStore = create_test_user_store(store_type)

    test_group = get_test_group()
    p3 = Permission(
        resource_type=ResourceType.MODEL,
        resource_id="mod1",
        method=MethodType.DELETE,
    )

    with ManagedUserSession(store.session()) as user_store:
        original_groups = user_store.group_mapper.list()

        # Set up needed permissions.
        internal_store = get_internal_store_session(user_store, store_type)
        internal_store.permission_mapper.create(p3)

        # Test creating a group.
        user_store.group_mapper.create(test_group)
        read_group = user_store.group_mapper.read(test_group.name)
        assert test_group == read_group

        # Test listing groups.
        groups = user_store.group_mapper.list()
        assert len(groups) == 1 + len(original_groups)

        # Test editing group.
        test_group.permissions.append(p3)
        _ = user_store.group_mapper.edit(test_group)
        read_group = user_store.group_mapper.read(test_group.name)
        assert read_group.permissions == test_group.permissions

        # Test deleting a group.
        user_store.group_mapper.delete(test_group.name)
        with pytest.raises(errors.ErrorNotFound):
            user_store.group_mapper.read(test_group.name)


@pytest.mark.parametrize("store_type", store_types())
def test_permission(store_type: StoreType, create_test_user_store) -> None:
    """An artifact store supports permission operations."""

    # Permissions will only be handled locally, so this is not tested for the remote one.
    if store_type == StoreType.REMOTE_HTTP:
        pytest.skip()

    store: UserStore = create_test_user_store(store_type)

    test_permission1 = get_test_permissions()[0]

    with ManagedUserSession(store.session()) as user_store:
        original_permissions = user_store.permission_mapper.list()

        # Test creating a permission.
        user_store.permission_mapper.create(test_permission1)
        read_permission = user_store.permission_mapper.read(
            test_permission1.to_str()
        )
        assert test_permission1 == read_permission

        # Test listing permission.
        groups = user_store.permission_mapper.list()
        assert len(groups) == 1 + len(original_permissions)

        # Test deleting a permission.
        user_store.permission_mapper.delete(test_permission1.to_str())
        with pytest.raises(errors.ErrorNotFound):
            user_store.permission_mapper.read(test_permission1.to_str())
