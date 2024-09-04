"""
mlte/store/catalog/common/http_store.py

Base class for HTTP based stores.
"""

from __future__ import annotations

from mlte.backend.core.config import settings
from mlte.store.base import StoreURI
from mlte.store.common.http_clients import OAuthHttpClient, RequestsClient

API_PREFIX = settings.API_PREFIX
"""API URL prefix."""


class HttpStorage:
    """An HTTP base storage."""

    def __init__(
        self,
        uri: StoreURI,
        client: OAuthHttpClient = RequestsClient(),
    ) -> None:
        self.client = client
        """The client for requests."""

        # Get credentials, if any, from the uri and into the client.
        uri.uri = self.client.process_credentials(uri.uri)
        self.url = uri.uri

    def start_session(self):
        # Authenticate.
        self.client.authenticate(f"{self.url}{API_PREFIX}")
