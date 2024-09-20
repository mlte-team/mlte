"""
mlte/store/underlying/http_clients.py

HTTP clients that can be used by underlying stores to access remote HTTP stores.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional, Union

import httpx
import requests

import mlte._private.url as url_utils
import mlte.backend.api.codes as codes
import mlte.store.error as errors


class HttpClientType(Enum):
    """An enumeration over HTTP client types."""

    REQUESTS = "requests"
    """The requests-based HTTP client."""

    TESTCLIENT = "testclient"
    """The fastapi TestClient HTTP client."""


HttpResponse = Union[requests.Response, httpx.Response]
"""Standard HTTP response, both have same implicit interface."""


class HttpClient:
    """Interface for an HTTP client."""

    def __init__(self, type: HttpClientType) -> None:
        self.type = type
        self.headers: dict[str, str] = {}

    def get(self, url: str, **kwargs) -> HttpResponse:
        raise NotImplementedError("get()")

    def post(
        self, url: str, data: Any = None, json: Any = None, **kwargs
    ) -> HttpResponse:
        raise NotImplementedError("post()")

    def put(
        self, url: str, data: Any = None, json: Any = None, **kwargs
    ) -> HttpResponse:
        raise NotImplementedError("put()")

    def delete(self, url: str, **kwargs) -> HttpResponse:
        raise NotImplementedError("delete()")

    @staticmethod
    def raise_for_response(response: HttpResponse) -> None:
        """
        Raise an error from from a response.
        :param response: The response object
        """
        if response.status_code == codes.OK:
            return
        if response.status_code == codes.NOT_FOUND:
            raise errors.ErrorNotFound(f"{response.json()}")
        if response.status_code == codes.ALREADY_EXISTS:
            raise errors.ErrorAlreadyExists(f"{response.json()}")
        if response.status_code == codes.UNAUTHORIZED:
            raise errors.UnauthenticatedError(f"{response.json()}")
        if response.status_code == codes.FORBIDDEN:
            raise errors.ForbiddenError(f"{response.json()}")
        else:
            raise errors.InternalError(f"{response.json()}")


class OAuthHttpClient(HttpClient):
    """A base HTTP client type for an server needing OAuth authentication."""

    TOKEN_REQ_PASS_PAYLOAD = {"grant_type": "password"}
    TOKEN_REQ_HEADERS = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }
    TOKEN_ENDPOINT = "/token"

    def __init__(
        self,
        type: HttpClientType,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> None:
        super().__init__(type)

        self.access_token: Optional[str] = None
        """The access token."""

        self.username = username
        """The username to use when authenticating."""

        self.password = password
        """The password to use when authenticating."""

    def _format_oauth_password_payload(
        self, username: str, password: str
    ) -> dict[str, str]:
        """Returns a properly structured payload with credentials to be sent to get a token."""
        payload = dict(self.TOKEN_REQ_PASS_PAYLOAD)
        payload.update({"username": username, "password": password})
        return payload

    def _store_token(self, access_token: str):
        """Stores the token and sets proper headers."""
        if access_token is not None:
            self.access_token = access_token
            self.headers = {"Authorization": f"Bearer {self.access_token}"}

    def authenticate(
        self,
        api_url: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        """Sends an authentication request and retrieves and stores the token."""
        # Validate we have a user and password.
        if username is None:
            username = self.username
            if username is None:
                raise Exception(
                    "Can't authenticate without user, no internal or argument username received."
                )
        if password is None:
            password = self.password
            if password is None:
                raise Exception(
                    "Can't authenticate without password, no internal or argument password received."
                )

        # Send authentication request to get token.
        self.headers = self.TOKEN_REQ_HEADERS
        url = f"{api_url}{self.TOKEN_ENDPOINT}"
        response = self.post(
            url,
            data=self._format_oauth_password_payload(username, password),
        )
        self.headers = {}
        if response.status_code != codes.OK:
            reply = response.content.decode("utf-8")
            raise Exception(
                f"Token request was unsuccessful - code: {response.status_code}, reply: {reply}"
            )

        # Process reply and store token.
        response_data = response.json()
        if response_data is None:
            raise Exception(
                "Did not receive any valid response for token request."
            )
        if "access_token" not in response_data:
            raise Exception("Access token was not contained in response.")
        self._store_token(response_data["access_token"])

    def process_credentials(self, uri: str) -> str:
        """Obtains user and password from uri for client auth, and returns cleaned up uri."""
        # Parse URI for user and password.
        uri, username, password = url_utils.remove_url_username_password(uri)
        if username is not None and password is not None:
            # If URI had user and password, get them for client auth.
            self.username = username
            self.password = password

        return uri


class RequestsClient(OAuthHttpClient):
    """Client implementation using requests library."""

    def __init__(
        self, username: Optional[str] = None, password: Optional[str] = None
    ) -> None:
        super().__init__(HttpClientType.REQUESTS, username, password)

    def get(self, url: str, **kwargs) -> requests.Response:
        return requests.get(url, headers=self.headers, **kwargs)

    def post(
        self, url: str, data: Any = None, json: Any = None, **kwargs
    ) -> requests.Response:
        return requests.post(
            url,
            headers=self.headers,
            data=data,
            json=json,
            **kwargs,
        )

    def put(
        self, url: str, data: Any = None, json: Any = None, **kwargs
    ) -> requests.Response:
        return requests.put(
            url,
            headers=self.headers,
            data=data,
            json=json,
            **kwargs,
        )

    def delete(self, url: str, **kwargs) -> requests.Response:
        return requests.delete(url, headers=self.headers, **kwargs)
