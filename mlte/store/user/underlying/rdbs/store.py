"""
mlte/store/user/underlying/rdbs/store.py

Implementation of relational database system user store.
"""
from __future__ import annotations

import typing
from typing import List, Optional, Union

from sqlalchemy import Engine, select
from sqlalchemy.orm import DeclarativeBase, Session

import mlte.store.error as errors
from mlte.store.base import StoreURI
from mlte.store.common.rdbs_storage import RDBStorage
from mlte.store.user.store import UserStore
from mlte.store.user.store_session import (
    GroupMapper,
    PermissionMapper,
    UserMapper,
    UserStoreSession,
)
from mlte.store.user.underlying.rdbs.metadata import (
    DBBase,
    DBGroup,
    DBPermission,
    DBUser,
    init_method_types,
    init_role_types,
)
from mlte.store.user.underlying.rdbs.reader import DBReader
from mlte.user.model import (
    BasicUser,
    Group,
    Permission,
    User,
    UserWithPassword,
    update_user_data,
)

# -----------------------------------------------------------------------------
# RelationalDBUserStore
# -----------------------------------------------------------------------------


class RelationalDBUserStore(UserStore):
    """A DB implementation of the MLTE user store."""

    def __init__(
        self,
        uri: StoreURI,
        add_default_data: bool = True,
        **kwargs,
    ) -> None:
        self.storage = RDBStorage(
            uri,
            base_class=typing.cast(DeclarativeBase, DBBase),
            init_tables_func=init_user_tables,
            **kwargs,
        )
        """The relational DB storage."""

        UserStore.__init__(self, uri, add_default_data)
        """Basic user setup."""

    def session(self) -> RelationalDBUserStoreSession:
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return RelationalDBUserStoreSession(storage=self.storage)


def init_user_tables(engine: Engine):
    """Pre-populate tables."""
    with Session(engine) as session:
        init_role_types(session)
        init_method_types(session)


# -----------------------------------------------------------------------------
# RelationalDBUserStoreSession
# -----------------------------------------------------------------------------


class RelationalDBUserStoreSession(UserStoreSession):
    """A relational DB implementation of the MLTE user store session."""

    def __init__(self, storage: RDBStorage) -> None:
        self.storage = storage
        """RDB storage."""

        self.user_mapper = RDBUserMapper(storage)
        """The mapper to user CRUD."""

        self.group_mapper = RDBGroupMapper(storage)
        """The mapper to group CRUD."""

        self.permission_mapper = RDBPermissionMapper(storage)
        """The mapper to group CRUD."""

    def close(self) -> None:
        """Close the session."""
        self.storage.close()


# -----------------------------------------------------------------------------
# RDBUserMapper
# -----------------------------------------------------------------------------


class RDBUserMapper(UserMapper):
    """RDB mapper for the user resource."""

    def __init__(self, storage: RDBStorage) -> None:
        self.storage = storage
        """A reference to underlying storage."""

    def create(self, user: UserWithPassword) -> User:
        with Session(self.storage.engine) as session:
            try:
                _, _ = DBReader.get_user(user.username, session)
                raise errors.ErrorAlreadyExists(
                    f"User with identifier {user.username} already exists."
                )
            except errors.ErrorNotFound:
                # If it was not found, it means we can create it.
                # Hash password and create a user with hashed passwords to be stored.
                hashed_user = user.to_hashed_user()
                user_obj = self._build_user(hashed_user, session)
                session.add(user_obj)
                session.commit()
                stored_user, _ = DBReader.get_user(user.username, session)
                return stored_user

    def edit(self, user: Union[UserWithPassword, BasicUser]) -> User:
        with Session(self.storage.engine) as session:
            curr_user, user_obj = DBReader.get_user(user.username, session)
            updated_user = update_user_data(curr_user, user)

            # Update existing user.
            user_obj = self._build_user(updated_user, session, user_obj)
            session.commit()

            stored_user, _ = DBReader.get_user(user.username, session)
            return stored_user

    def read(self, username: str) -> User:
        with Session(self.storage.engine) as session:
            user, _ = DBReader.get_user(username, session)
            return user

    def list(self) -> List[str]:
        users: List[str] = []
        with Session(self.storage.engine) as session:
            user_objs = session.scalars(select(DBUser))
            for user_obj in user_objs:
                users.append(user_obj.username)
        return users

    def delete(self, username: str) -> User:
        with Session(self.storage.engine) as session:
            user, user_obj = DBReader.get_user(username, session)
            session.delete(user_obj)
            session.commit()
            return user

    def _build_user(
        self, user: User, session: Session, user_obj: Optional[DBUser] = None
    ) -> DBUser:
        """Creates a DB user object from a model."""
        if user_obj is None:
            user_obj = DBUser()

        user_obj.username = user.username
        user_obj.email = user.email
        user_obj.full_name = user.full_name
        user_obj.disabled = user.disabled
        user_obj.hashed_password = user.hashed_password
        user_obj.role_type = DBReader.get_role_type(user.role, session)
        user_obj.groups = [
            DBReader.get_group(group_model.name, session)[1]
            for group_model in user.groups
        ]
        return user_obj


