"""
mlte/backend/api/auth/policy.py

Functions to define group and permission policies.
"""

from typing import Optional

import mlte.store.error as errors
from mlte.backend.api import dependencies
from mlte.context.model import Model
from mlte.user.model import (
    BasicUser,
    Group,
    MethodType,
    Permission,
    ResourceType,
    RoleType,
)

# -----------------------------------------------------------------------------
# Group naming.
# -----------------------------------------------------------------------------


WRITE_GROUP_PREFIX = "write-"
READ_GROUP_PREFIX = "read-"


def _build_read_group_name(model: Model):
    """Builds group name for readers."""
    return _build_group_name(READ_GROUP_PREFIX, model)


def _build_write_group_name(model: Model):
    """Builds group name for writers."""
    return _build_group_name(WRITE_GROUP_PREFIX, model)


def _build_group_name(prefix: str, model: Model):
    """Builds group ids for the given prefix and model."""
    return f"{prefix}{model.identifier}"


# -----------------------------------------------------------------------------
# Policy handling.
# -----------------------------------------------------------------------------


def model_has_policy(model: Model) -> bool:
    """Checks if the given model has permissions associated to it."""
    with dependencies.user_store_session() as user_store:
        try:
            # Try to read all permissions.
            for method in MethodType:
                _ = user_store.permission_mapper.read(
                    Permission(
                        resource_type=ResourceType.MODEL,
                        resource_id=model.identifier,
                        method=method,
                    ).to_str()
                )

            # Try to read all groups.
            _ = user_store.group_mapper.read(_build_read_group_name(model))
            _ = user_store.group_mapper.read(_build_write_group_name(model))
        except errors.ErrorNotFound:
            # At least one permission or group is missing.
            return False

    # If we found everything, policy is complete.
    return True


def define_policy_for_model(model: Model, user: Optional[BasicUser] = None):
    """Sets up groups and permissions for a given model and user."""

    with dependencies.user_store_session() as user_store:
        # Create a permission for each method type and this model.
        for method in MethodType:
            user_store.permission_mapper.create(
                Permission(
                    resource_type=ResourceType.MODEL,
                    resource_id=model.identifier,
                    method=method,
                )
            )

        # Create a group with read permissions.
        read_group = Group(
            name=_build_write_group_name(model),
            permissions=[
                Permission(
                    resource_type=ResourceType.MODEL,
                    resource_id=model.identifier,
                    method=MethodType.GET,
                )
            ],
        )
        user_store.group_mapper.create(read_group)

        # Create a group with write/delete permissions.
        write_group = Group(
            name=_build_read_group_name(model),
            permissions=[
                Permission(
                    resource_type=ResourceType.MODEL,
                    resource_id=model.identifier,
                    method=MethodType.POST,
                ),
                Permission(
                    resource_type=ResourceType.MODEL,
                    resource_id=model.identifier,
                    method=MethodType.DELETE,
                ),
            ],
        )
        user_store.group_mapper.create(write_group)

        # Add current user, if any, to both groups.
        if user and not user.role == RoleType.ADMIN:
            user.groups.append(read_group)
            user.groups.append(write_group)
            user_store.user_mapper.edit(user)


def remove_policy_for_model(deleted_model: Model):
    """Delete groups and permissions for a model"""

    # TODO: This is not atomic. Error deleting one part may leave the rest dangling.
    with dependencies.user_store_session() as user_store:
        user_store.group_mapper.delete(f"read-{deleted_model.identifier}")
        user_store.group_mapper.delete(f"write-{deleted_model.identifier}")

        for method in MethodType:
            user_store.permission_mapper.delete(
                Permission(
                    resource_type=ResourceType.MODEL,
                    resource_id=deleted_model.identifier,
                    method=method,
                ).to_str()
            )
