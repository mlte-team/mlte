"""
mlte/store/artifact/underlying/rdbs/store.py

Implementation of relational database system artifact store.
"""

from __future__ import annotations

import typing
from typing import List, Optional

from sqlalchemy import Engine, select
from sqlalchemy.orm import DeclarativeBase, Session

import mlte.store.artifact.util as storeutil
import mlte.store.error as errors
from mlte.artifact.model import ArtifactModel
from mlte.context.model import Model, Version
from mlte.store.artifact.store import ArtifactStore, ArtifactStoreSession
from mlte.store.artifact.underlying.rdbs import main_factory
from mlte.store.artifact.underlying.rdbs.card_metadata import (
    init_classification_types,
    init_problem_types,
)
from mlte.store.artifact.underlying.rdbs.evidence_metadata import (
    init_evidence_types,
)
from mlte.store.artifact.underlying.rdbs.main_metadata import (
    DBBase,
    DBModel,
    DBVersion,
    init_artifact_types,
)
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
        init_evidence_types(session)


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

    def create_model(self, model: Model) -> Model:
        with Session(self.storage.engine) as session:
            try:
                _, _ = DBReader.get_model(model.identifier, session)
                raise errors.ErrorAlreadyExists(
                    f"Model with identifier {model.identifier} already exists."
                )
            except errors.ErrorNotFound:
                # If it was not found, it means we can create it.
                model_orm = DBModel(
                    name=model.identifier,
                    versions=[],
                )
                session.add(model_orm)
                session.commit()
                return Model(identifier=model.identifier, versions=[])

    def read_model(self, model_id: str) -> Model:
        with Session(self.storage.engine) as session:
            model, _ = DBReader.get_model(model_id, session)
            return model

    def list_models(self) -> List[str]:
        models: List[str] = []
        with Session(self.storage.engine) as session:
            model_orms = session.scalars(select(DBModel))
            for model_orm in model_orms:
                models.append(model_orm.name)
        return models

    def delete_model(self, model_id: str) -> Model:
        with Session(self.storage.engine) as session:
            model, model_orm = DBReader.get_model(model_id, session)
            session.delete(model_orm)
            session.commit()
            return model

    def create_version(self, model_id: str, version: Version) -> Version:
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
                _, model_orm = DBReader.get_model(model_id, session)

                # Now create version.
                version_orm = DBVersion(
                    name=version.identifier, model_id=model_orm.id
                )
                session.add(version_orm)
                session.commit()
                return Version(identifier=version.identifier)

    def read_version(self, model_id: str, version_id: str) -> Version:
        with Session(self.storage.engine) as session:
            version, _ = DBReader.get_version(model_id, version_id, session)
            return version

    def list_versions(self, model_id: str) -> List[str]:
        versions: List[str] = []
        with Session(self.storage.engine) as session:
            version_orms = session.scalars(
                (
                    select(DBVersion)
                    .where(DBVersion.model_id == DBModel.id)
                    .where(DBModel.name == model_id)
                )
            )
            for version_orm in version_orms:
                versions.append(version_orm.name)
        return versions

    def delete_version(self, model_id: str, version_id: str) -> Version:
        with Session(self.storage.engine) as session:
            version, version_orm = DBReader.get_version(
                model_id, version_id, session
            )
            session.delete(version_orm)
            session.commit()
            return version

    # -------------------------------------------------------------------------
    # Artifacts
    # -------------------------------------------------------------------------

    def write_artifact(
        self,
        model_id: str,
        version_id: Optional[str],
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
                if version_id:
                    _ = DBReader.get_version(model_id, version_id, session)
                else:
                    _ = DBReader.get_model(model_id, session)
            # Check if artifact already exists.
            try:
                _, artifact_orm = DBReader.get_artifact(
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
                    session.delete(artifact_orm)
            except errors.ErrorNotFound:
                # If artifact was not found, it is ok, force it or not we will create it.
                pass

            # Create the actual object.
            new_artifact_orm = main_factory.create_artifact_orm(
                artifact, model_id, version_id, session
            )

            # Use session to add object.
            session.add(new_artifact_orm)
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
            artifacts = DBReader.get_artifacts(model_id, version_id, session)
            return artifacts[offset : offset + limit]

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
            artifact, artifact_orm = DBReader.get_artifact(
                model_id, version_id, artifact_id, session
            )
            session.delete(artifact_orm)
            session.commit()
            return artifact