# -----------------------------------------------------------------------------
# RDBGroupMapper
# -----------------------------------------------------------------------------


class RDBGroupMapper(GroupMapper):
    """RDB mapper for the group resource"""

    def __init__(self, storage: RDBStorage) -> None:
        self.storage = storage
        """A reference to underlying storage."""

    def create(self, new_group: Group) -> Group:
        with Session(self.storage.engine) as session:
            try:
                _, _ = DBReader.get_group(new_group.name, session)
                raise errors.ErrorAlreadyExists(
                    f"Group with identifier {new_group.name} already exists."
                )
            except errors.ErrorNotFound:
                # If it was not found, it means we can create it.
                group_obj = self._build_group(new_group, session)
                session.add(group_obj)
                session.commit()
                return new_group

    def edit(self, updated_group: Group) -> Group:
        with Session(self.storage.engine) as session:
            _, group_obj = DBReader.get_group(updated_group.name, session)

            # Update existing group.
            group_obj = self._build_group(updated_group, session, group_obj)
            session.commit()

            return updated_group

    def read(self, group_name: str) -> Group:
        with Session(self.storage.engine) as session:
            group, _ = DBReader.get_group(group_name, session)
            return group

    def list(self) -> List[str]:
        groups: List[str] = []
        with Session(self.storage.engine) as session:
            group_objs = session.scalars(select(DBGroup))
            for group_obj in group_objs:
                groups.append(group_obj.name)
        return groups

    def delete(self, group_name: str) -> Group:
        with Session(self.storage.engine) as session:
            group, group_obj = DBReader.get_group(group_name, session)
            session.delete(group_obj)
            session.commit()
            return group

    def _build_group(
        self,
        group: Group,
        session: Session,
        group_obj: Optional[DBGroup] = None,
    ) -> DBGroup:
        """Creates a DB group object from a model."""
        if group_obj is None:
            group_obj = DBGroup()

        all_permissions, all_permission_objs = DBReader.get_permissions(session)

        group_obj.name = group.name
        group_obj.permissions = [
            all_permission_objs[i]
            for i, permission in enumerate(all_permissions)
            if permission in group.permissions
        ]

        return group_obj


# -----------------------------------------------------------------------------
# RDBPermissionMapper
# -----------------------------------------------------------------------------


class RDBPermissionMapper(PermissionMapper):
    """A interface for mapping CRUD actions to store permissions."""

    def __init__(self, storage: RDBStorage) -> None:
        self.storage = storage
        """A reference to underlying storage."""

    def create(self, new_permission: Permission) -> Permission:
        with Session(self.storage.engine) as session:
            try:
                _, _ = DBReader.get_permission(new_permission, session)
                raise errors.ErrorAlreadyExists(
                    f"{new_permission} already exists."
                )
            except errors.ErrorNotFound:
                # If it was not found, it means we can create it.
                permission_obj = DBPermission(
                    resource_type=new_permission.resource_type,
                    resource_id=new_permission.resource_id,
                    method_type=DBReader.get_method_type(
                        new_permission.method, session
                    ),
                )
                session.add(permission_obj)
                session.commit()
                return new_permission

    def read(self, permission: str) -> Permission:
        with Session(self.storage.engine) as session:
            perm, _ = DBReader.get_permission(
                Permission.from_str(permission), session
            )
            return perm

    def list(self) -> List[str]:
        with Session(self.storage.engine) as session:
            permissions, _ = DBReader.get_permissions(session)
            return [permission.to_str() for permission in permissions]

    def delete(self, permission: str) -> Permission:
        with Session(self.storage.engine) as session:
            perm, permission_obj = DBReader.get_permission(
                Permission.from_str(permission), session
            )
            session.delete(permission_obj)
            session.commit()
            return perm
