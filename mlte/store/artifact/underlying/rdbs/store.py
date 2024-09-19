"""
mlte/store/artifact/underlying/rdbs/store.py

Implementation of relational database system artifact store.
"""
from __future__ import annotations

import typing
from typing import List

from sqlalchemy import Engine, select
from sqlalchemy.orm import DeclarativeBase, Session

import mlte.store.artifact.util as storeutil
import mlte.store.error as errors
from mlte.artifact.model import ArtifactModel
from mlte.context.model import Model, ModelCreate, Version, VersionCreate
from mlte.store.artifact.store import ArtifactStore, ArtifactStoreSession
from mlte.store.artifact.underlying.rdbs import factory
from mlte.store.artifact.underlying.rdbs.metadata import (
    DBBase,
    DBModel,
    DBVersion,
    init_artifact_types,
)
from mlte.store.artifact.underlying.rdbs.metadata_nc import (
    init_classification_types,
    init_problem_types,
)
from mlte.store.artifact.underlying.rdbs.metadata_value import init_value_types
from mlte.store.artifact.underlying.rdbs.reader import DBReader
from mlte.store.common.rdbs_storage import RDBStorage
from mlte.store.query import Query

# -----------------------------------------------------------------------------
# RelationalDBArtifactStore
# -----------------------------------------------------------------------------


class RelationalDBArtifactStore(ArtifactStore):
    """A DB implementation of the MLTE artifact store."""

    def __init__(self, uri, **kwargs):
        ArtifactStore.__init__(self, uri=uri)

        self.storage = RDBStorage(
            uri,
            base_class=typing.cast(DeclarativeBase, DBBase),
            init_tables_func=init_artifact_store_tables,
            **kwargs,
        )
        """The relational DB storage."""

    def session(self) -> RelationalDBArtifactStoreSession:
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return RelationalDBArtifactStoreSession(storage=self.storage)


def init_artifact_store_tables(engine: Engine):
    """Pre-populate tables."""
    with Session(engine) as session:
        init_artifact_types(session)
        init_problem_types(session)
        init_classification_types(session)
        init_value_types(session)


# -----------------------------------------------------------------------------
# RelationalDBArtifactStoreSession
# -----------------------------------------------------------------------------


class RelationalDBArtifactStoreSession(ArtifactStoreSession):
    """A relational DB implementation of the MLTE artifact store session."""

    def __init__(self, storage: RDBStorage) -> None:
        self.storage = storage
        """A reference to underlying storage."""

    def close(self) -> None:
        """Close the session."""
        self.storage.close()

    # -------------------------------------------------------------------------
    # Structural Elements
    # -------------------------------------------------------------------------

    def create_model(self, model: ModelCreate) -> Model:
        with Session(self.storage.engine) as session:
            try:
                _, _ = DBReader.get_model(model.identifier, session)
                raise errors.ErrorAlreadyExists(
                    f"Model with identifier {model.identifier} already exists."
                )
            except errors.ErrorNotFound:
                # If it was not found, it means we can create it.
                model_obj = DBModel(
                    name=model.identifier,
                    versions=[],
                )
                session.add(model_obj)
                session.commit()
                return Model(identifier=model.identifier, versions=[])

    def read_model(self, model_id: str) -> Model:
        with Session(self.storage.engine) as session:
            model, _ = DBReader.get_model(model_id, session)
            return model

    def list_models(self) -> List[str]:
        models: List[str] = []
        with Session(self.storage.engine) as session:
            model_objs = session.scalars(select(DBModel))
            for model_obj in model_objs:
                models.append(model_obj.name)
        return models

    def delete_model(self, model_id: str) -> Model:
        with Session(self.storage.engine) as session:
            model, model_obj = DBReader.get_model(model_id, session)
            session.delete(model_obj)
            session.commit()
            return model

    def create_version(self, model_id: str, version: VersionCreate) -> Version:
        with Session(self.storage.engine) as session:
            try:
                _, _ = DBReader.get_version(
                    model_id, version.identifier, session
                )
                raise errors.ErrorAlreadyExists(
                    f"Version with identifier {version.identifier} for model {model_id} already exists."
                )
            except errors.ErrorNotFound:
                # Check if model exists.
                _, model_obj = DBReader.get_model(model_id, session)

                # Now create version.
                version_obj = DBVersion(
                    name=version.identifier, model_id=model_obj.id
                )
                session.add(version_obj)
                session.commit()
                return Version(identifier=version.identifier)

    def read_version(self, model_id: str, version_id: str) -> Version:
        with Session(self.storage.engine) as session:
            version, _ = DBReader.get_version(model_id, version_id, session)
            return version

    def list_versions(self, model_id: str) -> List[str]:
        versions: List[str] = []
        with Session(self.storage.engine) as session:
            version_objs = session.scalars(
                (
                    select(DBVersion)
                    .where(DBVersion.model_id == DBModel.id)
                    .where(DBModel.name == model_id)
                )
            )
            for version_obj in version_objs:
                versions.append(version_obj.name)
        return versions

    def delete_version(self, model_id: str, version_id: str) -> Version:
        with Session(self.storage.engine) as session:
            version, version_obj = DBReader.get_version(
                model_id, version_id, session
            )
            session.delete(version_obj)
            session.commit()
            return version

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
        with Session(self.storage.engine) as session:
            if parents:
                storeutil.create_parents(self, model_id, version_id)
            else:
                # Ensure parents exist.
                _ = DBReader.get_version(model_id, version_id, session)

            # Check if artifact already exists.
            try:
                _, artifact_obj = DBReader.get_artifact(
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
            _, version_obj = DBReader.get_version(model_id, version_id, session)

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
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> ArtifactModel:
        with Session(self.storage.engine) as session:
            artifact, _ = DBReader.get_artifact(
                model_id, version_id, artifact_id, session
            )
            return artifact

    def read_artifacts(
        self,
        model_id: str,
        version_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ArtifactModel]:
        # TODO: not the best support of offset and limit, still loading everything from DB.
        with Session(self.storage.engine) as session:
            all_artifacts = []
            for artifact_type in DBReader.SUPPORTED_ARTIFACT_DB_CLASSES.keys():
                artifacts = DBReader.get_artifacts_for_type(
                    model_id, version_id, artifact_type, session
                )
                all_artifacts.extend(artifacts)
            return all_artifacts[offset : offset + limit]

    def search_artifacts(
        self,
        model_id: str,
        version_id: str,
        query: Query = Query(),
    ) -> List[ArtifactModel]:
        # TODO: not the most efficient way, since it loads all artifacts first, before filtering.
        artifacts = self.read_artifacts(model_id, version_id)
        return [
            artifact for artifact in artifacts if query.filter.match(artifact)
        ]

    def delete_artifact(
        self,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> ArtifactModel:
        with Session(self.storage.engine) as session:
            artifact, artifact_obj = DBReader.get_artifact(
                model_id, version_id, artifact_id, session
            )
            session.delete(artifact_obj)
            session.commit()
            return artifact
