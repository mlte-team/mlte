"""
mlte/store/catalog/common/http_store.py

Base class for HTTP based stores.
"""

from __future__ import annotations

from typing import Optional

from mlte.backend.core.config import settings
from mlte.store.base import StoreURI
from mlte.store.common.http_clients import OAuthHttpClient, RequestsClient
from mlte.store.common.storage import Storage

API_PREFIX = settings.API_PREFIX
"""API URL prefix."""


class HttpStorage(Storage):
    """An HTTP base storage."""

    def __init__(
        self,
        uri: StoreURI,
        client: Optional[OAuthHttpClient] = None,
    ) -> None:
        super().__init__(uri)

        if client is None:
            client = RequestsClient()
        self.client = client
        """The client for requests."""

        # Get credentials, if any, from the uri and into the client.
        uri.uri = self.client.process_credentials(uri.uri)
        self.clean_url = uri.uri
        """Store the clean URL without credentials."""

    def start_session(self):
        # Authenticate.
        self.client.authenticate(f"{self.clean_url}{API_PREFIX}")
