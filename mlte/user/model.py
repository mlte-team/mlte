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


class MethodType(str, Enum):
    """Types of methods for permissions."""

    GET = "get"
    """Get or read action."""

    POST = "post"
    """Creation action."""

    PUT = "put"
    """Action to edit."""

    DELETE = "delete"
    """Deletion action."""

    ALL = "all"
    """Special action to represnt all/any of them."""


class ResourceType(str, Enum):
    """Supported resource types."""

    MODEL = "/model"
    """Model and all related artifacts."""

    USER = "/user"
    """User resources."""

    GROUP = "/group"
    """Group resources."""

    @staticmethod
    def get_type_from_url(url: str) -> Optional[ResourceType]:
        """Returns the resource type for the given URL."""
        for resource_type in ResourceType:
            if url.startswith(resource_type.value):
                return resource_type

        # Return none if the URL did not match any known resource type.
        return None


class Group(BaseModel):
    """A user group to which permissions are associated."""

    name: str
    """The name of the group."""

    permissions: List[Permission] = []
    """The permissions associated to the group."""


class Permission(BaseModel):
    """Permissions for manipulating resources."""

    resource_type: ResourceType
    """The type of resource resource."""

    resource_id: Optional[str] = None
    """The specific resource id to give permissions to, if any."""

    method: MethodType = MethodType.ALL
    """The HTTP method applied on the resource."""

    def to_str(self) -> str:
        """Serialize the permission to a string"""
        return f"{self.resource_type.value.replace('/', '')}-{self.resource_id}-{self.method}"

    @staticmethod
    def from_str(permission_str: str) -> Permission:
        """Creates a permission from its string serialization."""
        type, model_id, method = permission_str.split("-")
        return Permission(
            resource_type=ResourceType(f"/{type}"),
            resource_id=model_id,
            method=MethodType(method),
        )


# TODO
#
# 2. Add default permissions/groups for User and Group resources, and maybe general Model resource access
# 3. Add special check for having access to a resource when there is no id, in is_authorized
# 4. Add separate unit tests for admin/user with permissions/user without permissions
#
