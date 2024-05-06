"""
mlte/user/model.py

Model implementation for a User.
"""
from __future__ import annotations

from enum import Enum
from typing import List, Optional

from mlte.model import BaseModel


class RoleType(str, Enum):
    """Roles for users."""

    ADMIN = "admin"
    """An admin role, access to everything."""

    REGULAR = "regular"
    """A role with access to artifacts only."""


class BasicUser(BaseModel):
    """A model class representing a user of the system"""

    username: str
    """The username to uniquely identify a user."""

    email: Optional[str] = None
    """An optional email associated to the user."""

    full_name: Optional[str] = None
    """The full name of the user."""

    disabled: bool = False
    """Whether the user is disabled."""

    role: RoleType = RoleType.REGULAR
    """The role associated to the user."""

    groups: List[Group] = []
    """The groups the user is in."""


class User(BasicUser):
    """User with additional information only used locally when stored."""

    hashed_password: str
    """The hashed password of the user."""


class UserCreate(BasicUser):
    """User with additional information only used when creating a user."""

    password: str
    """The plain password of the user."""


class PermissionType(str, Enum):
    """Enumerates all supported permission types."""

    READ = "read"
    """Permission to read a specific model and its artifacts."""

    WRITE = "write"
    """Permission to write artifacts for a specific model."""


class Permission(BaseModel):
    """Permissions for specific artifacts."""

    permission_type: PermissionType = PermissionType.READ
    """The type of permisison granted."""

    model_identifier: str
    """The model to give permissions to."""


class Group(BaseModel):
    """A user group to which permissions are associated."""

    name: str
    """The name of the group."""

    permissions: List[PermissionType] = []
    """The permissions associated to the group."""
