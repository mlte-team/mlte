"""
mlte/store/artifact/underlying/http.py

Implementation of HTTP artifact store.
"""

from __future__ import annotations

import typing
from enum import Enum
from typing import Any, List, Optional, Union

import httpx
import requests

import mlte.backend.api.codes as codes
import mlte.store.error as errors
from mlte.artifact.model import ArtifactModel
from mlte.backend.api.model import WriteArtifactRequest
from mlte.backend.core.config import settings
from mlte.context.model import Model, ModelCreate, Version, VersionCreate
from mlte.store.artifact.query import Query
from mlte.store.artifact.store import ArtifactStore, ArtifactStoreSession
from mlte.store.base import StoreURI
from mlte.store.user.underlying.default_user import (
    DEFAULT_PASSWORD,
    DEFAULT_USERNAME,
)

# -----------------------------------------------------------------------------
# HTTP Client Configuration
# -----------------------------------------------------------------------------


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

    def delete(self, url: str, **kwargs) -> HttpResponse:
        raise NotImplementedError("delete()")


class OAuthHttpClient(HttpClient):
    """A base HTTP client type for an server needing OAuth authentication."""

    TOKEN_REQ_PASS_PAYLOAD = {"grant_type": "password"}
    TOKEN_REQ_HEADERS = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    TOKEN_ENDPOINT = "/token"

    def __init__(self, type: HttpClientType) -> None:
        super().__init__(type)

        self.access_token: Optional[str] = None
        """The access token."""

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

    def authenticate(self, api_url: str, username: str, password: str):
        """Sends an authentication request and retrieves and stores the token."""
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

        response_data = response.json()
        if response_data is None:
            raise Exception(
                "Did not receive any valid response for token request."
            )
        if "access_token" not in response_data:
            raise Exception("Access token was not contained in response.")

        self._store_token(response_data["access_token"])


class RequestsClient(OAuthHttpClient):
    """Client implementation using requests library."""

    def __init__(self) -> None:
        super().__init__(HttpClientType.REQUESTS)

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

    def delete(self, url: str, **kwargs) -> requests.Response:
        return requests.delete(url, headers=self.headers, **kwargs)


# -----------------------------------------------------------------------------
# RemoteHttpStore
# -----------------------------------------------------------------------------


class RemoteHttpStore(ArtifactStore):
    """A remote HTTP implementation of the MLTE artifact store."""

    def __init__(
        self, uri: StoreURI, client: OAuthHttpClient = RequestsClient()
    ) -> None:
        super().__init__(uri=uri)

        self.client = client
        """The client for requests."""

    def session(self) -> RemoteHttpStoreSession:  # type: ignore[override]
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return RemoteHttpStoreSession(url=self.uri.uri, client=self.client)


# -----------------------------------------------------------------------------
# RemoteHttpStoreSession
# -----------------------------------------------------------------------------


