"""
mlte/store/artifact/underlying/rdbs/store.py

Implementation of relational database system artifact store.
"""

from typing import List, Tuple

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy_utils

import mlte.store.error as errors
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
from mlte.store.artifact.underlying.rdbs.metadata import (
    DBModel,
    DBNamespace,
    DBVersion,
    create_all,
)
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
            namespace, _ = self._read_namespace(namespace_id, session)
            return namespace

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
            namespace, namespace_obj = self._read_namespace(
                namespace_id, session
            )
            session.delete(namespace_obj)
            session.commit()
            return namespace

    def _read_namespace(
        self, namespace_id: str, session: sqlalchemy.orm.Session
    ) -> Tuple[Namespace, DBNamespace]:
        """Reads the namespace with the given identifier using the provided session, and returns a Namespace and DBNamespace object."""
        stmt = sqlalchemy.select(DBNamespace).where(
            DBNamespace.name == namespace_id
        )
        result = session.execute(stmt)

        namespace_obj = result.scalar()
        if namespace_obj is None:
            raise errors.ErrorNotFound(
                f"Namespace with identifier {namespace_id} was not found in the artifact store."
            )
        else:
            return (
                Namespace(
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
                ),
                namespace_obj,
            )

    def create_model(self, namespace_id: str, model: ModelCreate) -> Model:
        with sqlalchemy.orm.Session(self.engine) as session:
            # Check if namespace exists.
            _, namespace_obj = self._read_namespace(namespace_id, session)

            # Now create model.
            model_obj = DBModel(
                name=model.identifier,
                namespace_id=namespace_obj.id,
                versions=[],
            )
            session.add(model_obj)
            session.commit()
            return Model(identifier=model.identifier, versions=[])

    def read_model(self, namespace_id: str, model_id: str) -> Model:
        with sqlalchemy.orm.Session(self.engine) as session:
            model, _ = self._read_model(model_id, namespace_id, session)
            return model

    def list_models(self, namespace_id: str) -> List[str]:
        models: List[str] = []
        with sqlalchemy.orm.Session(self.engine) as session:
            stmt = sqlalchemy.select(DBModel).where(
                DBNamespace.name == namespace_id
            )
            result = session.execute(stmt)
            for model_obj in result.scalars():
                models.append(model_obj.name)
        return models

    def delete_model(self, namespace_id: str, model_id: str) -> Model:
        with sqlalchemy.orm.Session(self.engine) as session:
            model, model_obj = self._read_model(model_id, namespace_id, session)
            session.delete(model_obj)
            session.commit()
            return model

    def _read_model(
        self, model_id: str, namespace_id: str, session: sqlalchemy.orm.Session
    ) -> Tuple[Model, DBModel]:
        """Reads the model with the given identifier using the provided session, and returns a Model and DBModel object."""
        stmt = (
            sqlalchemy.select(DBModel)
            .where(DBModel.name == model_id)
            .where(DBNamespace.name == namespace_id)
        )
        result = session.execute(stmt)

        model_obj = result.scalar()
        if model_obj is None:
            raise errors.ErrorNotFound(
                f"Model with identifier {model_id} and associated to namespace {namespace_id} was not found in the artifact store."
            )
        else:
            return (
                Model(
                    identifier=model_obj.name,
                    versions=[
                        Version(identifier=version_obj.name)
                        for version_obj in model_obj.versions
                    ],
                ),
                model_obj,
            )

    def create_version(
        self, namespace_id: str, model_id: str, version: VersionCreate
    ) -> Version:
        with sqlalchemy.orm.Session(self.engine) as session:
            # Check if namespace and model exist.
            _, _ = self._read_namespace(namespace_id, session)
            _, model_obj = self._read_model(model_id, namespace_id, session)

            # Now create version.
            version_obj = DBVersion(
                name=version.identifier, model_id=model_obj.id
            )
            session.add(version_obj)
            session.commit()
            return Version(identifier=version.identifier)

    def read_version(
        self, namespace_id: str, model_id: str, version_id: str
    ) -> Version:
        with sqlalchemy.orm.Session(self.engine) as session:
            version, _ = self._read_version(
                version_id, model_id, namespace_id, session
            )
            return version

    def list_versions(self, namespace_id: str, model_id: str) -> List[str]:
        versions: List[str] = []
        with sqlalchemy.orm.Session(self.engine) as session:
            stmt = (
                sqlalchemy.select(DBVersion)
                .where(DBNamespace.name == namespace_id)
                .where(DBModel.name == model_id)
            )
            result = session.execute(stmt)
            for version_obj in result.scalars():
                versions.append(version_obj.name)
        return versions

    def delete_version(
        self, namespace_id: str, model_id: str, version_id: str
    ) -> Version:
        with sqlalchemy.orm.Session(self.engine) as session:
            version, version_obj = self._read_version(
                version_id, model_id, namespace_id, session
            )
            session.delete(version_obj)
            session.commit()
            return version

    def _read_version(
        self,
        version_id: str,
        model_id: str,
        namespace_id: str,
        session: sqlalchemy.orm.Session,
    ) -> Tuple[Version, DBVersion]:
        """Reads the version with the given identifier using the provided session, and returns a Version and DBVersion object."""
        stmt = (
            sqlalchemy.select(DBVersion)
            .where(DBVersion.name == version_id)
            .where(DBModel.name == model_id)
            .where(DBNamespace.name == namespace_id)
        )
        result = session.execute(stmt)

        version_obj = result.scalar()
        if version_obj is None:
            raise errors.ErrorNotFound(
                f"Version with identifier {version_id}  and associated to model {model_id} and namespace {namespace_id} was not found in the artifact store."
            )
        else:
            return (Version(identifier=version_obj.name)), version_obj

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

    def __init__(self, uri: StoreURI, **kwargs) -> None:
        super().__init__(uri=uri)

        self.engine = sqlalchemy.create_engine(uri.uri, **kwargs)
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
