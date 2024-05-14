"""
mlte/store/user/store.py

MLTE user store interface implementation.
"""

from __future__ import annotations

from typing import List, Union, cast

from mlte.store import error
from mlte.store.base import ManagedSession, ResourceMapper, Store, StoreSession
from mlte.user.model import BasicUser, Group, Permission, User, UserCreate

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
            self.session().user_mapper.create(
                UserCreate(username=DEFAULT_USERNAME, password=DEFAULT_PASSWORD)
            )
        except error.ErrorAlreadyExists:
            # If default user was already there, ignore warning, we don't want to overrwite any changes on it.
            pass


# -----------------------------------------------------------------------------
# UserStoreSession
# -----------------------------------------------------------------------------


class UserStoreSession(StoreSession):
    """The base class for all implementations of the MLTE user store session."""

    def __init__(self):
        self.user_mapper = UserMapper()
        """Mapper for the user resource."""

        self.group_mapper = GroupMapper()
        """Mapper for the group resource."""

        self.permission_mapper = PermissionMapper()
        """Mapper for the permission resource."""


class ManagedUserSession(ManagedSession):
    """A simple context manager for store sessions."""

    def __enter__(self) -> UserStoreSession:
        return cast(UserStoreSession, self.session)


class UserMapper(ResourceMapper):
    """A interface for mapping CRUD actions to store users."""

    def create(self, new_user: UserCreate) -> User:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def edit(self, updated_user: Union[UserCreate, BasicUser]) -> User:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def read(self, user_id: str) -> User:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def list(self) -> List[str]:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def delete(self, user_id: str) -> User:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)


class GroupMapper(ResourceMapper):
    """A interface for mapping CRUD actions to store groups."""

    def create(self, new_group: Group) -> Group:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def edit(self, updated_group: Group) -> Group:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def read(self, group_id: str) -> Group:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def list(self) -> List[str]:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def delete(self, group_id: str) -> Group:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)


class PermissionMapper(ResourceMapper):
    """A interface for mapping CRUD actions to store permissions."""

    def create(self, new_permission: Permission) -> Permission:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def edit(self, updated_permission: Permission) -> Permission:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def read(self, permission: str) -> Permission:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def list(self) -> List[str]:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def delete(self, permission: str) -> Permission:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)
