"""
mlte/store/user/policy.py

Class to define group and permission policies.
"""

from typing import Any, Optional

import mlte.store.error as errors
from mlte.store.artifact.store import ArtifactStoreSession
from mlte.store.user.store_session import UserStoreSession
from mlte.user.model import (
    BasicUser,
    Group,
    MethodType,
    Permission,
    ResourceType,
    RoleType,
)


def create_model_policies_if_needed(artifact_store: ArtifactStoreSession, user_store: UserStoreSession):
    """
    Function that checks, for all models, if policies have not been created.
    This is for cases where the model may have been created without the API.
    """
    models = artifact_store.list_models()
    for model_id in models:
        if not Policy.exists(ResourceType.MODEL, model_id, user_store):
            Policy.create(ResourceType.MODEL, model_id, user_store)


class Policy:
    # -----------------------------------------------------------------------------
    # Group naming.
    # -----------------------------------------------------------------------------

    WRITE_GROUP_PREFIX = "write"
    READ_GROUP_PREFIX = "read"

    @staticmethod
    def _build_read_group_name(resource_type: ResourceType, resource_id: Any):
        """Builds group name for readers."""
        return Policy._build_group_name(
            Policy.READ_GROUP_PREFIX, resource_type, resource_id
        )

    @staticmethod
    def _build_write_group_name(resource_type: ResourceType, resource_id: Any):
        """Builds group name for writers."""
        return Policy._build_group_name(
            Policy.WRITE_GROUP_PREFIX, resource_type, resource_id
        )

    @staticmethod
    def _build_group_name(
        prefix: str, resource_type: ResourceType, resource_id: Any
    ):
        """Builds group ids for the given prefix and resource id."""
        name = f"{prefix}-{resource_type}"
        if resource_id is not None:
            name = f"{name}-{resource_id}"
        return name

    # -----------------------------------------------------------------------------
    # Policy handling.
    # -----------------------------------------------------------------------------

    @staticmethod
    def exists(
        resource_type: ResourceType,
        resource_id: Any,
        user_store: UserStoreSession,
    ) -> bool:
        """Checks if the given resource type and id has permissions associated to it."""
        try:
            # Try to read all permissions.
            for method in MethodType:
                _ = user_store.permission_mapper.read(
                    Permission(
                        resource_type=resource_type,
                        resource_id=resource_id,
                        method=method,
                    ).to_str()
                )

                # Try to read all groups.
                _ = user_store.group_mapper.read(
                    Policy._build_read_group_name(resource_type, resource_id)
                )
                _ = user_store.group_mapper.read(
                    Policy._build_write_group_name(resource_type, resource_id)
                )
        except errors.ErrorNotFound:
            # At least one permission or group is missing.
            return False

        # If we found everything, policy is complete.
        return True

    @staticmethod
    def create(
        resource_type: ResourceType,
        resource_id: Any,
        user_store: UserStoreSession,
        user: Optional[BasicUser] = None,
    ):
        """Sets up groups and permissions for a given resource and user."""

        # Create a permission for each method type and this resource.
        for method in MethodType:
            user_store.permission_mapper.create(
                Permission(
                    resource_type=resource_type,
                    resource_id=resource_id,
                    method=method,
                )
            )

        # Create a group with read permissions.
        read_group = Group(
            name=Policy._build_write_group_name(resource_type, resource_id),
            permissions=[
                Permission(
                    resource_type=resource_type,
                    resource_id=resource_id,
                    method=MethodType.GET,
                )
            ],
        )
        user_store.group_mapper.create(read_group)

        # Create a group with write/delete permissions.
        write_group = Group(
            name=Policy._build_read_group_name(resource_type, resource_id),
            permissions=[
                Permission(
                    resource_type=resource_type,
                    resource_id=resource_id,
                    method=MethodType.POST,
                ),
                Permission(
                    resource_type=resource_type,
                    resource_id=resource_id,
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

    @staticmethod
    def remove(
        resource_type: ResourceType,
        resource_id: Any,
        user_store: UserStoreSession,
    ):
        """Delete groups and permissions for a resource."""

        # TODO: This is not atomic. Error deleting one part may leave the rest dangling.
        user_store.group_mapper.delete(
            Policy._build_read_group_name(resource_type, resource_id)
        )
        user_store.group_mapper.delete(
            Policy._build_write_group_name(resource_type, resource_id)
        )

        for method in MethodType:
            user_store.permission_mapper.delete(
                Permission(
                    resource_type=resource_type,
                    resource_id=resource_id,
                    method=method,
                ).to_str()
            )
