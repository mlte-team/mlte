"""
mlte/store/underlying/http.py

Implementation of remote HTTP artifact store.
"""

from __future__ import annotations

import typing
from enum import Enum
from typing import Any, List

import requests

import mlte.store.error as errors
import mlte.web.store.api.codes as codes
from mlte.artifact.model import ArtifactModel
from mlte.context.model import (
    Model,
    ModelCreate,
    Namespace,
    NamespaceCreate,
    Version,
    VersionCreate,
)
from mlte.store.base import Store, StoreSession, StoreURI
from mlte.store.query import Query
from mlte.web.store.api.model import WriteArtifactRequest

# -----------------------------------------------------------------------------
# Client Configuration
# -----------------------------------------------------------------------------


class ClientType(Enum):
    """An enumeration over client types."""

    REQUESTS = "requests"
    """The requests-based client."""

    TESTCLIENT = "testclient"
    """The fastapi TestClient client."""


class RemoteHttpStoreClient:
    """A base client type for RemoteHttpStore."""

    def __init__(self, type: ClientType) -> None:
        self.type = type

    def get(self, url: str, **kwargs) -> requests.Response:
        raise NotImplementedError("get()")

    def post(
        self, url: str, data: Any = None, json: Any = None, **kwargs
    ) -> requests.Response:
        raise NotImplementedError("post()")

    def delete(self, url: str, **kwargs) -> requests.Response:
        raise NotImplementedError("delete()")


class RequestsClient(RemoteHttpStoreClient):
    def __init__(self) -> None:
        super().__init__(ClientType.REQUESTS)

    def get(self, url: str, **kwargs) -> requests.Response:
        return requests.get(url, **kwargs)

    def post(
        self, url: str, data: Any = None, json: Any = None, **kwargs
    ) -> requests.Response:
        return requests.post(url, data=data, json=json, **kwargs)

    def delete(self, url: str, **kwargs) -> requests.Response:
        return requests.delete(url, **kwargs)


# -----------------------------------------------------------------------------
# RemoteHttpStoreSession
# -----------------------------------------------------------------------------


