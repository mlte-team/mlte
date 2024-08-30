"""
mlte/store/catalog/underlying/http.py

Implementation of HTTP catalog store.
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
from mlte.user.model import ResourceType

API_PREFIX = settings.API_PREFIX
"""API URL prefix."""


# -----------------------------------------------------------------------------
# HttpCatalogGroupStore
# -----------------------------------------------------------------------------


class HttpCatalogGroupStore(CatalogStore):
    """A HTTP implementation of the MLTE catalog store."""

    def __init__(
        self,
        uri: StoreURI,
        client: OAuthHttpClient = RequestsClient(),
    ) -> None:
        self.client = client
        """The client for requests."""

        # Get credentials, if any, from the uri and into the client.
        uri.uri = self.client.process_credentials(uri.uri)
        super().__init__(uri=uri)

    def session(self) -> HttpCatalogGroupStoreSession:  # type: ignore[override]
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return HttpCatalogGroupStoreSession(
            url=self.uri.uri, client=self.client
        )


# -----------------------------------------------------------------------------
# HttpCatalogGroupStoreSession
# -----------------------------------------------------------------------------


class HttpCatalogGroupStoreSession(CatalogStoreSession):
    """An HTTP implementation of the MLTE catalog store session."""

    def __init__(self, *, url: str, client: OAuthHttpClient) -> None:
        self.url = url
        """The remote catalog store URL."""

        self.client = client
        """The client for HTTP requests."""

        self.entry_mapper = HTTPCatalogGroupEntryMapper(
            url=self.url, client=self.client
        )
        """The mapper to entries CRUD."""

        # Authenticate.
        self.client.authenticate(
            f"{self.url}{API_PREFIX}",
        )

    def close(self) -> None:
        """Close the session."""
        # Closing a remote HTTP session is a no-op.
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
