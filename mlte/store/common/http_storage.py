"""
Base class for HTTP based stores.
"""

from __future__ import annotations

from typing import Any, Optional

from mlte.backend.core.config import settings
from mlte.store.base import StoreURI
from mlte.store.common.http_clients import OAuthHttpClient, RequestsClient
from mlte.store.common.storage import Storage
from mlte.user.model import MethodType, ResourceType

API_PREFIX = settings.API_PREFIX
"""API URL prefix."""


class HttpStorage(Storage):
    """An HTTP base storage for a given resource type."""

    def __init__(
        self,
        uri: StoreURI,
        resource_type: ResourceType,
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

        self.base_url = f"{self.clean_url}{API_PREFIX}/{resource_type.value}"
        """Base resource URL."""

    def start_session(self):
        """Perform authentication."""
        self.client.authenticate(f"{self.clean_url}{API_PREFIX}")

    def post(self, resource_url: str, json: Any) -> Any:
        """Post method, to create resource."""
        return self.send_command(resource_url, MethodType.POST, json)

    def put(self, resource_url: str, json: Any) -> Any:
        """Put method, to update resource."""
        return self.send_command(resource_url, MethodType.PUT, json)

    def get(self, resource_url: str) -> Any:
        """Get method, to read resource."""
        return self.send_command(resource_url, MethodType.GET)

    def delete(self, resource_url: str) -> Any:
        """Delete method, to remove resource."""
        return self.send_command(resource_url, MethodType.DELETE)

    def send_command(
        self, resource_url: str, method: MethodType, json: Optional[Any] = None
    ):
        url = f"{self.base_url}{resource_url}"
        if method == MethodType.POST:
            res = self.client.post(url, json=json)
        elif method == MethodType.PUT:
            res = self.client.put(url, json=json)
        elif method == MethodType.GET:
            res = self.client.get(url)
        elif method == MethodType.DELETE:
            res = self.client.delete(url)
        else:
            raise RuntimeError(f"Invalid method type: {method}")
        self.client.raise_for_response(res)
        return res.json()
