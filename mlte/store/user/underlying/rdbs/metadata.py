"""
mlte/store/user/underlying/rdbs/metadata.py

Definition of the metadata (DB schema) for the user store.
"""
from __future__ import annotations

from typing import List, Optional

from sqlalchemy import ForeignKey, UniqueConstraint, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
)

from mlte.user.model import MethodType, RoleType


class DBBase(DeclarativeBase):
    """Base class for DB table classes."""

    pass


class DBUser(DBBase):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[Optional[str]]
    full_name: Mapped[Optional[str]]
    hashed_password: Mapped[str]
    disabled: Mapped[bool] = mapped_column(default=False)

    role_type_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("role_type.id")
    )
    role_type: Mapped[DBRoleType] = relationship("DBRoleType")

    groups: Mapped[List[DBGroup]] = relationship(
        "DBGroup", secondary="user_group", back_populates="users"
    )

    __table_args__ = (UniqueConstraint("username", name="_username"),)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, email={self.email!r}, name={self.full_name}, disabled={self.disabled!r})"


class DBUserGroup(DBBase):
    __tablename__ = "user_group"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), primary_key=True
    )
    group_id: Mapped[int] = mapped_column(
        ForeignKey("group.id"), primary_key=True
    )


class DBGroup(DBBase):
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    users: Mapped[List[DBUser]] = relationship(
        DBUser, secondary="user_group", back_populates="groups"
    )
    permissions: Mapped[List[DBPermission]] = relationship(
        "DBPermission", secondary="group_permission", back_populates="groups"
    )

    __table_args__ = (UniqueConstraint("name", name="_group_name"),)

    def __repr__(self) -> str:
        return f"Group(id={self.id!r}, name={self.name!r})"


class DBGroupPermission(DBBase):
    __tablename__ = "group_permission"

    group_id: Mapped[int] = mapped_column(
        ForeignKey("group.id"), primary_key=True
    )
    permission_id: Mapped[int] = mapped_column(
        ForeignKey("permission.id"), primary_key=True
    )


class DBPermission(DBBase):
    __tablename__ = "permission"

    id: Mapped[int] = mapped_column(primary_key=True)
    resource_type: Mapped[str]
    resource_id: Mapped[Optional[str]]

    method_type_id: Mapped[int] = mapped_column(ForeignKey("method_type.id"))
    method_type: Mapped[DBMethodType] = relationship()

    groups: Mapped[List[DBGroup]] = relationship(
        DBGroup,
        secondary="group_permission",
        back_populates="permissions",
        cascade="all",
    )

    def __repr__(self) -> str:
        return f"Permission(id={self.id!r}, resource_type={self.resource_type}, resource_id={self.resource_id!r}, method={self.method_type})"


class DBRoleType(DBBase):
    __tablename__ = "role_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    def __repr__(self) -> str:
        return f"RoleType(id={self.id!r}, name={self.name!r})"


class DBMethodType(DBBase):
    __tablename__ = "method_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    def __repr__(self) -> str:
        return f"MethodType(id={self.id!r}, name={self.name!r})"


# -------------------------------------------------------------------------
# Pre-filled table functions.
# -------------------------------------------------------------------------


def init_role_types(session: Session):
    """Initializes the table with the configured role types."""
    if session.scalars(select(DBRoleType)).first() is None:
        types = [e.value for e in RoleType]
        for type in types:
            type_obj = DBRoleType(name=type)
            session.add(type_obj)
        session.commit()


def init_method_types(session: Session):
    """Initializes the table with the configured method types."""
    if session.scalars(select(DBMethodType)).first() is None:
        types = [e.value for e in MethodType]
        for type in types:
            type_obj = DBMethodType(name=type)
            session.add(type_obj)
        session.commit()
