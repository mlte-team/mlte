"""
mlte/store/catalog/underlying/http.py

Implementation of HTTP catalog store group.
"""

from __future__ import annotations

from typing import List, Optional, Tuple

from mlte.backend.core.config import settings
from mlte.catalog.model import CatalogEntry
from mlte.store.base import StoreURI
from mlte.store.catalog.store import (
    CatalogEntryMapper,
    CatalogStore,
    CatalogStoreSession,
)
from mlte.store.common.http_clients import OAuthHttpClient
from mlte.store.common.http_storage import HttpStorage
from mlte.user.model import ResourceType

API_PREFIX = settings.API_PREFIX
"""API URL prefix."""


# -----------------------------------------------------------------------------
# HttpCatalogGroupStore
# -----------------------------------------------------------------------------


class HttpCatalogGroupStore(CatalogStore):
    """
    A HTTP implementation of the MLTE catalog store group. Note that it is slightly
    different than the other implementations, in mapping to a store group through a
    backend, instead of a simple catalog store.
    """

    def __init__(
        self, *, uri: StoreURI, client: Optional[OAuthHttpClient] = None
    ) -> None:
        super().__init__(uri=uri)

        self.storage = HttpStorage(uri=uri, client=client)
        """HTTP storage."""

    def session(self) -> CatalogStoreSession:
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return HttpCatalogGroupStoreSession(
            storage=self.storage, read_only=self.read_only
        )


# -----------------------------------------------------------------------------
# HttpCatalogGroupStoreSession
# -----------------------------------------------------------------------------


class HttpCatalogGroupStoreSession(CatalogStoreSession):
    """An HTTP implementation of the MLTE catalog store session."""

    def __init__(
        self, *, storage: HttpStorage, read_only: bool = False
    ) -> None:
        self.storage = storage
        """Http Storage"""

        self.read_only = read_only
        """Whether this is read only or not."""

        self.entry_mapper = HTTPCatalogGroupEntryMapper(
            url=self.storage.clean_url, client=self.storage.client
        )
        """The mapper to entries CRUD."""

        storage.start_session()

    def close(self):
        # No closing needed.
        pass


# -----------------------------------------------------------------------------
# HTTPCatalogGroupEntryMapper
# -----------------------------------------------------------------------------


class HTTPCatalogGroupEntryMapper(CatalogEntryMapper):
    """HTTP mapper for the catalog group entry resource."""

    COMPOSITE_ID_SEPARATOR = "--"

    def __init__(self, url: str, client: OAuthHttpClient) -> None:
        self.url = url
        """The remote catalog store URL."""

        self.client = client
        """A reference to underlying HTTP client."""

        self.base_url = f"{self.url}{API_PREFIX}/{ResourceType.CATALOG.value}"
        """Base URL used in mapper."""

    def create(self, entry: CatalogEntry) -> CatalogEntry:
        # Entry id contains the remote catalog id as well.
        local_catalog_id, _ = self.split_ids(entry.header.identifier)
        new_entry = self._convert_to_local(entry)

        url = f"{self.base_url}/{local_catalog_id}/entry"
        res = self.client.post(url, json=new_entry.model_dump())
        self.client.raise_for_response(res)

        local_entry = CatalogEntry(**(res.json()))
        return self._convert_to_remote(local_entry)

    def edit(self, entry: CatalogEntry) -> CatalogEntry:
        # Entry id contains the remote catalog id as well.
        local_catalog_id, _ = self.split_ids(entry.header.identifier)
        edited_entry = self._convert_to_local(entry)

        url = f"{self.base_url}/{local_catalog_id}/entry"
        res = self.client.put(url, json=edited_entry.model_dump())
        self.client.raise_for_response(res)

        local_entry = CatalogEntry(**(res.json()))
        return self._convert_to_remote(local_entry)

    def read(self, catalog_and_entry_id: str) -> CatalogEntry:
        catalog_id, entry_id = self.split_ids(catalog_and_entry_id)
        url = f"{self.base_url}/{catalog_id}/entry/{entry_id}"
        res = self.client.get(url)
        self.client.raise_for_response(res)

        local_entry = CatalogEntry(**(res.json()))
        return self._convert_to_remote(local_entry)

    def list(self) -> List[str]:
        entries = self.list_details()
        return [entry.header.identifier for entry in entries]

    def delete(self, catalog_and_entry_id: str) -> CatalogEntry:
        local_catalog_id, entry_id = self.split_ids(catalog_and_entry_id)

        url = f"{self.base_url}/{local_catalog_id}/entry/{entry_id}"
        res = self.client.delete(url)
        self.client.raise_for_response(res)

        local_entry = CatalogEntry(**(res.json()))
        return self._convert_to_remote(local_entry)

    def list_details(
        self,
        limit: int = CatalogEntryMapper.DEFAULT_LIST_LIMIT,
        offset: int = 0,
    ) -> List[CatalogEntry]:
        url = f"{self.base_url}s/entry"
        res = self.client.get(url)
        self.client.raise_for_response(res)

        return [
            self._convert_to_remote(CatalogEntry(**entry))
            for entry in res.json()
        ][offset : offset + limit]

    @staticmethod
    def split_ids(composite_id: Optional[str]) -> Tuple[str, str]:
        if not composite_id:
            raise RuntimeError("No composite id received")

        parts = composite_id.split(
            HTTPCatalogGroupEntryMapper.COMPOSITE_ID_SEPARATOR
        )
        if len(parts) != 2:
            raise RuntimeError(f"Invalid composite id provided: {composite_id}")
        return parts[0], parts[1]

    @staticmethod
    def generate_composite_id(id1: Optional[str], id2: str) -> str:
        """Creates a composite id given two ids."""
        if id1:
            return f"{id1}{HTTPCatalogGroupEntryMapper.COMPOSITE_ID_SEPARATOR}{id2}"
        else:
            return id2

    def _convert_to_local(self, entry: CatalogEntry) -> CatalogEntry:
        """Creates a new entry from the given one, converting it to local by moving the remote catalog id from its identifier."""
        new_entry = entry.model_copy()
        new_entry.header = entry.header.model_copy()

        local_catalog_id, entry_id = self.split_ids(entry.header.identifier)
        http_catalog_id = new_entry.header.catalog_id
        new_entry.header.identifier = entry_id
        new_entry.header.catalog_id = self.generate_composite_id(
            http_catalog_id, local_catalog_id
        )

        return new_entry

    def _convert_to_remote(self, entry: CatalogEntry) -> CatalogEntry:
        """Creates a new entry from the given one, convertint it to remote by moving the remote catalog id to its identifier."""
        new_entry = entry.model_copy()
        new_entry.header = entry.header.model_copy()

        http_catalog_id, local_catalog_id = self.split_ids(
            new_entry.header.catalog_id
        )
        entry_id = new_entry.header.identifier
        new_entry.header.identifier = self.generate_composite_id(
            local_catalog_id, entry_id
        )
        new_entry.header.catalog_id = http_catalog_id

        return new_entry
