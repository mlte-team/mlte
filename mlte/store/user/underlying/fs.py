"""
mlte/store/artifact/underlying/fs.py

Implementation of local file system artifact store.
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Union

import mlte.store.error as errors
from mlte.store.base import StoreURI
from mlte.store.common.fs import FileSystemStorage
from mlte.store.user.store import UserStore
from mlte.store.user.store_session import (
    GroupMapper,
    PermissionMapper,
    UserMapper,
    UserStoreSession,
)
from mlte.user.model import BasicUser, Group, Permission, User, UserCreate
from mlte.user.model_logic import convert_to_hashed_user, update_user

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
        self.user_mapper = FileSystemUserMappper(storage)
        """The mapper to user CRUD."""

        self.group_mapper = FileSystemGroupMappper(storage)
        """The mapper to group CRUD."""

        self.permission_mapper = FileSystemPermissionMappper(storage)
        """The mapper to permisison CRUD."""

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

    def __init__(self, storage: FileSystemStorage) -> None:
        self.storage = storage.clone()
        """A reference to underlying storage."""

        self.storage.set_base_path(
            Path(FileSystemUserStore.BASE_USERS_FOLDER, self.USERS_FOLDER)
        )
        """Set the subfodler for this resrouce."""

    def create(self, user: UserCreate) -> User:
        if self.storage._resource_path(user.username).exists():
            raise errors.ErrorAlreadyExists(f"User '{user.username}'")

        new_user = convert_to_hashed_user(user)
        return self._write_user(new_user)

    def edit(self, user: Union[UserCreate, BasicUser]) -> User:
        if not self.storage._resource_path(user.username).exists():
            raise errors.ErrorNotFound(f"User '{user.username}'")

        updated_user = update_user(self._read_user(user.username), user)
        return self._write_user(updated_user)

    def read(self, username: str) -> User:
        return self._read_user(username)

    def list(self) -> List[str]:
        return [
            self.storage.get_just_filename(user_path)
            for user_path in self.storage.list_json_files(
                self.storage.base_path
            )
        ]

    def delete(self, username: str) -> User:
        self.storage._ensure_resource_exists(username)
        user = self._read_user(username)
        self.storage.delete_file(self.storage._resource_path(username))
        return user

    def _read_user(self, username: str) -> User:
        """
        Lazily construct a User object on read.
        :param username: The username
        :return: The user object
        """
        self.storage._ensure_resource_exists(username)
        return User(
            **self.storage.read_json_file(self.storage._resource_path(username))
        )

    def _write_user(self, user: User) -> User:
        """Writes a user to storage."""
        self.storage.write_json_to_file(
            self.storage._resource_path(user.username),
            user.model_dump(),
        )
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
        if self.storage._resource_path(group.name).exists():
            raise errors.ErrorAlreadyExists(f"Group '{group.name}'")
        return self._write_group(group)

    def edit(self, group: Group) -> Group:
        if not self.storage._resource_path(group.name).exists():
            raise errors.ErrorNotFound(f"Group '{group.name}'")
        return self._write_group(group)

    def read(self, group_name: str) -> Group:
        return self._read_group(group_name)

    def list(self) -> List[str]:
        return [
            self.storage.get_just_filename(group_path)
            for group_path in self.storage.list_json_files(
                self.storage.base_path
            )
        ]

    def delete(self, group_name: str) -> Group:
        self.storage._ensure_resource_exists(group_name)
        group = self._read_group(group_name)
        self.storage.delete_file(self.storage._resource_path(group_name))
        return group

    def _read_group(self, group_name: str) -> Group:
        """
        Lazily construct a Group object on read.
        :param group_name: The group name
        :return: The group object
        """
        self.storage._ensure_resource_exists(group_name)
        return Group(
            **self.storage.read_json_file(
                self.storage._resource_path(group_name)
            )
        )

    def _write_group(self, group: Group) -> Group:
        """Writes a Group to storage."""
        self.storage.write_json_to_file(
            self.storage._resource_path(group.name),
            group.model_dump(),
        )
        return group


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
        if self.storage._resource_path(permission.to_str()).exists():
            raise errors.ErrorAlreadyExists(
                f"Permission '{permission.to_str()}'"
            )
        return self._write_permission(permission)

    def edit(self, permission: Permission) -> Permission:
        if not self.storage._resource_path(permission.to_str()).exists():
            raise errors.ErrorNotFound(f"Permission '{permission.to_str()}'")
        return self._write_permission(permission)

    def read(self, permission_str: str) -> Permission:
        return self._read_permission(permission_str)

    def list(self) -> List[str]:
        return [
            self.storage.get_just_filename(perm_path)
            for perm_path in self.storage.list_json_files(
                self.storage.base_path
            )
        ]

    def delete(self, permission_str: str) -> Permission:
        self.storage._ensure_resource_exists(permission_str)
        permission = self._read_permission(permission_str)
        self.storage.delete_file(self.storage._resource_path(permission_str))
        return permission

    def _read_permission(self, permission_str: str) -> Permission:
        """
        Lazily construct a Permission object on read.
        :param permission_str: The permission str
        :return: The permission object
        """
        self.storage._ensure_resource_exists(permission_str)
        return Permission(
            **self.storage.read_json_file(
                self.storage._resource_path(permission_str)
            )
        )

    def _write_permission(self, permission: Permission) -> Permission:
        """Writes a Permission to storage."""
        self.storage.write_json_to_file(
            self.storage._resource_path(permission.to_str()),
            permission.model_dump(),
        )
        return permission
