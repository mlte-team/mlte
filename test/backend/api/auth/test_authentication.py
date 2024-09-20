"""
test/backend/auth/test_authentication.py

Test the authentication operations
"""


import pytest

from mlte.backend.api.auth import authentication
from mlte.backend.core import state_stores
from mlte.backend.core.state import state
from mlte.store.user.store import UserStore
from mlte.store.user.store_session import UserStoreSession
from mlte.user.model import UserWithPassword
from test.store.user.fixture import (  # noqa
    fs_store,
    memory_store,
    rdbs_store,
    user_stores,
)

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def set_user_store_in_state(
    store_fixture_name: str, request: pytest.FixtureRequest
):
    """Sets an provided fixture user store in the backend state."""
    user_store: UserStore = request.getfixturevalue(store_fixture_name)
    state.set_user_store(user_store)


def clear_state():
    """Clears the the backend state."""
    state._artifact_store = None
    state._user_store = None


def set_test_user(
    username: str, password: str, user_store_session: UserStoreSession
):
    """Sets a test user in the backend state."""
    user = UserWithPassword(
        username=username,
        password=password,
    )
    user_store_session.user_mapper.create(user)


@pytest.fixture(autouse=True)
def state_prep():
    yield
    # Reset state after every test.
    clear_state()


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


@pytest.mark.parametrize("store_fixture_name", user_stores())
def test_authenticate_valid_user(
    store_fixture_name: str, request: pytest.FixtureRequest
) -> None:
    """Checks that an existing user can be properly authenticated."""
    username = "myuser"
    password = "mypassword"

    # Set user store in state before each test.
    set_user_store_in_state(store_fixture_name, request)

    with state_stores.user_store_session() as user_store_sesion:
        set_test_user(username, password, user_store_sesion)

        success = authentication.authenticate_user(
            username, password, user_store_sesion
        )

        assert success


@pytest.mark.parametrize("store_fixture_name", user_stores())
def test_authenticate_inexistent_user(
    store_fixture_name: str, request: pytest.FixtureRequest
) -> None:
    """Checks that an inexistent user is not authenticated."""
    username = "myuser"
    password = "mypassword"

    # Set user store in state before each test.
    set_user_store_in_state(store_fixture_name, request)

    with state_stores.user_store_session() as user_store_sesion:
        success = authentication.authenticate_user(
            username, password, user_store_sesion
        )

        assert not success


@pytest.mark.parametrize("store_fixture_name", user_stores())
def test_authenticate_wrong_password(
    store_fixture_name: str, request: pytest.FixtureRequest
) -> None:
    """Checks that a user with a wrong password can not be properly authenticated."""
    username = "myuser"
    password = "mypassword"

    # Set user store in state before each test.
    set_user_store_in_state(store_fixture_name, request)

    with state_stores.user_store_session() as user_store_sesion:
        set_test_user(username, password, user_store_sesion)

        success = authentication.authenticate_user(
            username, "wrong_password", user_store_sesion
        )

        assert not success
