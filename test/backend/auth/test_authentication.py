"""
test/backend/auth/test_authentication.py

Test the authentication operations
"""


import pytest

from mlte.backend.api import dependencies
from mlte.backend.api.auth import authentication
from mlte.store.user.store import UserStoreSession
from mlte.user import passwords
from mlte.user.model import User

from ...store.user.fixture import memory_store, rdbs_store, stores  # noqa
from .. import state_setup


def set_test_user(
    username: str, password: str, user_store_session: UserStoreSession
):
    """Sets a test user in the backend state."""
    user = User(
        username=username,
        hashed_password=passwords.get_password_hash(password),
    )
    user_store_session.create_user(user)


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

    with dependencies.user_store_session() as user_store_sesion:
        set_test_user(username, password, user_store_sesion)

        success = authentication.authenticate_user(
            username, password, user_store_sesion
        )

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

    with dependencies.user_store_session() as user_store_sesion:
        success = authentication.authenticate_user(
            username, password, user_store_sesion
        )

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

    with dependencies.user_store_session() as user_store_sesion:
        set_test_user(username, password, user_store_sesion)

        success = authentication.authenticate_user(
            username, "wrong_password", user_store_sesion
        )

        assert not success
