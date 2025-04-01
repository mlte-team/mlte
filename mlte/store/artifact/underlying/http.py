"""
Implementation of HTTP artifact store.
"""

from __future__ import annotations

import typing
from typing import List, Optional

from mlte.artifact.model import ArtifactModel
from mlte.backend.api.models.artifact_model import WriteArtifactRequest
from mlte.context.model import Model, Version
from mlte.store.artifact.store import ArtifactStore, ArtifactStoreSession
from mlte.store.base import StoreURI
from mlte.store.common.http_clients import OAuthHttpClient
from mlte.store.common.http_storage import HttpStorage
from mlte.store.query import Query
from mlte.user.model import ResourceType

# -----------------------------------------------------------------------------
# HttpArtifactStore
# -----------------------------------------------------------------------------


class HttpArtifactStore(ArtifactStore):
    """A HTTP implementation of the MLTE artifact store."""

    def __init__(
        self, *, uri: StoreURI, client: Optional[OAuthHttpClient] = None
    ) -> None:
        super().__init__(uri=uri)

        self.storage = HttpStorage(
            uri=uri, resource_type=ResourceType.MODEL, client=client
        )
        """HTTP storage."""

    def session(self) -> HttpArtifactStoreSession:
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return HttpArtifactStoreSession(storage=self.storage)


# -----------------------------------------------------------------------------
# HttpArtifactStoreSession
# -----------------------------------------------------------------------------


class HttpArtifactStoreSession(ArtifactStoreSession):
    """An HTTP implementation of the MLTE artifact store session."""

    def __init__(self, *, storage: HttpStorage) -> None:
        self.storage = storage
        """HTTP Storage."""

        self.storage.start_session()

    def close(self):
        # No closing needed.
        pass

    # -------------------------------------------------------------------------
    # Model
    # -------------------------------------------------------------------------

    def create_model(self, model: Model) -> Model:
        response = self.storage.post(resource_url="", json=model.to_json())
        return Model(**response)

    def read_model(self, model_id: str) -> Model:
        response = self.storage.get(resource_url=f"/{model_id}")
        return Model(**response)

    def list_models(self) -> List[str]:
        response = self.storage.get(resource_url="")
        return typing.cast(List[str], response)

    def delete_model(self, model_id: str) -> Model:
        response = self.storage.delete(resource_url=f"/{model_id}")
        return Model(**response)

    # -------------------------------------------------------------------------
    # Version
    # -------------------------------------------------------------------------

    def create_version(self, model_id: str, version: Version) -> Version:
        response = self.storage.post(
            resource_url=f"/{model_id}/version", json=version.to_json()
        )
        return Version(**response)

    def read_version(self, model_id: str, version_id: str) -> Version:
        response = self.storage.get(
            resource_url=f"/{model_id}/version/{version_id}"
        )
        return Version(**response)

    def list_versions(self, model_id: str) -> List[str]:
        response = self.storage.get(resource_url=f"/{model_id}/version")
        return typing.cast(List[str], response)

    def delete_version(self, model_id: str, version_id: str) -> Version:
        response = self.storage.delete(
            resource_url=f"/{model_id}/version/{version_id}"
        )
        return Version(**response)

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
        url = f"{_url(model_id, version_id)}/artifact"
        response = self.storage.post(
            url,
            json=WriteArtifactRequest(
                artifact=artifact, force=force, parents=parents
            ).to_json(),
        )
        return ArtifactModel(**(response["artifact"]))

    def read_artifact(
        self,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> ArtifactModel:
        url = f"{_url(model_id, version_id)}/artifact/{artifact_id}"
        response = self.storage.get(url)
        return ArtifactModel(**response)

    def read_artifacts(
        self,
        model_id: str,
        version_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ArtifactModel]:
        url = f"{_url(model_id, version_id)}/artifact?limit={limit}&offset={offset}"
        response = self.storage.get(url)
        return [ArtifactModel(**object) for object in response]

    def search_artifacts(
        self,
        model_id: str,
        version_id: str,
        query: Query = Query(),
    ) -> List[ArtifactModel]:
        # NOTE(Kyle): This operation always uses the "advanced search" functionality
        url = f"{_url(model_id, version_id)}/artifact/search"
        response = self.storage.post(url, json=query.to_json())
        return [ArtifactModel(**object) for object in response]

    def delete_artifact(
        self,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> ArtifactModel:
        url = f"{_url(model_id, version_id)}/artifact/{artifact_id}"
        response = self.storage.delete(url)
        return ArtifactModel(**response)


def _url(model_id: str, version_id: str) -> str:
    """
    Format a URL.
    :param model_id: The model identifier
    :param version_id: The version identifier
    :return: The formatted URL
    """
    return f"/{model_id}/version/{version_id}"