class RemoteHttpStoreSession(StoreSession):
    """An in-memory implementation of the MLTE artifact store."""

    def __init__(self, *, url: str, client: RemoteHttpStoreClient) -> None:
        self.url = url
        """The remote artifact store URL."""

        self.client = client
        """The client for HTTP requests."""

    def close(self) -> None:
        """Close the session."""
        # NOTE(Kyle): Closing a remote HTTP session is a no-op.
        pass

    # -------------------------------------------------------------------------
    # Structural Elements
    # -------------------------------------------------------------------------

    def create_namespace(self, namespace: NamespaceCreate) -> Namespace:
        url = f"{self.url}/api/namespace"
        res = self.client.post(url, json=namespace.model_dump())
        raise_for_response(res)

        return Namespace(**res.json())

    def read_namespace(self, namespace_id: str) -> Namespace:
        url = f"{self.url}/api/namespace/{namespace_id}"
        res = self.client.get(url)
        raise_for_response(res)

        return Namespace(**res.json())

    def list_namespaces(self) -> List[str]:
        url = f"{self.url}/api/namespace"
        res = self.client.get(url)
        raise_for_response(res)

        return typing.cast(List[str], res.json())

    def delete_namespace(self, namespace_id: str) -> Namespace:
        url = f"{self.url}/api/namespace/{namespace_id}"
        res = self.client.delete(url)
        raise_for_response(res)

        return Namespace(**res.json())

    def create_model(self, namespace_id: str, model: ModelCreate) -> Model:
        url = f"{self.url}/api/namespace/{namespace_id}/model"
        res = self.client.post(url, json=model.model_dump())
        raise_for_response(res)

        return Model(**res.json())

    def read_model(self, namespace_id: str, model_id: str) -> Model:
        url = f"{self.url}/api/namespace/{namespace_id}/model/{model_id}"
        res = self.client.get(url)
        raise_for_response(res)

        return Model(**res.json())

    def list_models(self, namespace_id: str) -> List[str]:
        url = f"{self.url}/api/namespace/{namespace_id}/model"
        res = self.client.get(url)
        raise_for_response(res)

        return typing.cast(List[str], res.json())

    def delete_model(self, namespace_id: str, model_id: str) -> Model:
        url = f"{self.url}/api/namespace/{namespace_id}/model/{model_id}"
        res = self.client.delete(url)
        raise_for_response(res)

        return Model(**res.json())

    def create_version(
        self, namespace_id: str, model_id: str, version: VersionCreate
    ) -> Version:
        url = (
            f"{self.url}/api/namespace/{namespace_id}/model/{model_id}/version"
        )
        res = self.client.post(url, json=version.model_dump())
        raise_for_response(res)

        return Version(**res.json())

    def read_version(
        self, namespace_id: str, model_id: str, version_id: str
    ) -> Version:
        url = f"{self.url}/api/namespace/{namespace_id}/model/{model_id}/version/{version_id}"
        res = self.client.get(url)
        raise_for_response(res)

        return Version(**res.json())

    def list_versions(self, namespace_id: str, model_id: str) -> List[str]:
        url = (
            f"{self.url}/api/namespace/{namespace_id}/model/{model_id}/version"
        )
        res = self.client.get(url)
        raise_for_response(res)

        return typing.cast(List[str], res.json())

    def delete_version(
        self, namespace_id: str, model_id: str, version_id: str
    ) -> Version:
        url = f"{self.url}/api/namespace/{namespace_id}/model/{model_id}/version/{version_id}"
        res = self.client.delete(url)
        raise_for_response(res)

        return Version(**res.json())

    # -------------------------------------------------------------------------
    # Artifacts
    # -------------------------------------------------------------------------

    def write_artifact(
        self,
        namespace_id: str,
        model_id: str,
        version_id: str,
        artifact: ArtifactModel,
        *,
        force: bool = False,
        parents: bool = False,
    ) -> ArtifactModel:
        url = f"{_url(self.url, namespace_id, model_id, version_id)}/artifact"
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
        namespace_id: str,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> ArtifactModel:
        url = f"{_url(self.url, namespace_id, model_id, version_id)}/artifact/{artifact_id}"
        res = self.client.get(url)
        raise_for_response(res)

        return ArtifactModel(**res.json())

    def read_artifacts(
        self,
        namespace_id: str,
        model_id: str,
        version_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ArtifactModel]:
        url = f"{_url(self.url, namespace_id, model_id, version_id)}/artifact?limit={limit}&offset={offset}"
        res = self.client.get(url)
        raise_for_response(res)

        return [ArtifactModel(**object) for object in res.json()]

    def search_artifacts(
        self,
        namespace_id: str,
        model_id: str,
        version_id: str,
        query: Query = Query(),
    ) -> List[ArtifactModel]:
        # NOTE(Kyle): This operation always uses the "advanced search" functionality
        url = f"{_url(self.url, namespace_id, model_id, version_id)}/artifact/search"
        res = self.client.post(url, json=query.model_dump())
        raise_for_response(res)

        return [ArtifactModel(**object) for object in res.json()]

    def delete_artifact(
        self,
        namespace_id: str,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> ArtifactModel:
        url = f"{_url(self.url, namespace_id, model_id, version_id)}/artifact/{artifact_id}"
        res = self.client.delete(url)
        raise_for_response(res)

        return ArtifactModel(**res.json())


def _url(base: str, namespace_id: str, model_id: str, version_id: str) -> str:
    """
    Format a URL.
    :param base: The base URL
    :param namespace_id: The namespace identifier
    :param model_id: The model identifier
    :param version_id: The version identifier
    :return: The formatted URL
    """
    return f"{base}/api/namespace/{namespace_id}/model/{model_id}/version/{version_id}"


def raise_for_response(response: requests.Response) -> None:
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


class RemoteHttpStore(Store):
    """A remote HTTP implementation of the MLTE artifact store."""

    def __init__(
        self, uri: StoreURI, client: RemoteHttpStoreClient = RequestsClient()
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
