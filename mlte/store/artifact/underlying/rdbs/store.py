"""
mlte/store/artifact/underlying/rdbs/store.py

Implementation of relational database system artifact store.
"""
from __future__ import annotations

from typing import List, Tuple

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy_utils
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

import mlte.store.error as errors
from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
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
from mlte.store.artifact.underlying.rdbs import factory
from mlte.store.artifact.underlying.rdbs.metadata import (
    Base,
    DBArtifactType,
    DBModel,
    DBNamespace,
    DBVersion,
)
from mlte.store.base import StoreURI

# -----------------------------------------------------------------------------
# RelationalDBStore
# -----------------------------------------------------------------------------


class RelationalDBStore(ArtifactStore):
    """A DB implementation of the MLTE artifact store."""

    def __init__(self, uri: StoreURI, **kwargs) -> None:
        super().__init__(uri=uri)

        self.engine = sqlalchemy.create_engine(uri.uri, **kwargs)
        """The underlying storage for the store."""

        # Create the DB if it doesn't exist already.
        if not sqlalchemy_utils.database_exists(self.engine.url):
            sqlalchemy_utils.create_database(self.engine.url)

        # Creates the DB items if they don't exist already.
        self._create_tables()
        self._init_tables()

    def session(self) -> RelationalDBStoreSession:  # type: ignore[override]
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return RelationalDBStoreSession(engine=self.engine)

    def _create_tables(self):
        """Creates all items, if they don't exist already."""
        Base.metadata.create_all(self.engine)

    def _init_tables(self):
        """Pre-populate tables."""

        # Pre-populate artifact types.
        with Session(self.engine) as session:
            if session.scalars(select(DBArtifactType)).first() is None:
                types = [e.value for e in ArtifactType]
                for type in types:
                    type_obj = DBArtifactType(name=type)
                    session.add(type_obj)
                session.commit()


# -----------------------------------------------------------------------------
# RelationalDatabaseStoreSession
# -----------------------------------------------------------------------------


