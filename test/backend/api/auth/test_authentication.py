"""Test the authentication operations"""

import pytest

from mlte.backend.api.auth import authentication
from mlte.store.base import StoreType
from mlte.store.user.store import UserStore
from mlte.store.user.store_session import ManagedUserSession, UserStoreSession
from mlte.user.model import UserWithPassword
from test.store.utils import store_types

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def set_test_user(
    username: str, password: str, user_store_session: UserStoreSession
):
    """Sets a test user in the backend state."""
    user = UserWithPassword(
        username=username,
        password=password,
    )
    user_store_session.user_mapper.create(user)


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


@pytest.mark.parametrize("store_type", store_types())
def test_authenticate_valid_user(
    store_type: StoreType, create_test_user_store
) -> None:
    """Checks that an existing user can be properly authenticated."""
    username = "myuser"
    password = "mypassword"

    # Set user store in state before each test.
    user_store: UserStore = create_test_user_store(store_type)

    with ManagedUserSession(user_store.session()) as user_store_sesion:
        set_test_user(username, password, user_store_sesion)

        success = authentication.authenticate_user(
            username, password, user_store_sesion
        )

        assert success


@pytest.mark.parametrize("store_type", store_types())
def test_authenticate_inexistent_user(
    store_type: StoreType, create_test_user_store
) -> None:
    """Checks that an inexistent user is not authenticated."""
    username = "myuser"
    password = "mypassword"

    # Set user store in state before each test.
    user_store: UserStore = create_test_user_store(store_type)

    with ManagedUserSession(user_store.session()) as user_store_sesion:
        success = authentication.authenticate_user(
            username, password, user_store_sesion
        )

        assert not success


@pytest.mark.parametrize("store_type", store_types())
def test_authenticate_wrong_password(
    store_type: StoreType, create_test_user_store
) -> None:
    """Checks that a user with a wrong password can not be properly authenticated."""
    username = "myuser"
    password = "mypassword"

    # Set user store in state before each test.
    user_store: UserStore = create_test_user_store(store_type)

    with ManagedUserSession(user_store.session()) as user_store_sesion:
        set_test_user(username, password, user_store_sesion)

        success = authentication.authenticate_user(
            username, "wrong_password", user_store_sesion
        )

        assert not success
