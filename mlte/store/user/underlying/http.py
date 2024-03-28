"""
mlte/store/user/underlying/http.py

Implementation of HTTP user store.
"""

from __future__ import annotations

import typing
from typing import List

from mlte.backend.core.config import settings
from mlte.store.base import StoreURI
from mlte.store.common.http_clients import OAuthHttpClient, RequestsClient
from mlte.store.user.store import UserStore, UserStoreSession
from mlte.user.model import BasicUser, UserCreate

# -----------------------------------------------------------------------------
# HttpUserStore
# -----------------------------------------------------------------------------


class HttpUserStore(UserStore):
    """A HTTP implementation of the MLTE user store."""

    def __init__(
        self, uri: StoreURI, client: OAuthHttpClient = RequestsClient()
    ) -> None:
        self.client = client
        """The client for requests."""

        # Get credentials, if any, from the uri and into the client.
        uri.uri = self.client.process_credentials(uri.uri)
        super().__init__(uri=uri)

    def session(self) -> HttpUserStoreSession:  # type: ignore[override]
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return HttpUserStoreSession(url=self.uri.uri, client=self.client)


# -----------------------------------------------------------------------------
# HttpUserStoreSession
# -----------------------------------------------------------------------------


class HttpUserStoreSession(UserStoreSession):
    """An HTTP implementation of the MLTE user store session."""

    USER_URL = "/user"
    """The relative URL for user actions."""

    def __init__(self, *, url: str, client: OAuthHttpClient) -> None:
        self.url = url
        """The remote artifact store URL."""

        self.client = client
        """The client for HTTP requests."""

        # Authenticate.
        self.client.authenticate(
            f"{self.url}{settings.API_PREFIX}",
        )

    def close(self) -> None:
        """Close the session."""
        # Closing a remote HTTP session is a no-op.
        pass

    def _base_url(self) -> str:
        """Returns the base url for User actions."""
        return f"{self.url}{settings.API_PREFIX}{self.USER_URL}"

    # -------------------------------------------------------------------------
    # Actions
    # -------------------------------------------------------------------------

    def create_user(self, model: UserCreate) -> BasicUser:
        res = self.client.post(self._base_url(), json=model.model_dump())
        self.client.raise_for_response(res)
        return BasicUser(**res.json())

    def read_user(self, user_id: str) -> BasicUser:
        url = f"{self._base_url()}/{user_id}"
        res = self.client.get(url)
        self.client.raise_for_response(res)
        return BasicUser(**res.json())

    def list_users(self) -> List[str]:
        res = self.client.get(self._base_url())
        self.client.raise_for_response(res)
        return typing.cast(List[str], res.json())

    def delete_user(self, user_id: str) -> BasicUser:
        url = f"{self._base_url()}/{user_id}"
        res = self.client.delete(url)
        self.client.raise_for_response(res)
        return BasicUser(**res.json())
