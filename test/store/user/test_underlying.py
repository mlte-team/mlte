"""
test/store/user/test_underlying.py

Unit tests for the underlying user store implementations.
"""

from typing import List

import pytest

import mlte.store.error as errors
from mlte.store.user.store import (
    ManagedUserSession,
    UserStore,
    UserStoreSession,
)
from mlte.user.model import (
    BasicUser,
    Group,
    MethodType,
    Permission,
    ResourceType,
    UserCreate,
)
from mlte.user.model_logic import are_users_equal

from .fixture import (  # noqa
    create_fs_store,
    create_memory_store,
    create_rdbs_store,
    fs_store,
    memory_store,
    rdbs_store,
    user_stores,
)

TEST_MOD_ID = "mod1"


def test_init_memory() -> None:
    """An in-memory store can be initialized."""
    _ = create_memory_store()


def test_init_rdbs() -> None:
    """A relational DB store can be initialized."""
    _ = create_rdbs_store()


def test_init_fs(tmp_path) -> None:
    """A FSstore can be initialized."""
    _ = create_fs_store(tmp_path)


def get_test_user() -> UserCreate:
    """Helper to get a user structure."""
    username = "user1"
    email = "email@server.com"
    password = "1234"
    test_user = UserCreate(
        username=username,
        email=email,
        password=password,
        groups=[get_test_group()],
    )
    return test_user


def get_test_group() -> Group:
    """Helper to get a group structure."""
    group_name = "g1"
    test_user = Group(name=group_name, permissions=get_test_permissions())
    return test_user


def setup_user_groups(user: UserCreate, user_store: UserStoreSession):
    """Helper to set up groups."""
    for group in user.groups:
        setup_group_permisisons(group, user_store)
        user_store.group_mapper.create(group)


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


@pytest.mark.parametrize("store_fixture_name", user_stores())
def test_user(store_fixture_name: str, request: pytest.FixtureRequest) -> None:
    """An artifact store supports user operations."""
    store: UserStore = request.getfixturevalue(store_fixture_name)

    test_user = get_test_user()
    email2 = "email2@server.com"
    name2 = "new name"

    with ManagedUserSession(store.session()) as user_store:
        original_users = user_store.user_mapper.list()

        # Set up dependent groups.
        setup_user_groups(test_user, user_store)

        # Test creating a user.
        user_store.user_mapper.create(test_user)
        read_user = user_store.user_mapper.read(test_user.username)
        assert are_users_equal(test_user, read_user)

        # Test listing users.
        users = user_store.user_mapper.list()
        assert len(users) == 1 + len(original_users)

        # Test editing all user info.
        test_user.email = email2
        _ = user_store.user_mapper.edit(test_user)
        read_user = user_store.user_mapper.read(test_user.username)
        assert read_user.email == email2

        # Test editing user info w/out changing password.
        hashed_password = read_user.hashed_password
        test_user.password = "password that should be ignored"
        test_user2 = BasicUser(**test_user.model_dump())
        test_user2.full_name = name2
        _ = user_store.user_mapper.edit(test_user2)
        read_user = user_store.user_mapper.read(test_user2.username)
        assert read_user.full_name == name2
        assert read_user.hashed_password == hashed_password

        # Test deleting a user.
        user_store.user_mapper.delete(test_user.username)
        with pytest.raises(errors.ErrorNotFound):
            user_store.user_mapper.read(test_user.username)


@pytest.mark.parametrize("store_fixture_name", user_stores())
def test_group(store_fixture_name: str, request: pytest.FixtureRequest) -> None:
    """An artifact store supports group operations."""
    store: UserStore = request.getfixturevalue(store_fixture_name)

    test_group = get_test_group()
    p3 = Permission(
        resource_type=ResourceType.MODEL,
        resource_id="mod1",
        method=MethodType.DELETE,
    )

    with ManagedUserSession(store.session()) as user_store:
        original_groups = user_store.group_mapper.list()

        # Set up needed permissions.
        setup_group_permisisons(test_group, user_store)
        user_store.permission_mapper.create(p3)

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


@pytest.mark.parametrize("store_fixture_name", user_stores())
def test_permission(
    store_fixture_name: str, request: pytest.FixtureRequest
) -> None:
    """An artifact store supports permission operations."""
    store: UserStore = request.getfixturevalue(store_fixture_name)

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
