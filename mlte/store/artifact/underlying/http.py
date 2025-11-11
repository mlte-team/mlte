"""Implementation of HTTP artifact store."""

from __future__ import annotations

import typing
from typing import Any, Optional, OrderedDict

from mlte.artifact.model import ArtifactModel
from mlte.backend.api.models.artifact_model import WriteArtifactRequest
from mlte.context.model import Model, Version
from mlte.store.artifact.store import ArtifactStore
from mlte.store.artifact.store_session import (
    ArtifactMapper,
    ArtifactStoreSession,
    ModelMapper,
    VersionMapper,
)
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
        """HTTP storage."""

        self.version_mapper = HTTPVersionMapper(storage=storage)
        """The mapper to version CRUD."""

        self.model_mapper = HTTPModelMapper(storage=storage)
        """The mapper to model CRUD."""

        self.artifact_mapper = HTTPArtifactMapper(storage=storage)
        """The mapper to artifact CRUD."""

        self.storage.start_session()

    def close(self):
        # No closing needed.
        pass


# -------------------------------------------------------------------------
# Model
# -------------------------------------------------------------------------


class HTTPModelMapper(ModelMapper):
    """HTTP mapper for the model resource."""

    def __init__(self, storage: HttpStorage) -> None:
        self.storage = storage
        """The HTTP storage access."""

    def create(self, model: Model, context: Any = None) -> Model:
        response = self.storage.post(json=model.to_json())
        return Model(**response)

    def read(self, model_id: str, context: Any = None) -> Model:
        response = self.storage.get(id=model_id)
        return Model(**response)

    def list(self, context: Any = None) -> list[str]:
        response = self.storage.get()
        return typing.cast(list[str], response)

    def delete(self, model_id: str, context: Any = None) -> Model:
        response = self.storage.delete(id=model_id)
        return Model(**response)


# -------------------------------------------------------------------------
# Version
# -------------------------------------------------------------------------


class HTTPVersionMapper(VersionMapper):
    """HTTP mapper for the version resource."""

    def __init__(self, storage: HttpStorage) -> None:
        self.storage = storage
        """The HTTP storage access."""

    def create(self, version: Version, model_id: str) -> Version:
        response = self.storage.post(
            json=version.to_json(), groups=_version_group(model_id)
        )
        return Version(**response)

    def read(self, version_id: str, model_id: str) -> Version:
        response = self.storage.get(
            id=version_id, groups=_version_group(model_id)
        )
        return Version(**response)

    def list(self, model_id: str) -> list[str]:
        response = self.storage.get(groups=_version_group(model_id))
        return typing.cast(list[str], response)

    def delete(self, version_id: str, model_id: str) -> Version:
        response = self.storage.delete(
            id=version_id, groups=_version_group(model_id)
        )
        return Version(**response)


# -------------------------------------------------------------------------
# Artifacts
# -------------------------------------------------------------------------


class HTTPArtifactMapper(ArtifactMapper):
    """HTTP mapper for the artifact resource."""

    def __init__(self, storage: HttpStorage) -> None:
        self.storage = storage
        """The HTTP storage access."""

    def read(
        self, artifact_id: str, model_and_version: tuple[str, str]
    ) -> ArtifactModel:
        model_id, version_id = model_and_version
        response = self.storage.get(
            id=artifact_id,
            groups=_artifact_groups(model_id, version_id),
        )
        return ArtifactModel(**response)

    def search(
        self, query: Query, model_and_version: Optional[tuple[str, str]] = None
    ) -> list[ArtifactModel]:
        groups: OrderedDict[str, str] = OrderedDict()
        if model_and_version:
            model_id, version_id = model_and_version
            groups = _artifact_groups(model_id, version_id)
        response = self.storage.send_command(
            MethodType.POST,
            id="search",
            json=query.to_json(),
            groups=groups,
        )
        return [ArtifactModel(**object) for object in response]

    def delete(
        self, artifact_id: str, model_and_version: tuple[str, str]
    ) -> ArtifactModel:
        model_id, version_id = model_and_version
        response = self.storage.delete(
            id=artifact_id, groups=_artifact_groups(model_id, version_id)
        )
        return ArtifactModel(**response)

    def _store_artifact(
        self, artifact: ArtifactModel, model_and_version: tuple[str, str]
    ) -> ArtifactModel:
        model_id, version_id = model_and_version
        response = self.storage.post(
            groups=_artifact_groups(model_id, version_id),
            json=WriteArtifactRequest(artifact=artifact).to_json(),
        )
        return ArtifactModel(**(response["artifact"]))

    def write_artifact(
        self,
        model_id: str,
        version_id: str,
        artifact: ArtifactModel,
        *,
        force: bool = False,
    ) -> ArtifactModel:
        response = self.storage.post(
            groups=_artifact_groups(model_id, version_id),
            json=WriteArtifactRequest(
                artifact=artifact,
                force=force,
                parents=False,  # This is set to false as it will be handled at the object level when this store is used.
            ).to_json(),
        )
        return ArtifactModel(**(response["artifact"]))


def _version_group(model_id: str) -> OrderedDict[str, str]:
    """Returns the resource group info for versions inside a model."""
    return OrderedDict([(model_id, VERSION_URL_KEY)])


def _artifact_groups(model_id: str, version_id: str) -> OrderedDict[str, str]:
    """Returns the resource group info for artifacts inside a version inside a model."""
    groups = _version_group(model_id)
    groups[version_id] = ARTIFACT_URL_KEY
    return groups
