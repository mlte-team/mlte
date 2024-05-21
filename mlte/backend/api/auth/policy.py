"""
mlte/backend/api/auth/policy.py

Functions to define group and permission policies.
"""

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


def define_policy_for_model(model: Model, user: BasicUser):
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
            name=f"read-{model.identifier}",
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
            name=f"write-{model.identifier}",
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

        # Add current user to both groups.
        if not user.role == RoleType.ADMIN:
            user.groups.append(read_group)
            user.groups.append(write_group)
            user_store.user_mapper.edit(user)


def remove_policy_for_model(deleted_model: Model):
    """Delete groups and permissions for a model"""

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
