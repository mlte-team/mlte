"""
mlte/store/artifact/underlying/fs.py

Implementation of local file system artifact store.
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Union

from mlte.store.base import StoreURI
from mlte.store.common.fs_storage import FileSystemStorage
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
# FileSystemUserStore
# -----------------------------------------------------------------------------


class FileSystemUserStore(UserStore):
    """A local file system implementation of the MLTE user store."""

    BASE_USERS_FOLDER = "users"
    """Base fodler to store users store in."""

    def __init__(self, uri: StoreURI) -> None:
        self.storage = FileSystemStorage(
            uri=uri, sub_folder=self.BASE_USERS_FOLDER
        )
        """Underlying storage."""

        # Initialize defaults.
        super().__init__(uri=uri)

    def session(self) -> FileSystemUserStoreSession:
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return FileSystemUserStoreSession(storage=self.storage)


# -----------------------------------------------------------------------------
# FileSystemUserStoreSession
# -----------------------------------------------------------------------------


class FileSystemUserStoreSession(UserStoreSession):
    """A local file-system implementation of the MLTE user store."""

    def __init__(self, storage: FileSystemStorage) -> None:
        self.permission_mapper = FileSystemPermissionMappper(storage)
        """The mapper to permisison CRUD."""

        self.group_mapper = FileSystemGroupMappper(storage)
        """The mapper to group CRUD."""

        self.user_mapper = FileSystemUserMappper(storage, self.group_mapper)
        """The mapper to user CRUD."""

    def close(self) -> None:
        """Close the session."""
        # Closing a local FS session is a no-op.
        pass


# -----------------------------------------------------------------------------
# FileSystemUserMappper
# -----------------------------------------------------------------------------


class FileSystemUserMappper(UserMapper):
    """FS mapper for the user resource."""

    USERS_FOLDER = "users"
    """Subfolder for users."""

    def __init__(
        self, storage: FileSystemStorage, group_mapper: FileSystemGroupMappper
    ) -> None:
        self.storage = storage.clone()
        """A reference to underlying storage."""

        self.group_mapper = group_mapper
        """Refernce to group mapper, to get updated groups when needed."""

        self.storage.set_base_path(
            Path(FileSystemUserStore.BASE_USERS_FOLDER, self.USERS_FOLDER)
        )
        """Set the subfodler for this resrouce."""

    def create(self, user: UserWithPassword) -> User:
        self.storage.ensure_resource_does_not_exist(user.username)

        new_user = user.to_hashed_user()

        # Only store group names for consistency.
        new_user.groups = Group.get_group_names(new_user.groups)

        return self._write_user(new_user)

    def edit(self, user: Union[UserWithPassword, BasicUser]) -> User:
        # NOTE: a JSON file may not have the updated group data, which can make reading the JSON confusing.
        self.storage.ensure_resource_exists(user.username)

        curr_user = self._read_user(user.username)
        updated_user = update_user_data(curr_user, user)

        # Only store group names for consistency.
        updated_user.groups = Group.get_group_names(updated_user.groups)

        return self._write_user(updated_user)

    def read(self, username: str) -> User:
        user = self._read_user(username)

        # Now get updated info for each group.
        up_to_date_groups: List[Group] = []
        for group in user.groups:
            up_to_date_groups.append(self.group_mapper.read(group.name))
        user.groups = up_to_date_groups

        return user

    def list(self) -> List[str]:
        return self.storage.list_resources()

    def delete(self, username: str) -> User:
        self.storage.ensure_resource_exists(username)
        user = self._read_user(username)
        self.storage.delete_resource(username)
        return user

    def _read_user(self, username: str) -> User:
        """
        Lazily construct a User object on read.
        :param username: The username
        :return: The user object
        """
        self.storage.ensure_resource_exists(username)
        return User(**self.storage.read_resource(username))

    def _write_user(self, user: User) -> User:
        """Writes a user to storage."""
        self.storage.write_resource(user.username, user.model_dump())
        return user


# -------------------------------------------------------------------------
# FileSystemGroupMappper
# -------------------------------------------------------------------------


class FileSystemGroupMappper(GroupMapper):
    """FS mapper for the group resource."""

    GROUPS_FOLDER = "groups"
    """Subfolder for groups."""

    def __init__(self, storage: FileSystemStorage) -> None:
        self.storage = storage.clone()
        """A reference to underlying storage."""

        self.storage.set_base_path(
            Path(FileSystemUserStore.BASE_USERS_FOLDER, self.GROUPS_FOLDER)
        )
        """Set the subfodler for this resrouce."""

    def create(self, group: Group) -> Group:
        self.storage.ensure_resource_does_not_exist(group.name)
        return self._write_group(group)

    def edit(self, group: Group) -> Group:
        self.storage.ensure_resource_exists(group.name)
        return self._write_group(group)

    def read(self, group_name: str) -> Group:
        return self._read_group(group_name)

    def list(self) -> List[str]:
        return self.storage.list_resources()

    def delete(self, group_name: str) -> Group:
        self.storage.ensure_resource_exists(group_name)
        group = self._read_group(group_name)
        self.storage.delete_resource(group_name)
        return group

    def _read_group(self, group_name: str) -> Group:
        """
        Lazily construct a Group object on read.
        :param group_name: The group name
        :return: The group object
        """
        self.storage.ensure_resource_exists(group_name)
        return Group(**self.storage.read_resource(group_name))

    def _write_group(self, group: Group) -> Group:
        """Writes a Group to storage."""
        self.storage.write_resource(group.name, group.model_dump())
        return self._read_group(group.name)


# -------------------------------------------------------------------------
# FileSystemPermissionMappper
# -------------------------------------------------------------------------


class FileSystemPermissionMappper(PermissionMapper):
    """FS mapper for the permission resource."""

    PERMISSIONS_FOLDER = "permissions"
    """Subfolder for permissions."""

    def __init__(self, storage: FileSystemStorage) -> None:
        self.storage = storage.clone()
        """A reference to underlying storage."""

        self.storage.set_base_path(
            Path(FileSystemUserStore.BASE_USERS_FOLDER, self.PERMISSIONS_FOLDER)
        )
        """Set the subfodler for this resrouce."""

    def create(self, permission: Permission) -> Permission:
        self.storage.ensure_resource_does_not_exist(permission.to_str())
        return self._write_permission(permission)

    def edit(self, permission: Permission) -> Permission:
        self.storage.ensure_resource_exists(permission.to_str())
        return self._write_permission(permission)

    def read(self, permission_str: str) -> Permission:
        return self._read_permission(permission_str)

    def list(self) -> List[str]:
        return self.storage.list_resources()

    def delete(self, permission_str: str) -> Permission:
        self.storage.ensure_resource_exists(permission_str)
        permission = self._read_permission(permission_str)
        self.storage.delete_resource(permission_str)
        return permission

    def _read_permission(self, permission_str: str) -> Permission:
        """
        Lazily construct a Permission object on read.
        :param permission_str: The permission str
        :return: The permission object
        """
        self.storage.ensure_resource_exists(permission_str)
        return Permission(**self.storage.read_resource(permission_str))

    def _write_permission(self, permission: Permission) -> Permission:
        """Writes a Permission to storage."""
        self.storage.write_resource(
            permission.to_str(), permission.model_dump()
        )
        return self._read_permission(permission.to_str())
