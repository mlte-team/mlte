"""
test/backend/auth/test_authentication.py

Test the authentication operations
"""


import pytest

from mlte.backend.api import dependencies
from mlte.backend.api.auth import authentication
from mlte.user import passwords
from mlte.user.model import User

from ...store.user.fixture import memory_store, rdbs_store, stores  # noqa
from .. import state_setup


def set_test_user(username: str, password: str):
    """Sets a test user in the backend state."""
    with dependencies.user_store_session() as handle:
        user = User(
            username=username,
            hashed_password=passwords.get_password_hash(password),
        )
        handle.create_user(user)


@pytest.fixture(autouse=True)
def state_prep():
    yield
    # Reset state after every test.
    state_setup.clear_state()


@pytest.mark.parametrize("store_fixture_name", stores())
def test_authenticate_valid_user(
    store_fixture_name: str, request: pytest.FixtureRequest
) -> None:
    """Checks that an existing user can be properly authenticated."""
    username = "myuser"
    password = "mypassword"

    # Set user store in state before each test.
    state_setup.set_memory_user_store_in_state(store_fixture_name, request)

    set_test_user(username, password)

    success = authentication.authenticate_user(username, password)

    assert success


@pytest.mark.parametrize("store_fixture_name", stores())
def test_authenticate_inexistent_user(
    store_fixture_name: str, request: pytest.FixtureRequest
) -> None:
    """Checks that an inexistent user is not authenticated."""
    username = "myuser"
    password = "mypassword"

    # Set user store in state before each test.
    state_setup.set_memory_user_store_in_state(store_fixture_name, request)

    success = authentication.authenticate_user(username, password)

    assert not success


@pytest.mark.parametrize("store_fixture_name", stores())
def test_authenticate_wrong_password(
    store_fixture_name: str, request: pytest.FixtureRequest
) -> None:
    """Checks that a user with a wrong password can not be properly authenticated."""
    username = "myuser"
    password = "mypassword"

    # Set user store in state before each test.
    state_setup.set_memory_user_store_in_state(store_fixture_name, request)

    set_test_user(username, password)

    success = authentication.authenticate_user(username, "wrong_password")

    assert not success
