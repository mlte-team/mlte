"""
mlte/store/user/underlying/memory.py

Implementation of in-memory user store.
"""

from __future__ import annotations

from typing import Dict, List, Union

import mlte.store.error as errors
from mlte.store.base import StoreURI
from mlte.store.user.store import UserStore
from mlte.store.user.store_session import (
    GroupMapper,
    PermissionMapper,
    UserMapper,
    UserStoreSession,
)
from mlte.user.model import (
    BasicUser,
    Group,
    Permission,
    User,
    UserWithPassword,
    update_user_data,
)

# -----------------------------------------------------------------------------
# Memory Store
# -----------------------------------------------------------------------------


class InMemoryUserStore(UserStore):
    """An in-memory implementation of the MLTE user store."""

    def __init__(self, uri: StoreURI, add_default_data: bool = True) -> None:
        self.storage = MemoryUserStorage()
        """The underlying storage for the store."""

        # Initialize defaults.
        super().__init__(uri=uri, add_default_data=add_default_data)

    def session(self) -> InMemoryUserStoreSession:
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return InMemoryUserStoreSession(storage=self.storage)

    def clone(self) -> InMemoryUserStore:
        """
        Clones the store. Shallow clone.
        :return: The cloned store
        """
        clone = InMemoryUserStore(self.uri, add_default_data=False)
        clone.storage.users = self.storage.users.copy()
        clone.storage.groups = self.storage.groups.copy()
        clone.storage.permissions = self.storage.permissions.copy()
        return clone


class MemoryUserStorage:
    """A simple storage wrapper for the in-memory store."""

    def __init__(self) -> None:
        self.users: Dict[str, User] = {}
        self.groups: Dict[str, Group] = {}
        self.permissions: Dict[str, Permission] = {}


# -----------------------------------------------------------------------------
# InMemoryStoreSession
# -----------------------------------------------------------------------------


class InMemoryUserStoreSession(UserStoreSession):
    """An in-memory implementation of the MLTE user store."""

    def __init__(self, *, storage: MemoryUserStorage) -> None:
        self.permission_mapper = InMemoryPermissionMapper(storage=storage)
        """The mapper to permission CRUD."""

        self.group_mapper = InMemoryGroupMapper(storage=storage)
        """The mapper to group CRUD."""

        self.user_mapper = InMemoryUserMapper(
            storage=storage, group_mapper=self.group_mapper
        )
        """The mapper to user CRUD."""

    def close(self) -> None:
        """Close the session."""
        # Closing an in-memory session is a no-op.
        pass


class InMemoryUserMapper(UserMapper):
    """In-memory mapper for the user resource."""

    def __init__(
        self, *, storage: MemoryUserStorage, group_mapper: InMemoryGroupMapper
    ) -> None:
        self.storage = storage
        """A reference to underlying storage."""

        self.group_mapper = group_mapper
        """A reference to the group mapper, to get updated group info if needed."""

    def create(self, user: UserWithPassword) -> User:
        if user.username in self.storage.users:
            raise errors.ErrorAlreadyExists(f"User {user.username}")

        # Create user with hashed passwords.
        stored_user = user.to_hashed_user()

        # Only store group names for consistency.
        user.groups = Group.get_group_names(user.groups)

        self.storage.users[user.username] = stored_user
        return stored_user

    def edit(self, user: Union[UserWithPassword, BasicUser]) -> User:
        if user.username not in self.storage.users:
            raise errors.ErrorNotFound(f"User {user.username}")

        curr_user = self.storage.users[user.username]
        updated_user = update_user_data(curr_user, user)

        # Only store group names for consistency.
        user.groups = Group.get_group_names(user.groups)

        self.storage.users[user.username] = updated_user
        return curr_user

    def read(self, username: str) -> User:
        if username not in self.storage.users:
            raise errors.ErrorNotFound(f"User {username}")
        user = self.storage.users[username]

        # Now get updated info for each group.
        up_to_date_groups: List[Group] = []
        for group in user.groups:
            up_to_date_groups.append(self.group_mapper.read(group.name))
        user.groups = up_to_date_groups

        return user

    def list(self) -> List[str]:
        return [username for username in self.storage.users.keys()]

    def delete(self, username: str) -> User:
        if username not in self.storage.users:
            raise errors.ErrorNotFound(f"User {username}")

        popped = self.storage.users[username]
        del self.storage.users[username]
        return popped


class InMemoryGroupMapper(GroupMapper):
    """In-memory mapper for the group resource."""

    def __init__(self, *, storage: MemoryUserStorage) -> None:
        self.storage = storage
        """A reference to underlying storage."""

    def create(self, group: Group) -> Group:
        if group.name in self.storage.groups:
            raise errors.ErrorAlreadyExists(f"Group {group.name}")
        self.storage.groups[group.name] = group
        return group

    def edit(self, updated_group: Group) -> Group:
        if updated_group.name not in self.storage.groups:
            raise errors.ErrorNotFound(f"Group {updated_group.name}")

        self.storage.groups[updated_group.name] = updated_group
        return self.read(updated_group.name)

    def read(self, group_name: str) -> Group:
        if group_name not in self.storage.groups:
            raise errors.ErrorNotFound(f"Group {group_name}")
        return self.storage.groups[group_name]

    def list(self) -> List[str]:
        return [group_name for group_name in self.storage.groups.keys()]

    def delete(self, group_name: str) -> Group:
        if group_name not in self.storage.groups:
            raise errors.ErrorNotFound(f"Group {group_name}")

        popped = self.storage.groups[group_name]
        del self.storage.groups[group_name]
        return popped


class InMemoryPermissionMapper(PermissionMapper):
    """In-memory mapper for the permission resource."""

    def __init__(self, *, storage: MemoryUserStorage) -> None:
        self.storage = storage
        """A reference to underlying storage."""

    def create(self, permission: Permission) -> Permission:
        if permission.to_str() in self.storage.permissions:
            raise errors.ErrorAlreadyExists(f"Permission {permission.to_str()}")
        self.storage.permissions[permission.to_str()] = permission
        return permission

    def read(self, permission_str: str) -> Permission:
        if permission_str not in self.storage.permissions:
            raise errors.ErrorNotFound(f"Permission {permission_str}")
        return self.storage.permissions[permission_str]

    def list(self) -> List[str]:
        return [
            permission_str for permission_str in self.storage.permissions.keys()
        ]

    def delete(self, permission_str: str) -> Permission:
        if permission_str not in self.storage.permissions:
            raise errors.ErrorNotFound(f"Permission {permission_str}")

        popped = self.storage.permissions[permission_str]
        del self.storage.permissions[permission_str]
        return popped
