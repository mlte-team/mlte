"""
mlte/store/user/store.py

MLTE user store interface implementation.
"""

from __future__ import annotations

from typing import List, Union, cast

from mlte.store import error
from mlte.store.base import ManagedSession, Store, StoreSession
from mlte.user.model import BasicUser, User, UserCreate

DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "admin1234"
"""Default user for setup."""


# -----------------------------------------------------------------------------
# UserStore
# -----------------------------------------------------------------------------


class UserStore(Store):
    """
    An abstract user store.
    """

    def session(self) -> UserStoreSession:
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        raise NotImplementedError("Cannot get handle to abstract Store.")

    def _init_default_user(self):
        """Adds the default user."""
        try:
            self.session().create_user(
                UserCreate(username=DEFAULT_USERNAME, password=DEFAULT_PASSWORD)
            )
        except error.ErrorAlreadyExists:
            # If default user was already there, ignore warning, we don't want to overrwite any changes on it.
            pass


# -----------------------------------------------------------------------------
# ArtifactStoreSession
# -----------------------------------------------------------------------------


class UserStoreSession(StoreSession):
    """The base class for all implementations of the MLTE user store session."""

    NOT_IMPLEMENTED_ERROR_MSG = (
        "Cannot invoke method on abstract UserStoreSession."
    )
    """Default error message for this abstract class."""

    # -------------------------------------------------------------------------
    # Interface: Context
    # -------------------------------------------------------------------------

    def create_user(self, user: UserCreate) -> User:
        """
        Create a user.
        :param user: The data to create the user
        :return: The created user
        """
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def edit_user(self, user: Union[UserCreate, BasicUser]) -> User:
        """
        Edit an existing user.
        :param user: The data to edit the user
        :return: The edited user
        """
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def read_user(self, username: str) -> User:
        """
        Read a user.
        :param username: The identifier for the user
        :return: The user
        """
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def list_users(self) -> List[str]:
        """
        List all users in the store.
        :return: A collection of identifiers for all users
        """
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def delete_user(self, username: str) -> User:
        """
        Delete a user.
        :param username: The identifier for the user
        :return: The deleted user
        """
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)


class ManagedUserSession(ManagedSession):
    """A simple context manager for store sessions."""

    def __enter__(self) -> UserStoreSession:
        return cast(UserStoreSession, self.session)
