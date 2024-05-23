"""
mlte/store/user/underlying/rdbs/store.py

Implementation of relational database system user store.
"""
from __future__ import annotations

from typing import List, Optional, Union

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy_utils
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

import mlte.store.error as errors
from mlte.store.base import StoreURI
from mlte.store.user.store import (
    GroupMapper,
    PermissionMapper,
    UserMapper,
    UserStore,
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
from mlte.user.model import BasicUser, Group, Permission, User, UserCreate
from mlte.user.model_logic import convert_to_hashed_user, update_user

# -----------------------------------------------------------------------------
# RelationalDBUserStore
# -----------------------------------------------------------------------------


class RelationalDBUserStore(UserStore):
    """A DB implementation of the MLTE user store."""

    def __init__(self, uri: StoreURI, **kwargs) -> None:
        self.engine = sqlalchemy.create_engine(uri.uri, **kwargs)
        """The underlying storage for the store."""

        # Create the DB if it doesn't exist already.
        if not sqlalchemy_utils.database_exists(self.engine.url):
            sqlalchemy_utils.create_database(self.engine.url)

        # Creates the DB items if they don't exist already.
        self._create_tables()
        self._init_tables()

        # Intialize base defaults.
        super().__init__(uri=uri)

    def session(self) -> RelationalDBUserStoreSession:  # type: ignore[override]
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return RelationalDBUserStoreSession(engine=self.engine)

    def _create_tables(self):
        """Creates all items, if they don't exist already."""
        DBBase.metadata.create_all(self.engine)

    def _init_tables(self):
        """Pre-populate tables."""
        with Session(self.engine) as session:
            init_role_types(session)
            init_method_types(session)


# -----------------------------------------------------------------------------
# RelationalDBUserStoreSession
# -----------------------------------------------------------------------------


class RelationalDBUserStoreSession(UserStoreSession):
    """A relational DB implementation of the MLTE user store session."""

    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        """A reference to underlying storage."""

        self.user_mapper = RDBUserMapper(engine)
        """The mapper to user CRUD."""

        self.group_mapper = RDBGroupMapper(engine)
        """The mapper to group CRUD."""

        self.permission_mapper = RDBPermissionMapper(engine)
        """The mapper to group CRUD."""

    def close(self) -> None:
        """Close the session."""
        self.engine.dispose()


# -----------------------------------------------------------------------------
# RDBUserMapper
# -----------------------------------------------------------------------------


class RDBUserMapper(UserMapper):
    """RDB mapper for the user resource."""

    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        """A reference to underlying storage."""

    def create(self, user: UserCreate) -> User:
        with Session(self.engine) as session:
            try:
                _, _ = DBReader.get_user(user.username, session)
                raise errors.ErrorAlreadyExists(
                    f"User with identifier {user.username} already exists."
                )
            except errors.ErrorNotFound:
                # If it was not found, it means we can create it.
                # Hash password and create a user with hashed passwords to be stored.
                hashed_user = convert_to_hashed_user(user)
                user_obj = self._build_user(hashed_user, session)
                session.add(user_obj)
                session.commit()
                return hashed_user

    def edit(self, user: Union[UserCreate, BasicUser]) -> User:
        with Session(self.engine) as session:
            curr_user, user_obj = DBReader.get_user(user.username, session)
            updated_user = update_user(curr_user, user)

            # Update existing user.
            user_obj = self._build_user(updated_user, session, user_obj)
            session.commit()

            return updated_user

    def read(self, username: str) -> User:
        with Session(self.engine) as session:
            user, _ = DBReader.get_user(username, session)
            return user

    def list(self) -> List[str]:
        users: List[str] = []
        with Session(self.engine) as session:
            user_objs = session.scalars(select(DBUser))
            for user_obj in user_objs:
                users.append(user_obj.username)
        return users

    def delete(self, username: str) -> User:
        with Session(self.engine) as session:
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

    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        """A reference to underlying storage."""

    def create(self, new_group: Group) -> Group:
        with Session(self.engine) as session:
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
        with Session(self.engine) as session:
            _, group_obj = DBReader.get_group(updated_group.name, session)

            # Update existing group.
            group_obj = self._build_group(updated_group, session, group_obj)
            session.commit()

            return updated_group

    def read(self, group_name: str) -> Group:
        with Session(self.engine) as session:
            group, _ = DBReader.get_group(group_name, session)
            return group

    def list(self) -> List[str]:
        groups: List[str] = []
        with Session(self.engine) as session:
            group_objs = session.scalars(select(DBGroup))
            for group_obj in group_objs:
                groups.append(group_obj.name)
        return groups

    def delete(self, group_name: str) -> Group:
        with Session(self.engine) as session:
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

    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        """A reference to underlying storage."""

    def create(self, new_permission: Permission) -> Permission:
        with Session(self.engine) as session:
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
        with Session(self.engine) as session:
            perm, _ = DBReader.get_permission(
                Permission.from_str(permission), session
            )
            return perm

    def list(self) -> List[str]:
        with Session(self.engine) as session:
            permissions, _ = DBReader.get_permissions(session)
            return [permission.to_str() for permission in permissions]

    def delete(self, permission: str) -> Permission:
        with Session(self.engine) as session:
            perm, permission_obj = DBReader.get_permission(
                Permission.from_str(permission), session
            )
            session.delete(permission_obj)
            session.commit()
            return perm
