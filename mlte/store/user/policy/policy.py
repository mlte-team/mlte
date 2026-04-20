"""Class to define group and permission policies."""

from __future__ import annotations

from typing import Optional, Union

from mlte.user.model import (
    BasicUser,
    Group,
    MethodType,
    Permission,
    ResourceType,
    RoleType,
    UserWithPassword,
)


class Policy:
    # -----------------------------------------------------------------------------
    # Group naming.
    # -----------------------------------------------------------------------------

    CREATE_GROUP_PREFIX = "create"
    EDIT_GROUP_PREFIX = "edit"
    READ_GROUP_PREFIX = "read"

    SEPARATOR = "-"
    SEPARATOR_REPLACEMENT = "___"
    """Used when building group name."""

    @staticmethod
    def _build_group_name(
        prefix: str, resource_type: ResourceType, resource_id: Optional[str]
    ):
        """Builds group ids for the given prefix and resource id."""
        name = f"{prefix}{Policy.SEPARATOR}{resource_type}"
        if resource_id is not None:
            name = f"{name}{Policy.SEPARATOR}{resource_id.replace(Policy.SEPARATOR, Policy.SEPARATOR_REPLACEMENT)}"
        return name

    # -----------------------------------------------------------------------------
    # Policy handling.
    # -----------------------------------------------------------------------------

    def __init__(
        self,
        resource_type: ResourceType,
        resource_id: Optional[str] = None,
        read_group: bool = True,
        edit_group: bool = True,
        create_group: bool = True,
    ):
        """Initializes a policy from a list of groups."""

        self.resource_type = resource_type
        """The resource type for this policy."""

        self.resource_id = resource_id
        """The id of the specific resource this policy is for, if any."""

        self.read_group = read_group
        self.edit_group = edit_group
        self.create_group = create_group
        """Define which types of groups are enabled."""

        self.groups = self._build_groups()
        """A list of groups and their permissions, defining a policy."""

    def _build_groups(self) -> list[Group]:
        """Generates in memory representations of read and write groups for the given resource."""
        groups: list[Group] = []

        # Group with read permissions.
        if self.read_group:
            read_group = Group(
                name=Policy._build_group_name(
                    Policy.READ_GROUP_PREFIX,
                    self.resource_type,
                    self.resource_id,
                ),
                permissions=[
                    Permission(
                        resource_type=self.resource_type,
                        resource_id=self.resource_id,
                        method=MethodType.GET,
                    )
                ],
            )
            groups.append(read_group)

        # Group with create permissions.
        if self.create_group:
            # Create group is only created for non-resource-id related groups, create is always general, never associated to an id.
            if self.resource_id is None:
                create_group = Group(
                    name=Policy._build_group_name(
                        Policy.CREATE_GROUP_PREFIX, self.resource_type, None
                    ),
                    permissions=[
                        Permission(
                            resource_type=self.resource_type,
                            resource_id=self.resource_id,
                            method=MethodType.POST,
                        ),
                    ],
                )
                groups.append(create_group)

        # Group with edit/delete permissions.
        if self.edit_group:
            write_group = Group(
                name=Policy._build_group_name(
                    Policy.EDIT_GROUP_PREFIX,
                    self.resource_type,
                    self.resource_id,
                ),
                permissions=[
                    Permission(
                        resource_type=self.resource_type,
                        resource_id=self.resource_id,
                        method=MethodType.PUT,
                    ),
                    Permission(
                        resource_type=self.resource_type,
                        resource_id=self.resource_id,
                        method=MethodType.DELETE,
                    ),
                ],
            )

            # Creating/editing items inside the major resources will happen with a POST and an id of the major resource.
            if self.resource_id is not None:
                write_group.permissions.append(
                    Permission(
                        resource_type=self.resource_type,
                        resource_id=self.resource_id,
                        method=MethodType.POST,
                    ),
                )

            groups.append(write_group)

        return groups

    def assign_to_user(
        self, user: Union[UserWithPassword, BasicUser]
    ) -> Union[UserWithPassword, BasicUser]:
        """
        Add to this user object the groups from this policy he is not a member of.
        """
        # Groups are not assigned to admin role, which has access to everything.
        if user.role == RoleType.ADMIN:
            return user

        # Only add groups the user does not already belong to.
        for group in self.groups:
            user_already_in_group = False
            for existing_group in user.groups:
                if existing_group.name == group.name:
                    user_already_in_group = True
                    break

            if not user_already_in_group:
                user.groups.append(group)

        return user

    def __str__(self) -> str:
        return f"Resource {self.resource_type}, Id: {self.resource_id}, Read: {self.read_group}, Edit: {self.edit_group}, Create: {self.create_group}, Groups: {self.groups}"
