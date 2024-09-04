"""
mlte/store/catalog/underlying/http.py

Implementation of HTTP catalog store group.
"""

from __future__ import annotations

from typing import List, Tuple

from mlte.backend.core.config import settings
from mlte.catalog.model import CatalogEntry
from mlte.store.base import StoreURI
from mlte.store.catalog.store import (
    CatalogEntryMapper,
    CatalogStore,
    CatalogStoreSession,
)
from mlte.store.common.http_clients import OAuthHttpClient, RequestsClient
from mlte.store.common.http_store import HttpStorage
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
        self, *, uri: StoreURI, client: OAuthHttpClient = RequestsClient()
    ) -> None:
        super().__init__(uri=uri)

        self.storage = HttpStorage(uri=uri, client=client)
        """HTTP storage."""

    def session(self) -> CatalogStoreSession:
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return HttpCatalogGroupStoreSession(storage=self.storage)


# -----------------------------------------------------------------------------
# HttpCatalogGroupStoreSession
# -----------------------------------------------------------------------------


class HttpCatalogGroupStoreSession(CatalogStoreSession):
    """An HTTP implementation of the MLTE catalog store session."""

    def __init__(self, *, storage: HttpStorage) -> None:
        self.storage = storage
        """Http Storage"""

        self.entry_mapper = HTTPCatalogGroupEntryMapper(
            url=self.storage.url, client=self.storage.client
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

    CATALOG_ENTRY_ID_SEPARATOR = "--"

    def __init__(self, url: str, client: OAuthHttpClient) -> None:
        self.url = url
        """The remote catalog store URL."""

        self.client = client
        """A reference to underlying HTTP client."""

        self.base_url = f"{self.url}/{ResourceType.CATALOG_ENTRY.value}"
        """Base URL used in mapper."""

    def create(self, entry: CatalogEntry) -> CatalogEntry:
        # Entry id contains the remote catalog id as well.
        catalog_id, entry_id = self._split_ids(entry.header.identifier)
        entry.header.identifier = entry_id

        url = f"{self.base_url}/{catalog_id}/entry"
        res = self.client.post(url, json=entry.model_dump())
        self.client.raise_for_response(res)

        return CatalogEntry(**(res.json()))

    def edit(self, entry: CatalogEntry) -> CatalogEntry:
        # Entry id contains the remote catalog id as well.
        catalog_id, entry_id = self._split_ids(entry.header.identifier)
        entry.header.identifier = entry_id

        url = f"{self.base_url}/{catalog_id}/entry"
        res = self.client.put(url, json=entry.model_dump())
        self.client.raise_for_response(res)

        return CatalogEntry(**(res.json()))

    def read(self, catalog_and_entry_id: str) -> CatalogEntry:
        catalog_id, entry_id = self._split_ids(catalog_and_entry_id)
        url = f"{self.base_url}/{catalog_id}/entry/{entry_id}"
        res = self.client.get(url)
        self.client.raise_for_response(res)

        return CatalogEntry(**(res.json()))

    def list(self) -> List[str]:
        entries = self.list_details()
        return [entry.header.identifier for entry in entries]

    def delete(self, catalog_and_entry_id: str) -> CatalogEntry:
        catalog_id, entry_id = self._split_ids(catalog_and_entry_id)
        url = f"{self.base_url}/{catalog_id}/entry/{entry_id}"
        res = self.client.delete(url)
        self.client.raise_for_response(res)

        return CatalogEntry(**(res.json()))

    def list_details(
        self,
        limit: int = CatalogEntryMapper.DEFAULT_LIST_LIMIT,
        offset: int = 0,
    ) -> List[CatalogEntry]:
        url = f"{self.base_url}s/entry"
        res = self.client.get(url)
        self.client.raise_for_response(res)

        return [CatalogEntry(**entry) for entry in res.json()][
            offset : offset + limit
        ]

    def _split_ids(self, catalog_and_entry_id: str) -> Tuple[str, str]:
        parts = catalog_and_entry_id.split(
            HTTPCatalogGroupEntryMapper.CATALOG_ENTRY_ID_SEPARATOR
        )
        if len(parts) != 2:
            raise RuntimeError(
                f"Invalid catalog and entry id provided: {catalog_and_entry_id}"
            )
        return parts[0], parts[1]
