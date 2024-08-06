"""
mlte/store/catalog/underlying/http.py

Implementation of HTTP catalog store.
"""

from __future__ import annotations

from mlte.backend.core.config import settings
from mlte.store.base import StoreURI
from mlte.store.catalog.store import CatalogStore, CatalogStoreSession
from mlte.store.common.http_clients import OAuthHttpClient, RequestsClient

API_PREFIX = settings.API_PREFIX
"""API URL prefix."""

# -----------------------------------------------------------------------------
# HttpCatalogStore
# -----------------------------------------------------------------------------


class HttpCatalogStore(CatalogStore):
    """A HTTP implementation of the MLTE catalog store."""

    def __init__(
        self, uri: StoreURI, client: OAuthHttpClient = RequestsClient()
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

        # Authenticate.
        self.client.authenticate(
            f"{self.url}{API_PREFIX}",
        )

    def close(self) -> None:
        """Close the session."""
        # Closing a remote HTTP session is a no-op.
        pass

    # TODO: implement read, search and mapper. Depends on backend existing first.
