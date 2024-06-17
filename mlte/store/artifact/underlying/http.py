"""
mlte/store/artifact/underlying/http.py

Implementation of HTTP artifact store.
"""

from __future__ import annotations

import typing
from typing import List

from mlte.artifact.model import ArtifactModel
from mlte.backend.api.model import WriteArtifactRequest
from mlte.backend.core.config import settings
from mlte.context.model import Model, ModelCreate, Version, VersionCreate
from mlte.store.artifact.query import Query
from mlte.store.artifact.store import ArtifactStore, ArtifactStoreSession
from mlte.store.base import StoreURI
from mlte.store.common.http_clients import OAuthHttpClient, RequestsClient

# -----------------------------------------------------------------------------
# HttpArtifactStore
# -----------------------------------------------------------------------------


class HttpArtifactStore(ArtifactStore):
    """A HTTP implementation of the MLTE artifact store."""

    def __init__(
        self, uri: StoreURI, client: OAuthHttpClient = RequestsClient()
    ) -> None:
        self.client = client
        """The client for requests."""

        # Get credentials, if any, from the uri and into the client.
        uri.uri = self.client.process_credentials(uri.uri)
        super().__init__(uri=uri)

    def session(self) -> HttpArtifactStoreSession:  # type: ignore[override]
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return HttpArtifactStoreSession(url=self.uri.uri, client=self.client)


# -----------------------------------------------------------------------------
# HttpArtifactStoreSession
# -----------------------------------------------------------------------------


class HttpArtifactStoreSession(ArtifactStoreSession):
    """An HTTP implementation of the MLTE artifact store session."""

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

    # -------------------------------------------------------------------------
    # Structural Elements
    # -------------------------------------------------------------------------

    def create_model(self, model: ModelCreate) -> Model:
        url = f"{self.url}{settings.API_PREFIX}/model"
        res = self.client.post(url, json=model.model_dump())
        self.client.raise_for_response(res)

        return Model(**res.json())

    def read_model(self, model_id: str) -> Model:
        url = f"{self.url}{settings.API_PREFIX}/model/{model_id}"
        res = self.client.get(url)
        self.client.raise_for_response(res)

        return Model(**res.json())

    def list_models(self) -> List[str]:
        url = f"{self.url}{settings.API_PREFIX}/model"
        res = self.client.get(url)
        self.client.raise_for_response(res)

        return typing.cast(List[str], res.json())

    def delete_model(self, model_id: str) -> Model:
        url = f"{self.url}{settings.API_PREFIX}/model/{model_id}"
        res = self.client.delete(url)
        self.client.raise_for_response(res)

        return Model(**res.json())

    def create_version(self, model_id: str, version: VersionCreate) -> Version:
        url = f"{self.url}{settings.API_PREFIX}/model/{model_id}/version"
        res = self.client.post(url, json=version.model_dump())
        self.client.raise_for_response(res)

        return Version(**res.json())

    def read_version(self, model_id: str, version_id: str) -> Version:
        url = f"{self.url}{settings.API_PREFIX}/model/{model_id}/version/{version_id}"
        res = self.client.get(url)
        self.client.raise_for_response(res)

        return Version(**res.json())

    def list_versions(self, model_id: str) -> List[str]:
        url = f"{self.url}{settings.API_PREFIX}/model/{model_id}/version"
        res = self.client.get(url)
        self.client.raise_for_response(res)

        return typing.cast(List[str], res.json())

    def delete_version(self, model_id: str, version_id: str) -> Version:
        url = f"{self.url}{settings.API_PREFIX}/model/{model_id}/version/{version_id}"
        res = self.client.delete(url)
        self.client.raise_for_response(res)

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
        self.client.raise_for_response(res)

        return ArtifactModel(**(res.json()["artifact"]))

    def read_artifact(
        self,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> ArtifactModel:
        url = f"{_url(self.url, model_id, version_id)}/artifact/{artifact_id}"
        res = self.client.get(url)
        self.client.raise_for_response(res)

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
        self.client.raise_for_response(res)

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
        self.client.raise_for_response(res)

        return [ArtifactModel(**object) for object in res.json()]

    def delete_artifact(
        self,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> ArtifactModel:
        url = f"{_url(self.url, model_id, version_id)}/artifact/{artifact_id}"
        res = self.client.delete(url)
        self.client.raise_for_response(res)

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