class RemoteHttpStoreSession(ArtifactStoreSession):
    """An in-memory implementation of the MLTE artifact store."""

    def __init__(self, *, url: str, client: OAuthHttpClient) -> None:
        self.url = url
        """The remote artifact store URL."""

        self.client = client
        """The client for HTTP requests."""

        # Authenticate.
        # TODO: fix this, what username is used in general? How does a local install get this?
        self.client.authenticate(
            f"{self.url}{settings.API_PREFIX}",
            username=DEFAULT_USERNAME,
            password=DEFAULT_PASSWORD,
        )

    def close(self) -> None:
        """Close the session."""
        # NOTE(Kyle): Closing a remote HTTP session is a no-op.
        pass

    # -------------------------------------------------------------------------
    # Structural Elements
    # -------------------------------------------------------------------------

    def create_model(self, model: ModelCreate) -> Model:
        url = f"{self.url}{settings.API_PREFIX}/model"
        res = self.client.post(url, json=model.model_dump())
        raise_for_response(res)

        return Model(**res.json())

    def read_model(self, model_id: str) -> Model:
        url = f"{self.url}{settings.API_PREFIX}/model/{model_id}"
        res = self.client.get(url)
        raise_for_response(res)

        return Model(**res.json())

    def list_models(self) -> List[str]:
        url = f"{self.url}{settings.API_PREFIX}/model"
        res = self.client.get(url)
        raise_for_response(res)

        return typing.cast(List[str], res.json())

    def delete_model(self, model_id: str) -> Model:
        url = f"{self.url}{settings.API_PREFIX}/model/{model_id}"
        res = self.client.delete(url)
        raise_for_response(res)

        return Model(**res.json())

    def create_version(self, model_id: str, version: VersionCreate) -> Version:
        url = f"{self.url}{settings.API_PREFIX}/model/{model_id}/version"
        res = self.client.post(url, json=version.model_dump())
        raise_for_response(res)

        return Version(**res.json())

    def read_version(self, model_id: str, version_id: str) -> Version:
        url = f"{self.url}{settings.API_PREFIX}/model/{model_id}/version/{version_id}"
        res = self.client.get(url)
        raise_for_response(res)

        return Version(**res.json())

    def list_versions(self, model_id: str) -> List[str]:
        url = f"{self.url}{settings.API_PREFIX}/model/{model_id}/version"
        res = self.client.get(url)
        raise_for_response(res)

        return typing.cast(List[str], res.json())

    def delete_version(self, model_id: str, version_id: str) -> Version:
        url = f"{self.url}{settings.API_PREFIX}/model/{model_id}/version/{version_id}"
        res = self.client.delete(url)
        raise_for_response(res)

        return Version(**res.json())

    # -------------------------------------------------------------------------
    # Artifacts
    # -------------------------------------------------------------------------

    def write_artifact(
        self,
        model_id: str,
        version_id: str,
        artifact: ArtifactModel,
        *,
        force: bool = False,
        parents: bool = False,
    ) -> ArtifactModel:
        url = f"{_url(self.url, model_id, version_id)}/artifact"
        res = self.client.post(
            url,
            json=WriteArtifactRequest(
                artifact=artifact, force=force, parents=parents
            ).model_dump(),
        )
        raise_for_response(res)

        return ArtifactModel(**(res.json()["artifact"]))

    def read_artifact(
        self,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> ArtifactModel:
        url = f"{_url(self.url, model_id, version_id)}/artifact/{artifact_id}"
        res = self.client.get(url)
        raise_for_response(res)

        return ArtifactModel(**res.json())

    def read_artifacts(
        self,
        model_id: str,
        version_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ArtifactModel]:
        url = f"{_url(self.url, model_id, version_id)}/artifact?limit={limit}&offset={offset}"
        res = self.client.get(url)
        raise_for_response(res)

        return [ArtifactModel(**object) for object in res.json()]

    def search_artifacts(
        self,
        model_id: str,
        version_id: str,
        query: Query = Query(),
    ) -> List[ArtifactModel]:
        # NOTE(Kyle): This operation always uses the "advanced search" functionality
        url = f"{_url(self.url, model_id, version_id)}/artifact/search"
        res = self.client.post(url, json=query.model_dump())
        raise_for_response(res)

        return [ArtifactModel(**object) for object in res.json()]

    def delete_artifact(
        self,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> ArtifactModel:
        url = f"{_url(self.url, model_id, version_id)}/artifact/{artifact_id}"
        res = self.client.delete(url)
        raise_for_response(res)

        return ArtifactModel(**res.json())


def _url(base: str, model_id: str, version_id: str) -> str:
    """
    Format a URL.
    :param base: The base URL
    :param model_id: The model identifier
    :param version_id: The version identifier
    :return: The formatted URL
    """
    return f"{base}{settings.API_PREFIX}/model/{model_id}/version/{version_id}"


def raise_for_response(response: HttpResponse) -> None:
    """
    Raise an error from from a response.
    :param response: The response object
    :raises: Error in the event an error occurred
    """
    if response.status_code == codes.OK:
        return
    if response.status_code == codes.NOT_FOUND:
        raise errors.ErrorNotFound(f"{response.json()}")
    if response.status_code == codes.ALREADY_EXISTS:
        raise errors.ErrorAlreadyExists(f"{response.json()}")
    else:
        raise errors.InternalError(f"{response.json()}")
