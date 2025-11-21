"""Manages current session info about stores."""

from typing import Optional

from mlte.store.artifact import factory as artifact_store_factory
from mlte.store.artifact.store import ArtifactStore
from mlte.store.base import StoreType, StoreURI
from mlte.store.catalog.catalog_group import CatalogStoreGroup
from mlte.store.catalog.sample_catalog import SampleCatalog
from mlte.store.catalog.store import CatalogStore
from mlte.store.custom_list.initial_custom_lists import InitialCustomLists
from mlte.store.custom_list.store import CustomListStore
from mlte.store.user import factory as user_store_factory
from mlte.store.user.store import UserStore
from mlte.store.validators.composite_validator import CompositeValidator
from mlte.store.validators.validators import (
    ArtifactCustomListValidator,
    ArtifactUserValidator,
    CatalogCustomListValidator,
    CatalogUserValidator,
)


class SessionStores:
    """
    Contains the store sessions currently being used.
    """

    LOCAL_CATALOG_STORE_ID = "local"
    """Name of the default catalog store."""

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
        if not self._artifact_store:
            raise RuntimeError("Store was not properly set up.")
        return self._artifact_store

    @property
    def custom_list_store(self) -> CustomListStore:
        """Get the session custom list store."""
        if not self._custom_list_store:
            raise RuntimeError("Store was not properly set up.")
        return self._custom_list_store

    @property
    def user_store(self) -> UserStore:
        """Get session user store."""
        if not self._user_store:
            raise RuntimeError("Store was not properly set up.")
        return self._user_store

    @property
    def catalog_stores(self) -> CatalogStoreGroup:
        """Get all catalog stores."""
        return self._catalog_stores


def setup_stores(
    stores_uri: str,
    catalog_uris: dict[str, str] = {},
) -> SessionStores:
    """
    Sets up all stores required by MLTE, from the provided URIs.

    :param stores_uri: The store URI string, used as the common type and root location for all non-catalog stores.
    :param catalog_uris: A dict of URIs for catalog stores.
    """
    stores = SessionStores()

    # Initialize the backing artifact store instance.
    artifact_store = artifact_store_factory.create_artifact_store(stores_uri)
    stores.set_artifact_store(artifact_store)

    # Initialize the backing user store instance.
    user_store = user_store_factory.create_user_store(stores_uri)
    stores.set_user_store(user_store)

    # Initialize the backing custom list store instance.
    custom_list_store = InitialCustomLists.setup_custom_list_store(stores_uri)
    stores.set_custom_list_store(custom_list_store)

    # Setup catalog store validators
    catalog_store_validators = CompositeValidator(
        [
            CatalogUserValidator(user_store=stores.user_store),
            CatalogCustomListValidator(
                custom_list_store=stores.custom_list_store
            ),
        ]
    )

    # Catalogs: first add the sample catalog store.
    sample_catalog = SampleCatalog.setup_sample_catalog(
        stores_uri, catalog_store_validators
    )
    stores.add_catalog_store(
        store=sample_catalog, id=SampleCatalog.SAMPLE_CATALOG_ID
    )

    # Throw error if trying to set a remote catalog with the id of the local catalog
    if SessionStores.LOCAL_CATALOG_STORE_ID in catalog_uris:
        raise RuntimeError(
            f"Remote catalog store ID cannot be {SessionStores.LOCAL_CATALOG_STORE_ID}. This is the local catalog store ID."
        )

    # Create local catalog
    stores.add_catalog_store_from_uri(
        stores_uri, SessionStores.LOCAL_CATALOG_STORE_ID
    )

    # Catalogs: Add all configured catalog stores.
    for id, uri in catalog_uris.items():
        stores.add_catalog_store_from_uri(uri, id)

    # Setup artifact store validators
    artifact_store_validators = CompositeValidator(
        [
            ArtifactUserValidator(user_store=stores.user_store),
            ArtifactCustomListValidator(
                custom_list_store=stores.custom_list_store
            ),
        ]
    )
    stores.artifact_store.set_validators(artifact_store_validators)

    # Add catalog store validators to stores
    for uri, catalog_store in stores.catalog_stores.catalogs.items():
        if uri == SessionStores.LOCAL_CATALOG_STORE_ID:
            catalog_store.set_validators(catalog_store_validators)
        # It is added to the sample catalog when it is setup initially
        elif (
            uri != SampleCatalog.SAMPLE_CATALOG_ID
            and StoreURI.from_string(uri).type != StoreType.REMOTE_HTTP
        ):
            catalog_store.set_validators(catalog_store_validators)

    return stores
