"""
mlte/store/catalog/sample_catalog.py

MLTE sample catalog to come with installation.
"""

from __future__ import annotations

import importlib.resources
import json
import os
from typing import Optional

import mlte.store.catalog.sample as sample_entries
from mlte.catalog.model import CatalogEntry
from mlte.store.base import StoreType, StoreURI
from mlte.store.catalog.factory import create_catalog_store
from mlte.store.catalog.store import (
    CatalogStore,
    CatalogStoreSession,
    ManagedCatalogSession,
)


class SampleCatalog:
    """A catalog with sample code. This class is used to set that catalog up when needed."""

    SAMPLE_CATALOG_ID = "sample"
    """Id for sample catalog."""

    DEFAULT_STORES_FOLDER = "stores"
    """Default root folder for all built-in stores."""

    @staticmethod
    def setup_sample_catalog(
        stores_uri: Optional[StoreURI] = None,
    ) -> CatalogStore:
        """
        Sets up the sample catalog.

        :param stores_uri: The URI of the stores being used (i.e., base folder, base DB, etc).
        :return: The sample catalog store.
        """
        # Set file system URI if we didn't get one, or if we got a non-file system one.
        if stores_uri is None or (
            stores_uri is not None
            and stores_uri.type != StoreType.LOCAL_FILESYSTEM
        ):
            # We will always create the sample catalog store as a file system store, regardless of where the other
            # stores of the system are.
            stores_uri = StoreURI.from_string(
                f"{StoreURI.get_default_prefix(StoreType.LOCAL_FILESYSTEM)}{SampleCatalog.DEFAULT_STORES_FOLDER}"
            )

        # The base stores folder has to exist, so create it if it doesn't.
        os.makedirs(f"./{stores_uri.path}", exist_ok=True)

        # Create the actual sample catalog.
        print(f"Creating sample catalog at URI: {stores_uri}")
        catalog = create_catalog_store(
            stores_uri.uri, SampleCatalog.SAMPLE_CATALOG_ID
        )

        # Ensure the catalog is always reset to its initial state, and mark it as read only.
        SampleCatalog.reset_catalog(catalog)
        catalog.read_only = True

        return catalog

    @staticmethod
    def reset_catalog(catalog_store: CatalogStore) -> None:
        """Ensures the sample catalog is reset to default values."""
        with ManagedCatalogSession(catalog_store.session()) as store:
            # First remove all existing entries.
            entry_ids = store.entry_mapper.list()
            for entry_id in entry_ids:
                store.entry_mapper.delete(entry_id)

            # Now populate it again with the default values.
            SampleCatalog._populate_catalog(store)

    @staticmethod
    def _populate_catalog(catalog_session: CatalogStoreSession) -> None:
        """Load all entry files from entry folder and put them into sample catalog."""
        num_entries = 0
        resources = importlib.resources.files(sample_entries)
        with importlib.resources.as_file(resources) as resources_path:
            with os.scandir(resources_path) as files:
                print("Loading sample catalog entries.")
                for file in files:
                    if file.is_file() and file.name.endswith("json"):
                        with open(file.path) as open_file:
                            entry = CatalogEntry(**json.load(open_file))
                            entry.header.catalog_id = (
                                SampleCatalog.SAMPLE_CATALOG_ID
                            )
                            catalog_session.entry_mapper.create(entry)
                            num_entries += 1
                print(f"Loaded {num_entries} entries for sample catalog.")
