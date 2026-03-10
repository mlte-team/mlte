"""Class to store group and permission policies."""

from __future__ import annotations

import mlte.store.error as errors
from mlte.store.user.policy import Policy
from mlte.store.user.store_session import GroupMapper, PermissionMapper


class PolicyStore:
    """Handles access to stored policies. It is not a store in the same sense as the rest, does not derive from Store."""

    def __init__(
        self, group_mapper: GroupMapper, permission_mapper: PermissionMapper
    ):
        """Sets up the group and permissions mapper to be used."""
        self.group_mapper = group_mapper
        self.permission_mapper = permission_mapper

    def is_stored(self, policy: Policy) -> bool:
        """
        Checks if this policy is stored in the given mappers.

        :param policy: The policy to be checked.
        """
        try:
            # Try to read all groups and permissions.
            for group in policy.groups:
                _ = self.group_mapper.read(group.name)

                for permission in group.permissions:
                    _ = self.permission_mapper.read(permission.to_str())
        except errors.ErrorNotFound:
            # At least one permission or group is missing.
            return False

        # If we found everything, policy is complete.
        return True

    def save_to_store(self, policy: Policy) -> None:
        """
        Store this policy's groups and permissions in the given store.

        :param policy: The policy to be stored.
        """
        # Create groups and permissions in store.
        for group in policy.groups:
            for permission in group.permissions:
                self.permission_mapper.create(permission)

            self.group_mapper.create(group)

    def remove_from_store(self, policy: Policy) -> None:
        """Delete groups and permissions for a resource."""
        # TODO: This is not atomic. Error deleting one part may leave the rest dangling.
        permissions: dict[str, bool] = {}
        for group in policy.groups:
            for permission in group.permissions:
                # Store permissions in dict for later removal, to avoid trying to re-remove already deleted ones.
                permissions[permission.to_str()] = True

            self.group_mapper.delete(group.name)

        # Now remove all permissions.
        # TODO: note that this main leave other groups using these permissions dangling. Not trivial to check if
        # a permission is no longer used. Even worse, we may want to leave some of them, even with no groups.
        for permission_str in permissions:
            self.permission_mapper.delete(permission_str)
