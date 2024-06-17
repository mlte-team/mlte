"""
mlte/store/user/underlying/rdbs/reader.py

DB utils for getting user related data from the DB.
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
        user_obj = session.scalar(
            select(DBUser).where(DBUser.username == username)
        )

        if user_obj is None:
            raise errors.ErrorNotFound(
                f"User with username {username} was not found in the user store."
            )
        else:
            return (
                User(
                    username=user_obj.username,
                    email=user_obj.email,
                    full_name=user_obj.full_name,
                    disabled=user_obj.disabled,
                    hashed_password=user_obj.hashed_password,
                    role=RoleType(user_obj.role_type.name),
                    groups=[
                        DBReader._build_group(group_obj, session)
                        for group_obj in user_obj.groups
                    ],
                ),
                user_obj,
            )

    @staticmethod
    def get_group(group_name: str, session: Session) -> Tuple[Group, DBGroup]:
        """Reads the group with the given name using the provided session, and returns a Group and DBGroup object."""
        group_obj = session.scalar(
            select(DBGroup).where(DBGroup.name == group_name)
        )

        if group_obj is None:
            raise errors.ErrorNotFound(
                f"Group with name {group_name} was not found in the user store."
            )
        else:
            return (DBReader._build_group(group_obj, session), group_obj)

    @staticmethod
    def _build_group(
        group_obj: DBGroup,
        session: Session,
    ) -> Group:
        """Builds a Group object out of its DB model."""
        all_permissions, all_permissions_db = DBReader.get_permissions(session)
        return Group(
            name=group_obj.name,
            permissions=[
                all_permissions[i]
                for i, permission_obj in enumerate(all_permissions_db)
                if group_obj in permission_obj.groups
            ],
        )

    @staticmethod
    def get_permission(
        permission: Permission,
        session: Session,
    ) -> Tuple[Permission, DBPermission]:
        """Reads a permission from the DB, and returns a Permission and DBPermission objects."""
        permissions_obj = session.scalar(
            select(DBPermission)
            .where(DBPermission.resource_id == permission.resource_id)
            .where(DBPermission.resource_type == permission.resource_type)
            .where(DBPermission.method_type_id == DBMethodType.id)
            .where(DBMethodType.name == permission.method.value)
        )

        if permissions_obj is None:
            raise errors.ErrorNotFound(
                f"{permission.to_str()} was not found in the user store."
            )
        else:
            return permission, permissions_obj

    @staticmethod
    def get_permissions(
        session: Session,
    ) -> Tuple[List[Permission], List[DBPermission]]:
        """Reads all permissions in the DB, and returns a list of Permission and DBPermission objects."""
        permissions_obj = list(
            session.execute(select(DBPermission)).scalars().all()
        )
        permissions: List[Permission] = []
        for permission_obj in permissions_obj:
            permission = Permission(
                resource_type=ResourceType(permission_obj.resource_type),
                resource_id=permission_obj.resource_id,
                method=MethodType(permission_obj.method_type.name),
            )
            permissions.append(permission)

        return permissions, permissions_obj

    @staticmethod
    def get_role_type(type: RoleType, session: Session) -> DBRoleType:
        """Gets the role type DB object corresponding to the given internal type."""
        type_obj = session.scalar(
            select(DBRoleType).where(DBRoleType.name == type)
        )

        if type_obj is None:
            raise Exception(f"Unknown role type requested: {type}")
        return type_obj

    @staticmethod
    def get_method_type(type: MethodType, session: Session) -> DBMethodType:
        """Gets the method type DB object corresponding to the given internal type."""
        type_obj = session.scalar(
            select(DBMethodType).where(DBMethodType.name == type)
        )

        if type_obj is None:
            raise Exception(f"Unknown method type requested: {type}")
        return type_obj
