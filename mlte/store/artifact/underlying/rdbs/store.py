"""
mlte/store/artifact/underlying/rdbs/store.py

Implementation of relational database system artifact store.
"""
from __future__ import annotations

from typing import List

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy_utils
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

import mlte.store.artifact.util as storeutil
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
from mlte.store.artifact.underlying.rdbs import factory
from mlte.store.artifact.underlying.rdbs.metadata import (
    DBBase,
    DBModel,
    DBNamespace,
    DBVersion,
    init_artifact_types,
)
from mlte.store.artifact.underlying.rdbs.metadata_nc import (
    init_classification_types,
    init_problem_types,
)
from mlte.store.artifact.underlying.rdbs.metadata_value import init_value_types
from mlte.store.artifact.underlying.rdbs.reader import DBReader
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
        DBBase.metadata.create_all(self.engine)

    def _init_tables(self):
        """Pre-populate tables."""

        # Pre-populate artifact types.
        with Session(self.engine) as session:
            init_artifact_types(session)
            init_problem_types(session)
            init_classification_types(session)
            init_value_types(session)


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
                _, _ = DBReader.get_namespace(namespace.identifier, session)
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
            namespace, _ = DBReader.get_namespace(namespace_id, session)
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
            namespace, namespace_obj = DBReader.get_namespace(
                namespace_id, session
            )
            session.delete(namespace_obj)
            session.commit()
            return namespace

    def create_model(self, namespace_id: str, model: ModelCreate) -> Model:
        with Session(self.engine) as session:
            try:
                _, _ = DBReader.get_model(
                    namespace_id, model.identifier, session
                )
                raise errors.ErrorAlreadyExists(
                    f"Model with identifier {model.identifier} in namespace {namespace_id} already exists."
                )
            except errors.ErrorNotFound:
                # Check if namespace exists.
                _, namespace_obj = DBReader.get_namespace(namespace_id, session)

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
            model, _ = DBReader.get_model(namespace_id, model_id, session)
            return model

    def list_models(self, namespace_id: str) -> List[str]:
        models: List[str] = []
        with Session(self.engine) as session:
            model_objs = session.scalars(
                select(DBModel)
                .where(DBNamespace.name == namespace_id)
                .where(DBModel.namespace_id == DBNamespace.id)
            )
            for model_obj in model_objs:
                models.append(model_obj.name)
        return models

    def delete_model(self, namespace_id: str, model_id: str) -> Model:
        with Session(self.engine) as session:
            model, model_obj = DBReader.get_model(
                namespace_id, model_id, session
            )
            session.delete(model_obj)
            session.commit()
            return model

    def create_version(
        self, namespace_id: str, model_id: str, version: VersionCreate
    ) -> Version:
        with Session(self.engine) as session:
            try:
                _, _ = DBReader.get_version(
                    namespace_id, model_id, version.identifier, session
                )
                raise errors.ErrorAlreadyExists(
                    f"Version with identifier {version.identifier} for model {model_id} in namespace {namespace_id} already exists."
                )
            except errors.ErrorNotFound:
                # Check if namespace and model exist.
                _, _ = DBReader.get_namespace(namespace_id, session)
                _, model_obj = DBReader.get_model(
                    namespace_id, model_id, session
                )

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
            version, _ = DBReader.get_version(
                namespace_id, model_id, version_id, session
            )
            return version

    def list_versions(self, namespace_id: str, model_id: str) -> List[str]:
        versions: List[str] = []
        with Session(self.engine) as session:
            version_objs = session.scalars(
                (
                    select(DBVersion)
                    .where(DBVersion.model_id == DBModel.id)
                    .where(DBModel.namespace_id == DBNamespace.id)
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
            version, version_obj = DBReader.get_version(
                namespace_id, model_id, version_id, session
            )
            session.delete(version_obj)
            session.commit()
            return version

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
                storeutil.create_parents(
                    self, namespace_id, model_id, version_id
                )
            else:
                # Ensure parents exist.
                _ = DBReader.get_version(
                    namespace_id, model_id, version_id, session
                )

            # Check if artifact already exists.
            try:
                artifact, artifact_obj = DBReader.get_artifact(
                    namespace_id,
                    model_id,
                    version_id,
                    artifact.header.identifier,
                    session,
                )
                if not force:
                    raise errors.ErrorAlreadyExists(
                        f"Artifact '{artifact.header.identifier}' already exists."
                    )
                else:
                    # We have no edit functionality, nor any versioning system, so delete the previous version.
                    # TODO: versioning? Keep previous versions?
                    session.delete(artifact_obj)
            except errors.ErrorNotFound:
                # If artifact was not found, it is ok, force it or not we will create it.
                pass

            # Get type and parent version info.
            artifact_type_obj = DBReader.get_artifact_type(
                artifact.header.type, session
            )
            _, version_obj = DBReader.get_version(
                namespace_id, model_id, version_id, session
            )

            # Create the actual object.
            new_artifact_obj = factory.create_db_artifact(
                artifact, artifact_type_obj, version_obj.id, session
            )

            # Use session to add object.
            session.add(new_artifact_obj)
            session.commit()
            return artifact

    def read_artifact(
        self,
        namespace_id: str,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> ArtifactModel:
        with Session(self.engine) as session:
            artifact, _ = DBReader.get_artifact(
                namespace_id, model_id, version_id, artifact_id, session
            )
            return artifact

    def read_artifacts(
        self,
        namespace_id: str,
        model_id: str,
        version_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ArtifactModel]:
        # TODO: support for limit and offset.
        with Session(self.engine) as session:
            all_artifacts = []
            for artifact_type in DBReader.SUPPORTED_ARTIFACT_DB_CLASSES.keys():
                artifacts = DBReader.get_artifacts_for_type(
                    namespace_id, model_id, version_id, artifact_type, session
                )
                all_artifacts.extend(artifacts)
            return all_artifacts

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
        with Session(self.engine) as session:
            artifact, artifact_obj = DBReader.get_artifact(
                namespace_id, model_id, version_id, artifact_id, session
            )
            session.delete(artifact_obj)
            session.commit()
            return artifact
