"""
mlte/store/catalog/underlying/http.py

Implementation of HTTP catalog store.
"""

from __future__ import annotations

from typing import List

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
# HttpCatalogStore
# -----------------------------------------------------------------------------


class HttpCatalogStore(CatalogStore):
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

    def session(self) -> HttpCatalogStoreSession:  # type: ignore[override]
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return HttpCatalogStoreSession(url=self.uri.uri, client=self.client)


# -----------------------------------------------------------------------------
# HttpCatalogStoreSession
# -----------------------------------------------------------------------------


class HttpCatalogStoreSession(CatalogStoreSession):
    """An HTTP implementation of the MLTE catalog store session."""

    def __init__(self, *, url: str, client: OAuthHttpClient) -> None:
        self.url = url
        """The remote catalog store URL."""

        self.client = client
        """The client for HTTP requests."""

        self.entry_mapper = HTTPCatalogEntryMapper(
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
# HTTPCatalogEntryMapper
# -----------------------------------------------------------------------------


class HTTPCatalogEntryMapper(CatalogEntryMapper):
    """HTTP mapper for the catalog entry resource."""

    def __init__(self, url: str, client: OAuthHttpClient) -> None:
        self.url = url
        """The remote catalog store URL."""

        self.client = client
        """A reference to underlying HTTP client."""

        self.base_url = f"{self.url}/{ResourceType.CATALOG_ENTRY.value}"
        """Base URL used in mapper."""

    def create2(self, entry: CatalogEntry) -> CatalogEntry:
        url = f"{self.base_url}/{entry.header.catalog_id}/entry"
        res = self.client.post(url, json=entry.model_dump())
        self.client.raise_for_response(res)

        return CatalogEntry(**(res.json()))

    def edit2(self, entry: CatalogEntry) -> CatalogEntry:
        url = f"{self.base_url}/{entry.header.catalog_id}/entry"
        res = self.client.put(url, json=entry.model_dump())
        self.client.raise_for_response(res)

        return CatalogEntry(**(res.json()))

    def read2(self, entry_id: str, catalog_id: str) -> CatalogEntry:
        url = f"{self.base_url}/{catalog_id}/entry/{entry_id}"
        res = self.client.get(url)
        self.client.raise_for_response(res)

        return CatalogEntry(**(res.json()))

    def list2(self, catalog_id: str) -> List[str]:
        entries = self.list_details2(catalog_id)
        return [entry.header.identifier for entry in entries]

    def delete2(self, entry_id: str, catalog_id: str) -> CatalogEntry:
        url = f"{self.base_url}/{catalog_id}/entry/{entry_id}"
        res = self.client.delete(url)
        self.client.raise_for_response(res)

        return CatalogEntry(**(res.json()))

    def list_details2(
        self,
        catalog_id: str,
        limit: int = CatalogEntryMapper.DEFAULT_LIST_LIMIT,
        offset: int = 0,
    ) -> List[CatalogEntry]:
        url = f"{self.base_url}/{catalog_id}/entry"
        res = self.client.get(url)
        self.client.raise_for_response(res)

        return [CatalogEntry(**entry) for entry in res.json()][
            offset : offset + limit
        ]
