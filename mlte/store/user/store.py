"""
mlte/store/user/store.py

MLTE user store interface implementation.
"""

from __future__ import annotations

from mlte.store import error
from mlte.store.base import Store, StoreURI
from mlte.store.user.policy import Policy
from mlte.store.user.store_session import ManagedUserSession, UserStoreSession
from mlte.user.model import ResourceType, RoleType, UserCreate

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

    def __init__(self, uri: StoreURI):
        """Base constructor."""
        super().__init__(uri=uri)

        # Sets up default user and permissions.
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
                UserCreate(
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
        with ManagedUserSession(self.session()) as user_store:
            for resource_type in ResourceType:
                if not Policy.exists(
                    resource_type, resource_id=None, user_store=user_store
                ):
                    Policy.create(
                        resource_type, resource_id=None, user_store=user_store
                    )
