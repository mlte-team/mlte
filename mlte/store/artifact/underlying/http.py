"""
Implementation of HTTP artifact store.
"""

from __future__ import annotations

import typing
from typing import List, Optional, OrderedDict

from mlte.artifact.model import ArtifactModel
from mlte.backend.api.models.artifact_model import WriteArtifactRequest
from mlte.context.model import Model, Version
from mlte.store.artifact.store import ArtifactStore, ArtifactStoreSession
from mlte.store.base import StoreURI
from mlte.store.common.http_clients import OAuthHttpClient
from mlte.store.common.http_storage import HttpStorage
from mlte.store.query import Query
from mlte.user.model import MethodType, ResourceType

# -----------------------------------------------------------------------------
# HttpArtifactStore
# -----------------------------------------------------------------------------

VERSION_URL_KEY = "version"
ARTIFACT_URL_KEY = "artifact"


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
        response = self.storage.post(json=model.to_json())
        return Model(**response)

    def read_model(self, model_id: str) -> Model:
        response = self.storage.get(id=model_id)
        return Model(**response)

    def list_models(self) -> List[str]:
        response = self.storage.get()
        return typing.cast(List[str], response)

    def delete_model(self, model_id: str) -> Model:
        response = self.storage.delete(id=model_id)
        return Model(**response)

    # -------------------------------------------------------------------------
    # Version
    # -------------------------------------------------------------------------

    def create_version(self, model_id: str, version: Version) -> Version:
        response = self.storage.post(
            json=version.to_json(), groups=_version_group(model_id)
        )
        return Version(**response)

    def read_version(self, model_id: str, version_id: str) -> Version:
        response = self.storage.get(
            id=version_id, groups=_version_group(model_id)
        )
        return Version(**response)

    def list_versions(self, model_id: str) -> List[str]:
        response = self.storage.get(groups=_version_group(model_id))
        return typing.cast(List[str], response)

    def delete_version(self, model_id: str, version_id: str) -> Version:
        response = self.storage.delete(
            id=version_id, groups=_version_group(model_id)
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
        response = self.storage.post(
            groups=_artifact_groups(model_id, version_id),
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
        response = self.storage.get(
            id=artifact_id,
            groups=_artifact_groups(model_id, version_id),
        )
        return ArtifactModel(**response)

    def read_artifacts(
        self,
        model_id: str,
        version_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ArtifactModel]:
        response = self.storage.get(
            groups=_artifact_groups(model_id, version_id),
            query_args={"limit": f"{limit}", "offset": f"{offset}"},
        )
        return [ArtifactModel(**object) for object in response]

    def search_artifacts(
        self,
        model_id: str,
        version_id: str,
        query: Query = Query(),
    ) -> List[ArtifactModel]:
        # NOTE(Kyle): This operation always uses the "advanced search" functionality
        response = self.storage.send_command(
            MethodType.POST,
            id="search",
            json=query.to_json(),
            groups=_artifact_groups(model_id, version_id),
        )
        return [ArtifactModel(**object) for object in response]

    def delete_artifact(
        self,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> ArtifactModel:
        response = self.storage.delete(
            id=artifact_id, groups=_artifact_groups(model_id, version_id)
        )
        return ArtifactModel(**response)


def _version_group(model_id: str) -> OrderedDict[str, str]:
    """Returns the resource group info for versions inside a model."""
    return OrderedDict([(model_id, VERSION_URL_KEY)])


def _artifact_groups(model_id: str, version_id: str) -> OrderedDict[str, str]:
    """Returns the resource group info for artifacts inside a version inside a model."""
    groups = _version_group(model_id)
    groups[version_id] = ARTIFACT_URL_KEY
    return groups
