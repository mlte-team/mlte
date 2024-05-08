"""
mlte/user/model.py

Model implementation for a User.
"""
from __future__ import annotations

from enum import Enum
from typing import List, Optional

from mlte.model import BaseModel

RESOURCE_ALL_VALUES = "*"
"""Special character used to identify all values of a certain permission."""

# -----------------------------------------------------------------------------
# User model (and sub-models)
# -----------------------------------------------------------------------------


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


# -----------------------------------------------------------------------------
# Group model (and sub-models)
# -----------------------------------------------------------------------------


class Group(BaseModel):
    """A user group to which permissions are associated."""

    name: str
    """The name of the group."""

    permissions: List[ResourceAction] = []
    """The permissions associated to the group."""


class ResourceAction(BaseModel):
    """Resources to be given permissions."""

    model_identifier: Optional[str] = None
    """The model to give permissions to."""

    url: str = RESOURCE_ALL_VALUES
    """The URL of the endpoint for the resource."""

    method: str = RESOURCE_ALL_VALUES
    """The HTTP method applied on the resource."""
