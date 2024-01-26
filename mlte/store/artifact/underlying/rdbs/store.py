"""
mlte/store/artifact/underlying/rdbs/store.py

Implementation of relational database system artifact store.
"""

from typing import List

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy_utils

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
from mlte.store.artifact.underlying.rdbs.metadata import DBNamespace, create_all
from mlte.store.base import StoreURI

# -----------------------------------------------------------------------------
# RelationalDatabaseStoreSession
# -----------------------------------------------------------------------------


class RelationalDBStoreSession(ArtifactStoreSession):
    """A relational DB implementation of the MLTE artifact store."""

    def __init__(self, engine: sqlalchemy.engine.Engine) -> None:
        self.engine = engine
        """A reference to underlying storage."""

    def close(self) -> None:
        """Close the session."""
        self.engine.dispose()

    # -------------------------------------------------------------------------
    # Structural Elements
    # -------------------------------------------------------------------------

    def create_namespace(self, namespace: NamespaceCreate) -> Namespace:
        with sqlalchemy.orm.Session(self.engine) as session:
            namespace_obj = DBNamespace(name=namespace.identifier, models=[])
            session.add(namespace_obj)
            session.commit()
            return Namespace(identifier=namespace.identifier, models=[])

    def read_namespace(self, namespace_id: str) -> Namespace:
        with sqlalchemy.orm.Session(self.engine) as session:
            stmt = sqlalchemy.select(DBNamespace).where(
                DBNamespace.name == namespace_id
            )
            result = session.execute(stmt)

            namespace_obj = result.scalar()
            if namespace_obj is None:
                raise Exception(
                    f"Namespace with identifier {namespace_id} was not found in the artifact store."
                )
            else:
                return Namespace(
                    identifier=namespace_obj.name,
                    models=[
                        Model(
                            identifier=model_obj.name,
                            versions=[
                                Version(identifier=version_obj.name)
                                for version_obj in model_obj.versions
                            ],
                        )
                        for model_obj in namespace_obj.models
                    ],
                )

    def list_namespaces(self) -> List[str]:
        namespaces: List[str] = []
        with sqlalchemy.orm.Session(self.engine) as session:
            stmt = sqlalchemy.select(DBNamespace)
            result = session.execute(stmt)

            for namespace_obj in result.scalars():
                namespaces.append(namespace_obj.name)

        return namespaces

    def delete_namespace(self, namespace_id: str) -> Namespace:
        with sqlalchemy.orm.Session(self.engine) as session:
            stmt = sqlalchemy.select(DBNamespace).where(
                DBNamespace.name == namespace_id
            )
            result = session.execute(stmt)

            namespace_obj = result.scalar()
            if namespace_obj is None:
                raise Exception(
                    f"Namespace with identifier {namespace_id} was not found in the artifact store."
                )
            else:
                namespace = Namespace(
                    identifier=namespace_obj.name,
                    models=[
                        Model(
                            identifier=model_obj.name,
                            versions=[
                                Version(identifier=version_obj.name)
                                for version_obj in model_obj.versions
                            ],
                        )
                        for model_obj in namespace_obj.models
                    ],
                )
                session.delete(namespace_obj)
                session.commit()
                return namespace

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

        self.engine = sqlalchemy.create_engine(uri.uri, echo=True)
        """The underlying storage for the store."""

        # Create the DB if it doesn't exist already.
        if not sqlalchemy_utils.database_exists(self.engine.url):
            sqlalchemy_utils.create_database(self.engine.url)

        # Creates the DB items if they don't exist already.
        create_all(self.engine)

    def session(self) -> RelationalDBStoreSession:  # type: ignore[override]
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return RelationalDBStoreSession(engine=self.engine)
