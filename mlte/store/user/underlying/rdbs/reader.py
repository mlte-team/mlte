"""DB utils for getting user related data from the DB.
"""

from __future__ import annotations

from typing import List, Tuple

from sqlalchemy import select
from sqlalchemy.orm import Session

import mlte.store.error as errors
from mlte.store.user.underlying.rdbs.metadata import (
    DBGroup,
    DBMethodType,
    DBPermission,
    DBRoleType,
    DBUser,
)
from mlte.user.model import (
    Group,
    MethodType,
    Permission,
    ResourceType,
    RoleType,
    User,
)


class DBReader:
    """Class encapsulating functions to read user related data from the DB."""

    @staticmethod
    def get_user(username: str, session: Session) -> Tuple[User, DBUser]:
        """Reads the user with the given user using the provided session, and returns a User and DBUser object."""
        user_orm = session.scalar(
            select(DBUser).where(DBUser.username == username)
        )

        if user_orm is None:
            raise errors.ErrorNotFound(
                f"User with username {username} was not found in the user store."
            )
        else:
            return (
                User(
                    username=user_orm.username,
                    email=user_orm.email,
                    full_name=user_orm.full_name,
                    disabled=user_orm.disabled,
                    hashed_password=user_orm.hashed_password,
                    role=RoleType(user_orm.role_type.name),
                    groups=[
                        DBReader._build_group(group_orm, session)
                        for group_orm in user_orm.groups
                    ],
                ),
                user_orm,
            )

    @staticmethod
    def get_group(group_name: str, session: Session) -> Tuple[Group, DBGroup]:
        """Reads the group with the given name using the provided session, and returns a Group and DBGroup object."""
        group_orm = session.scalar(
            select(DBGroup).where(DBGroup.name == group_name)
        )

        if group_orm is None:
            raise errors.ErrorNotFound(
                f"Group with name {group_name} was not found in the user store."
            )
        else:
            return (DBReader._build_group(group_orm, session), group_orm)

    @staticmethod
    def _build_group(
        group_orm: DBGroup,
        session: Session,
    ) -> Group:
        """Builds a Group object out of its DB model."""
        all_permissions, all_permissions_db = DBReader.get_permissions(session)
        return Group(
            name=group_orm.name,
            permissions=[
                all_permissions[i]
                for i, permission_obj in enumerate(all_permissions_db)
                if group_orm in permission_obj.groups
            ],
        )

    @staticmethod
    def get_permission(
        permission: Permission,
        session: Session,
    ) -> Tuple[Permission, DBPermission]:
        """Reads a permission from the DB, and returns a Permission and DBPermission objects."""
        permissions_orm = session.scalar(
            select(DBPermission)
            .where(DBPermission.resource_id == permission.resource_id)
            .where(DBPermission.resource_type == permission.resource_type)
            .where(DBPermission.method_type_id == DBMethodType.id)
            .where(DBMethodType.name == permission.method.value)
        )

        if permissions_orm is None:
            raise errors.ErrorNotFound(
                f"{permission.to_str()} was not found in the user store."
            )
        else:
            return permission, permissions_orm

    @staticmethod
    def get_permissions(
        session: Session,
    ) -> Tuple[List[Permission], List[DBPermission]]:
        """Reads all permissions in the DB, and returns a list of Permission and DBPermission objects."""
        permissions_orm = list(
            session.execute(select(DBPermission)).scalars().all()
        )
        permissions: List[Permission] = []
        for permission_orm in permissions_orm:
            permission = Permission(
                resource_type=ResourceType(permission_orm.resource_type),
                resource_id=permission_orm.resource_id,
                method=MethodType(permission_orm.method_type.name),
            )
            permissions.append(permission)

        return permissions, permissions_orm

    @staticmethod
    def get_role_type(type: RoleType, session: Session) -> DBRoleType:
        """Gets the role type DB object corresponding to the given internal type."""
        type_orm = session.scalar(
            select(DBRoleType).where(DBRoleType.name == type)
        )

        if type_orm is None:
            raise Exception(f"Unknown role type requested: {type}")
        return type_orm

    @staticmethod
    def get_method_type(type: MethodType, session: Session) -> DBMethodType:
        """Gets the method type DB object corresponding to the given internal type."""
        type_orm = session.scalar(
            select(DBMethodType).where(DBMethodType.name == type)
        )

        if type_orm is None:
            raise Exception(f"Unknown method type requested: {type}")
        return type_orm
