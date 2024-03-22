"""
test/store/user/test_underlying.py

Unit tests for the underlying user store implementations.
"""

import pytest

import mlte.store.error as errors
from mlte.store.user.store import ManagedUserSession, UserStore
from mlte.user.model import User

from .fixture import (  # noqa
    create_memory_store,
    create_rdbs_store,
    memory_store,
    rdbs_store,
    stores,
)


def test_init_memory() -> None:
    """An in-memory store can be initialized."""
    _ = create_memory_store()


def test_init_rdbs() -> None:
    """A relational DB store can be initialized."""
    _ = create_rdbs_store()


def get_test_user() -> User:
    username = "user1"
    email = "email@server.com"
    hashed_password = "fakehash..."
    test_user = User(
        username=username, email=email, hashed_password=hashed_password
    )
    return test_user


@pytest.mark.parametrize("store_fixture_name", stores())
def test_user(store_fixture_name: str, request: pytest.FixtureRequest) -> None:
    """An artifact store supports model operations."""
    store: UserStore = request.getfixturevalue(store_fixture_name)

    test_user = get_test_user()

    with ManagedUserSession(store.session()) as handle:
        handle.create_user(test_user)

        read_user = handle.read_user(test_user.username)
        assert read_user == test_user

        users = handle.list_users()
        assert len(users) == 1

        handle.delete_user(test_user.username)

        with pytest.raises(errors.ErrorNotFound):
            handle.read_user(test_user.username)
