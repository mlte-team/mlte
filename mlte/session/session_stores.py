"""Manages current session info about stores."""

import os
from typing import Optional

from mlte.store.artifact.factory import create_artifact_store
from mlte.store.artifact.store import ArtifactStore
from mlte.store.catalog.catalog_group import CatalogStoreGroup
from mlte.store.catalog.store import CatalogStore
from mlte.store.custom_list.initial_custom_lists import InitialCustomLists
from mlte.store.custom_list.store import CustomListStore
from mlte.store.user.factory import create_user_store
from mlte.store.user.store import UserStore


class SessionStores:
    """
    Contains the store sessions currently being used.
    """

    ENV_ARTIFACT_STORE_URI_VAR = "MLTE_ARTIFACT_STORE_URI"
    """Environment variable to get the artifact store URI from, if needed."""

    ENV_CUSTOM_LIST_STORE_URI_VAR = "MLTE_CUSTOM_LIST_STORE_URI"
    """Environment variable to get the custom list store URI from, if needed."""

    ENV_USER_STORE_URI_VAR = "MLTE_CUSTOM_LIST_STORE_URI"
    """Environment variable to get the custom list store URI from, if needed."""

    def __init__(self):
        """Defines the existing stores, none loaded yet."""

        self._artifact_store: Optional[ArtifactStore] = None
        """The MLTE artifact store instance for the session."""

        self._custom_list_store: Optional[CustomListStore] = None
        """The MLTE custom list store instance for the session."""

        self._user_store: Optional[UserStore] = None
        """The user store instance for the session."""

        self._catalog_stores: CatalogStoreGroup = CatalogStoreGroup()
        """The list of catalog store instances maintained by the session object."""

    def set_artifact_store(self, store: ArtifactStore) -> None:
        """Set the globally-configured backend artifact store."""
        self._artifact_store = store

    def set_custom_list_store(self, store: CustomListStore) -> None:
        """Set the globally-configured backend custom list store."""
        self._custom_list_store = store

    def set_user_store(self, store: UserStore) -> None:
        """Set the globally-configured backend user store."""
        self._user_store = store

    def add_catalog_store(
        self, store: CatalogStore, id: str, overwite: bool = False
    ) -> None:
        """Adds to the the globally-configured backend list of catalog stores."""
        self._catalog_stores.add_catalog(id, store, overwite)

    def add_catalog_store_from_uri(
        self, store_uri: str, id: str, overwite: bool = False
    ) -> None:
        """Adds to the the globally-configured backend list of catalog stores."""
        self._catalog_stores.add_catalog_from_uri(id, store_uri, overwite)

    @property
    def artifact_store(self) -> ArtifactStore:
        """Get the session artifact store."""
        if self._artifact_store is None:
            # If the URI has not been manually set, get it from environment.
            store_uri = self._get_env_var(self.ENV_ARTIFACT_STORE_URI_VAR)
            if store_uri:
                self._artifact_store = create_artifact_store(store_uri)
            else:
                raise RuntimeError(
                    "Must initialize artifact store, either manually or through environment variables."
                )
        return self._artifact_store

    @property
    def custom_list_store(self) -> CustomListStore:
        """Get the session custom list store."""
        if self._custom_list_store is None:
            # If the store URI has not been manually set, get it from environment.
            store_uri = self._get_env_var(self.ENV_CUSTOM_LIST_STORE_URI_VAR)
            if store_uri:
                self._custom_list_store = (
                    InitialCustomLists.setup_custom_list_store(store_uri)
                )
            else:
                raise RuntimeError(
                    "Must initialize custom list store, either manually or through environment variables."
                )
        return self._custom_list_store

    @property
    def user_store(self) -> UserStore:
        """Get session user store."""
        if self._user_store is None:
            # If the store URI has not been manually set, get it from environment.
            store_uri = self._get_env_var(self.ENV_USER_STORE_URI_VAR)
            if store_uri:
                self._user_store = create_user_store(store_uri)
            else:
                raise RuntimeError(
                    "Must initialize user store, either manually or through environment variables."
                )
        return self._user_store

    @property
    def catalog_stores(self) -> CatalogStoreGroup:
        """Get all catalog stores."""
        return self._catalog_stores

    def _get_env_var(self, env_var: str) -> Optional[str]:
        """Get env var or return none if does not exist."""
        return os.environ.get(env_var, None)