class RelationalDBStoreSession(ArtifactStoreSession):
    """A relational DB implementation of the MLTE artifact store session."""

    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        """A reference to underlying storage."""

    def close(self) -> None:
        """Close the session."""
        self.engine.dispose()

    # -------------------------------------------------------------------------
    # Structural Elements
    # -------------------------------------------------------------------------

    def create_namespace(self, namespace: NamespaceCreate) -> Namespace:
        with Session(self.engine) as session:
            try:
                _, _ = self._read_namespace(namespace.identifier, session)
                raise errors.ErrorAlreadyExists(
                    f"Namespace with identifier {namespace.identifier} already exists."
                )
            except errors.ErrorNotFound:
                # If it was not found, it means we can create it.
                namespace_obj = DBNamespace(
                    name=namespace.identifier, models=[]
                )
                session.add(namespace_obj)
                session.commit()
                return Namespace(identifier=namespace.identifier, models=[])

    def read_namespace(self, namespace_id: str) -> Namespace:
        with Session(self.engine) as session:
            namespace, _ = self._read_namespace(namespace_id, session)
            return namespace

    def list_namespaces(self) -> List[str]:
        namespaces: List[str] = []
        with Session(self.engine) as session:
            namespace_objs = session.scalars(select(DBNamespace))
            for namespace_obj in namespace_objs:
                namespaces.append(namespace_obj.name)
        return namespaces

    def delete_namespace(self, namespace_id: str) -> Namespace:
        with Session(self.engine) as session:
            namespace, namespace_obj = self._read_namespace(
                namespace_id, session
            )
            session.delete(namespace_obj)
            session.commit()
            return namespace

    def create_model(self, namespace_id: str, model: ModelCreate) -> Model:
        with Session(self.engine) as session:
            try:
                _, _ = self._read_model(model.identifier, namespace_id, session)
                raise errors.ErrorAlreadyExists(
                    f"Model with identifier {model.identifier} in namespace {namespace_id} already exists."
                )
            except errors.ErrorNotFound:
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
        with Session(self.engine) as session:
            model, _ = self._read_model(model_id, namespace_id, session)
            return model

    def list_models(self, namespace_id: str) -> List[str]:
        models: List[str] = []
        with Session(self.engine) as session:
            model_objs = session.scalars(
                select(DBModel).where(DBNamespace.name == namespace_id)
            )
            for model_obj in model_objs:
                models.append(model_obj.name)
        return models

    def delete_model(self, namespace_id: str, model_id: str) -> Model:
        with Session(self.engine) as session:
            model, model_obj = self._read_model(model_id, namespace_id, session)
            session.delete(model_obj)
            session.commit()
            return model

    def create_version(
        self, namespace_id: str, model_id: str, version: VersionCreate
    ) -> Version:
        with Session(self.engine) as session:
            try:
                _, _ = self._read_version(
                    version.identifier, model_id, namespace_id, session
                )
                raise errors.ErrorAlreadyExists(
                    f"Version with identifier {version.identifier} for model {model_id} in namespace {namespace_id} already exists."
                )
            except errors.ErrorNotFound:
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
        with Session(self.engine) as session:
            version, _ = self._read_version(
                version_id, model_id, namespace_id, session
            )
            return version

    def list_versions(self, namespace_id: str, model_id: str) -> List[str]:
        versions: List[str] = []
        with Session(self.engine) as session:
            version_objs = session.scalars(
                (
                    select(DBVersion)
                    .where(DBNamespace.name == namespace_id)
                    .where(DBModel.name == model_id)
                )
            )
            for version_obj in version_objs:
                versions.append(version_obj.name)
        return versions

    def delete_version(
        self, namespace_id: str, model_id: str, version_id: str
    ) -> Version:
        with Session(self.engine) as session:
            version, version_obj = self._read_version(
                version_id, model_id, namespace_id, session
            )
            session.delete(version_obj)
            session.commit()
            return version

    def _read_namespace(
        self, namespace_id: str, session: Session
    ) -> Tuple[Namespace, DBNamespace]:
        """Reads the namespace with the given identifier using the provided session, and returns a Namespace and DBNamespace object."""
        namespace_obj = session.scalar(
            select(DBNamespace).where(DBNamespace.name == namespace_id)
        )
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

    def _read_model(
        self, model_id: str, namespace_id: str, session: Session
    ) -> Tuple[Model, DBModel]:
        """Reads the model with the given identifier using the provided session, and returns a Model and DBModel object."""
        model_obj = session.scalar(
            select(DBModel)
            .where(DBModel.name == model_id)
            .where(DBNamespace.name == namespace_id)
        )

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

    def _read_version(
        self,
        version_id: str,
        model_id: str,
        namespace_id: str,
        session: Session,
    ) -> Tuple[Version, DBVersion]:
        """Reads the version with the given identifier using the provided session, and returns a Version and DBVersion object."""
        version_obj = session.scalar(
            select(DBVersion)
            .where(DBVersion.name == version_id)
            .where(DBModel.name == model_id)
            .where(DBNamespace.name == namespace_id)
        )

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
        with Session(self.engine) as session:
            if parents:
                pass
                # TODO: create parents
                # storeutil.create_parents(self, namespace_id, model_id, version_id)

            # TODO: check already exists
            #        artifacts = self._get_version_artifacts(
            #            namespace_id, model_id, version_id
            #        )
            #        if artifact.header.identifier in artifacts and not force:
            #            raise errors.ErrorAlreadyExists(
            #                f"Artifact '{artifact.header.identifier}'"
            #            )
            artifact_type_obj = self._read_artifact_type(
                artifact.header.type, session
            )
            artifact_obj = factory.create_db_artifact(
                artifact, artifact_type_obj
            )
            session.add(artifact_obj)
            session.commit()
            return artifact

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

    def _read_artifact_type(
        self, type: ArtifactType, session: Session
    ) -> DBArtifactType:
        """Gets the artifact type DB object corresponding to the given internal type."""
        artifact_type_obj = session.scalar(
            select(DBArtifactType).where(DBArtifactType.name == type)
        )

        if artifact_type_obj is None:
            raise Exception(f"Unknown artifact type requested: {type}")
        return artifact_type_obj
