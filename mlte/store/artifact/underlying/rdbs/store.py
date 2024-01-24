"""
mlte/store/artifact/underlying/rdbs/store.py

Implementation of relational database system artifact store.
"""

from typing import List

import sqlalchemy

from mlte.artifact.model import ArtifactModel
from mlte.context.model import (
    Model,
    ModelCreate,
    Namespace,
    NamespaceCreate,
    Version,
    VersionCreate,
)
from mlte.store.artifact.query import Query
from mlte.store.artifact.store import ArtifactStore, ArtifactStoreSession
from mlte.store.base import StoreURI

# -----------------------------------------------------------------------------
# RelationalDatabaseStoreSession
# -----------------------------------------------------------------------------


class RelationalDBStoreSession(ArtifactStoreSession):
    """A local file-system implementation of the MLTE artifact store."""

    def __init__(self, storage: sqlalchemy.engine.Engine) -> None:
        self.storage = storage
        """A reference to underlying storage."""

    def close(self) -> None:
        """Close the session."""
        self.storage.dispose()

    # -------------------------------------------------------------------------
    # Structural Elements
    # -------------------------------------------------------------------------

    def create_namespace(self, namespace: NamespaceCreate) -> Namespace:
        raise NotImplementedError("Not implemented")

    def read_namespace(self, namespace_id: str) -> Namespace:
        raise NotImplementedError("Not implemented")

    def list_namespaces(self) -> List[str]:
        raise NotImplementedError("Not implemented")

    def delete_namespace(self, namespace_id: str) -> Namespace:
        raise NotImplementedError("Not implemented")

    def create_model(self, namespace_id: str, model: ModelCreate) -> Model:
        raise NotImplementedError("Not implemented")

    def read_model(self, namespace_id: str, model_id: str) -> Model:
        raise NotImplementedError("Not implemented")

    def list_models(self, namespace_id: str) -> List[str]:
        raise NotImplementedError("Not implemented")

    def delete_model(self, namespace_id: str, model_id: str) -> Model:
        raise NotImplementedError("Not implemented")

    def create_version(
        self, namespace_id: str, model_id: str, version: VersionCreate
    ) -> Version:
        raise NotImplementedError("Not implemented")

    def read_version(
        self, namespace_id: str, model_id: str, version_id: str
    ) -> Version:
        raise NotImplementedError("Not implemented")

    def list_versions(self, namespace_id: str, model_id: str) -> List[str]:
        raise NotImplementedError("Not implemented")

    def delete_version(
        self, namespace_id: str, model_id: str, version_id: str
    ) -> Version:
        raise NotImplementedError("Not implemented")

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
        raise NotImplementedError("Not implemented")

    def read_artifact(
        self,
        namespace_id: str,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> ArtifactModel:
        raise NotImplementedError("Not implemented")

    def read_artifacts(
        self,
        namespace_id: str,
        model_id: str,
        version_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ArtifactModel]:
        raise NotImplementedError("Not implemented")

    def search_artifacts(
        self,
        namespace_id: str,
        model_id: str,
        version_id: str,
        query: Query = Query(),
    ) -> List[ArtifactModel]:
        raise NotImplementedError("Not implemented")

    def delete_artifact(
        self,
        namespace_id: str,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> ArtifactModel:
        raise NotImplementedError("Not implemented")


class RelationalDBStore(ArtifactStore):
    """A local file system implementation of the MLTE artifact store."""

    def __init__(self, uri: StoreURI) -> None:
        super().__init__(uri=uri)

        self.storage = sqlalchemy.create_engine(uri.uri, echo=True)
        """The underlying storage for the store."""

    def session(self) -> RelationalDBStoreSession:  # type: ignore[override]
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return RelationalDBStoreSession(storage=self.storage)
