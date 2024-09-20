"""
mlte/store/user/policy.py

Class to define group and permission policies.
"""

from typing import Any, List, Optional

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


def create_model_policies_if_needed(
    artifact_store: ArtifactStoreSession, user_store: UserStoreSession
):
    """
    Function that checks, for all models, if policies have not been created.
    This is for cases where the model may have been created without the API.
    """
    models = artifact_store.list_models()
    for model_id in models:
        if not Policy.is_stored(ResourceType.MODEL, model_id, user_store):
            Policy.create(ResourceType.MODEL, model_id, user_store)


class Policy:
    # -----------------------------------------------------------------------------
    # Group naming.
    # -----------------------------------------------------------------------------

    CREATE_GROUP_PREFIX = "create"
    EDIT_GROUP_PREFIX = "edit"
    READ_GROUP_PREFIX = "read"

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
    def build_groups(
        resource_type: ResourceType,
        resource_id: Any = None,
        build_read_group: bool = True,
        build_edit_group: bool = True,
        build_create_group: bool = True,
    ) -> List[Group]:
        """Generates in memory representations of read and write groups for the given resource."""
        groups: List[Group] = []

        # Group with read permissions.
        if build_read_group:
            read_group = Group(
                name=Policy._build_group_name(
                    Policy.READ_GROUP_PREFIX, resource_type, resource_id
                ),
                permissions=[
                    Permission(
                        resource_type=resource_type,
                        resource_id=resource_id,
                        method=MethodType.GET,
                    )
                ],
            )
            groups.append(read_group)

        # Group with create permissions.
        if build_create_group:
            # Create group is only created for non-resource-id related groups, create is always general, never associated to an id.
            if resource_id is None:
                create_group = Group(
                    name=Policy._build_group_name(
                        Policy.CREATE_GROUP_PREFIX, resource_type, None
                    ),
                    permissions=[
                        Permission(
                            resource_type=resource_type,
                            resource_id=resource_id,
                            method=MethodType.POST,
                        ),
                    ],
                )
                groups.append(create_group)

        # Group with edit/delete permissions.
        if build_edit_group:
            write_group = Group(
                name=Policy._build_group_name(
                    Policy.EDIT_GROUP_PREFIX, resource_type, resource_id
                ),
                permissions=[
                    Permission(
                        resource_type=resource_type,
                        resource_id=resource_id,
                        method=MethodType.PUT,
                    ),
                    Permission(
                        resource_type=resource_type,
                        resource_id=resource_id,
                        method=MethodType.DELETE,
                    ),
                ],
            )

            # Creating/editing items inside the major resources will happen with a POST and an id of the major resource.
            if resource_id is not None:
                write_group.permissions.append(
                    Permission(
                        resource_type=resource_type,
                        resource_id=resource_id,
                        method=MethodType.POST,
                    ),
                )

            groups.append(write_group)

        return groups

    @staticmethod
    def is_stored(
        resource_type: ResourceType,
        resource_id: Any,
        user_store: UserStoreSession,
    ) -> bool:
        """Checks if the given resource type and id has a policy stored in the DB for them."""
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
                for group in Policy.build_groups(resource_type, resource_id):
                    _ = user_store.group_mapper.read(group.name)
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
        """Sets up groups and permissions for a given resource type and id."""

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
        policy_groups = Policy.build_groups(resource_type, resource_id)
        for group in policy_groups:
            user_store.group_mapper.create(group)

        # Add current user, if any, to all groups.
        if user and not user.role == RoleType.ADMIN:
            for group in policy_groups:
                user.groups.append(group)
            user_store.user_mapper.edit(user)

    @staticmethod
    def remove(
        resource_type: ResourceType,
        resource_id: Any,
        user_store: UserStoreSession,
    ):
        """Delete groups and permissions for a resource."""

        # TODO: This is not atomic. Error deleting one part may leave the rest dangling.
        for group in Policy.build_groups(resource_type, resource_id):
            user_store.group_mapper.delete(group.name)

        for method in MethodType:
            user_store.permission_mapper.delete(
                Permission(
                    resource_type=resource_type,
                    resource_id=resource_id,
                    method=method,
                ).to_str()
            )
