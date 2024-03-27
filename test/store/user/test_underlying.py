"""
test/store/user/test_underlying.py

Unit tests for the underlying user store implementations.
"""

import pytest

import mlte.store.error as errors
from mlte.store.user.store import ManagedUserSession, UserStore
from mlte.user.model import UserCreate
from mlte.user.model_logic import are_users_equal

from .fixture import (  # noqa
    create_memory_store,
    create_rdbs_store,
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

    with ManagedUserSession(store.session()) as handle:
        original_users = handle.list_users()

        handle.create_user(test_user)

        read_user = handle.read_user(test_user.username)
        assert are_users_equal(test_user, read_user)

        users = handle.list_users()
        assert len(users) == 1 + len(original_users)

        handle.delete_user(test_user.username)

        with pytest.raises(errors.ErrorNotFound):
            handle.read_user(test_user.username)
