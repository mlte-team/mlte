"""
mlte/store/user/store.py

MLTE user store interface implementation.
"""

from __future__ import annotations

from mlte.store import error
from mlte.store.base import Store, StoreURI
from mlte.store.user.policy import Policy
from mlte.store.user.store_session import UserStoreSession
from mlte.user.model import ResourceType, RoleType, UserWithPassword

DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "admin1234"
"""Default user for setup."""


# -----------------------------------------------------------------------------
# UserStore
# -----------------------------------------------------------------------------


class UserStore(Store):
    """
    An abstract user store.
    """

    ID_MAP: dict[str, str] = {
        ResourceType.USER: "username",
        ResourceType.MODEL: "identifier",
        ResourceType.GROUP: "name",
    }
    """Map of ids used for each resource."""

    def __init__(self, uri: StoreURI, add_default_data: bool = True):
        """Base constructor."""
        super().__init__(uri=uri)
        "Store uri."

        # Sets up default user and permissions.
        if add_default_data:
            self._init_default_user()
            self._init_default_permissions()

    def session(self) -> UserStoreSession:
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        raise NotImplementedError("Cannot get handle to abstract Store.")

    def _init_default_user(self):
        """Adds the default user."""
        try:
            self.session().user_mapper.create(
                UserWithPassword(
                    username=DEFAULT_USERNAME,
                    password=DEFAULT_PASSWORD,
                    role=RoleType.ADMIN,
                )
            )
        except error.ErrorAlreadyExists:
            # If default user was already there, ignore warning, we don't want to overrwite any changes on it.
            pass

    def _init_default_permissions(self):
        """Create all default permissions."""
        user_store = self.session()
        for resource_type in ResourceType:
            if not Policy.is_stored(
                resource_type, resource_id=None, user_store=user_store
            ):
                Policy.create(
                    resource_type, resource_id=None, user_store=user_store
                )
