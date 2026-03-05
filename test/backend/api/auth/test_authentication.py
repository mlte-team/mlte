"""Test the authentication operations"""

import pytest

from mlte.backend.api.auth import authentication
from mlte.backend.core import state_stores
from mlte.backend.core.state import state
from mlte.store.user.store import UserStore
from mlte.store.user.store_session import UserStoreSession
from mlte.user.model import UserWithPassword
from test.store.fixture import store_types  # noqa
from test.store.user.fixture import create_test_user_store  # noqa

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def set_user_store_in_state(store_type: str, create_test_store):  # noqa
    """Sets an provided fixture user store in the backend state."""
    store: UserStore = create_test_store(store_type)
    state.stores.set_user_store(store)


def clear_state():
    """Clears the the backend state."""
    state.reset()


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


@pytest.mark.parametrize("store_type", store_types())
def test_authenticate_valid_user(
    store_type: str, create_test_user_store  # noqa
) -> None:  # noqa
    """Checks that an existing user can be properly authenticated."""
    username = "myuser"
    password = "mypassword"

    # Set user store in state before each test.
    set_user_store_in_state(store_type, create_test_user_store)

    with state_stores.user_store_session() as user_store_sesion:
        set_test_user(username, password, user_store_sesion)

        success = authentication.authenticate_user(
            username, password, user_store_sesion
        )

        assert success


@pytest.mark.parametrize("store_type", store_types())
def test_authenticate_inexistent_user(
    store_type: str, create_test_user_store  # noqa
) -> None:
    """Checks that an inexistent user is not authenticated."""
    username = "myuser"
    password = "mypassword"

    # Set user store in state before each test.
    set_user_store_in_state(store_type, create_test_user_store)

    with state_stores.user_store_session() as user_store_sesion:
        success = authentication.authenticate_user(
            username, password, user_store_sesion
        )

        assert not success


@pytest.mark.parametrize("store_type", store_types())
def test_authenticate_wrong_password(
    store_type: str, create_test_user_store  # noqa
) -> None:
    """Checks that a user with a wrong password can not be properly authenticated."""
    username = "myuser"
    password = "mypassword"

    # Set user store in state before each test.
    set_user_store_in_state(store_type, create_test_user_store)

    with state_stores.user_store_session() as user_store_sesion:
        set_test_user(username, password, user_store_sesion)

        success = authentication.authenticate_user(
            username, "wrong_password", user_store_sesion
        )

        assert not success
