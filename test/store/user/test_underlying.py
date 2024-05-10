"""
test/store/user/test_underlying.py

Unit tests for the underlying user store implementations.
"""

import pytest

import mlte.store.error as errors
from mlte.store.user.store import ManagedUserSession, UserStore
from mlte.user.model import BasicUser, UserCreate
from mlte.user.model_logic import are_users_equal

from .fixture import (  # noqa
    create_memory_store,
    create_rdbs_store,
    fs_store,
    memory_store,
    rdbs_store,
    user_stores,
)


def test_init_memory() -> None:
    """An in-memory store can be initialized."""
    _ = create_memory_store()


def test_init_rdbs() -> None:
    """A relational DB store can be initialized."""
    _ = create_rdbs_store()


def get_test_user() -> UserCreate:
    username = "user1"
    email = "email@server.com"
    password = "1234"
    test_user = UserCreate(username=username, email=email, password=password)
    return test_user


@pytest.mark.parametrize("store_fixture_name", user_stores())
def test_user(store_fixture_name: str, request: pytest.FixtureRequest) -> None:
    """An artifact store supports model operations."""
    store: UserStore = request.getfixturevalue(store_fixture_name)

    test_user = get_test_user()
    email2 = "email2@server.com"
    name2 = "new name"

    with ManagedUserSession(store.session()) as handle:
        original_users = handle.user_mapper.list()

        # Test creating a user.
        handle.user_mapper.create(test_user)
        read_user = handle.user_mapper.read(test_user.username)
        assert are_users_equal(test_user, read_user)

        # Test listing users.
        users = handle.user_mapper.list()
        assert len(users) == 1 + len(original_users)

        # Test editing all user info.
        test_user.email = email2
        _ = handle.user_mapper.edit(test_user)
        read_user = handle.user_mapper.read(test_user.username)
        assert read_user.email == email2

        # Test editing user info w/out changing password.
        hashed_password = read_user.hashed_password
        test_user.password = "password that should be ignored"
        test_user2 = BasicUser(**test_user.model_dump())
        test_user2.full_name = name2
        _ = handle.user_mapper.edit(test_user2)
        read_user = handle.user_mapper.read(test_user2.username)
        assert read_user.full_name == name2
        assert read_user.hashed_password == hashed_password

        # Test deleting a user.
        handle.user_mapper.delete(test_user.username)
        with pytest.raises(errors.ErrorNotFound):
            handle.user_mapper.read(test_user.username)
