"""Implementation of relational database system artifact store."""

from __future__ import annotations

import typing
from typing import Any, Optional

from sqlalchemy import Engine, select
from sqlalchemy.orm import DeclarativeBase, Session

import mlte.store.error as errors
from mlte.artifact.model import ArtifactModel
from mlte.context.model import Model, Version
from mlte.store.artifact.store import ArtifactStore
from mlte.store.artifact.store_session import (
    ArtifactMapper,
    ArtifactStoreSession,
    ModelMapper,
    VersionMapper,
)
from mlte.store.artifact.underlying.rdbs import main_factory
from mlte.store.artifact.underlying.rdbs.card_metadata import (
    init_classification_types,
    init_problem_types,
)
from mlte.store.artifact.underlying.rdbs.evidence_metadata import (
    init_evidence_types,
)
from mlte.store.artifact.underlying.rdbs.main_metadata import (
    DBArtifact,
    DBBase,
    DBModel,
    DBVersion,
    init_artifact_types,
)
from mlte.store.artifact.underlying.rdbs.reader import DBReader
from mlte.store.common.rdbs_storage import RDBStorage
from mlte.store.validators.cross_validator import CompositeValidator

# -----------------------------------------------------------------------------
# RelationalDBArtifactStore
# -----------------------------------------------------------------------------


class RelationalDBArtifactStore(ArtifactStore):
    """A DB implementation of the MLTE artifact store."""

    def __init__(self, uri, **kwargs):
        super().__init__(uri=uri)

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
        return RelationalDBArtifactStoreSession(
            storage=self.storage, validators=self.validators
        )


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

    def __init__(
        self, storage: RDBStorage, validators: CompositeValidator
    ) -> None:
        self.storage = storage
        """A reference to underlying storage."""

        self.version_mapper = RDBSVersionMapper(storage=storage)
        """The mapper to version CRUD."""

        self.model_mapper = RDBSModelMapper(storage=storage)
        """The mapper to model CRUD."""

        self.artifact_mapper = RDBSArtifactMapper(
            storage=storage, validators=validators
        )
        """The mapper to artifact CRUD."""

    def close(self) -> None:
        """Close the session."""
        self.storage.close()


# -------------------------------------------------------------------------
# Structural Elements
# -------------------------------------------------------------------------


class RDBSModelMapper(ModelMapper):
    """In-memory mapper for the model resource."""

    def __init__(self, storage: RDBStorage) -> None:
        self.storage = storage
        """A reference to underlying storage."""

    def create(self, model: Model, context: Any = None) -> Model:
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

    def read(self, model_id: str, context: Any = None) -> Model:
        with Session(self.storage.engine) as session:
            model, _ = DBReader.get_model(model_id, session)
            return model

    def list(self, context: Any = None) -> list[str]:
        models: list[str] = []
        with Session(self.storage.engine) as session:
            model_orms = session.scalars(select(DBModel))
            for model_orm in model_orms:
                models.append(model_orm.name)
        return models

    def delete(self, model_id: str, context: Any = None) -> Model:
        with Session(self.storage.engine) as session:
            model, model_orm = DBReader.get_model(model_id, session)
            session.delete(model_orm)
            session.commit()
            return model


class RDBSVersionMapper(VersionMapper):
    """In-memory mapper for the version resource."""

    def __init__(self, storage: RDBStorage) -> None:
        self.storage = storage
        """A reference to underlying storage."""

    def create(self, version: Version, model_id: str) -> Version:
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

    def read(self, version_id: str, model_id: str) -> Version:
        with Session(self.storage.engine) as session:
            version, _ = DBReader.get_version(model_id, version_id, session)
            return version

    def list(self, model_id: str) -> list[str]:
        versions: list[str] = []
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

    def delete(self, version_id: str, model_id: str) -> Version:
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


class RDBSArtifactMapper(ArtifactMapper):
    """In-memory mapper for the version resource."""

    def __init__(
        self, storage: RDBStorage, validators: CompositeValidator
    ) -> None:
        super().__init__(validators=validators)

        self.storage = storage
        """A reference to underlying storage."""

    def read(
        self, artifact_id: str, model_and_version: tuple[str, str]
    ) -> ArtifactModel:
        model_id, version_id = model_and_version
        with Session(self.storage.engine) as session:
            artifact, _ = DBReader.get_artifact(
                model_id, version_id, artifact_id, session
            )
            return artifact

    def delete(
        self, artifact_id: str, model_and_version: tuple[str, str]
    ) -> ArtifactModel:
        model_id, version_id = model_and_version
        with Session(self.storage.engine) as session:
            artifact, artifact_orm = DBReader.get_artifact(
                model_id, version_id, artifact_id, session
            )
            session.delete(artifact_orm)
            session.commit()
            return artifact

    def list(self, model_and_version: tuple[str, str]) -> list[str]:
        model_id, version_id = model_and_version
        with Session(self.storage.engine) as session:
            artifacts = DBReader.get_artifacts(model_id, version_id, session)
            return [artifact.header.identifier for artifact in artifacts]

    # -------------------------------------------------------------------------
    # Internal helpers.
    # -------------------------------------------------------------------------

    def _read_artifact(
        self, artifact_id: str, model_and_version: tuple[str, str]
    ) -> tuple[ArtifactModel, DBArtifact]:
        """
        Looks for an artifact in the DB store, returns it as a model and as an ORM object,
        or throws an ErrorNotFound if not present.
        """
        model_id, version_id = model_and_version
        with Session(self.storage.engine) as session:
            artifact, artifact_orm = DBReader.get_artifact(
                model_id, version_id, artifact_id, session
            )
            return artifact, artifact_orm

    def _store_artifact(
        self,
        artifact: ArtifactModel,
        model_and_version: tuple[str, str],
    ):
        """Writes an artifact to the store."""
        model_id, version_id = model_and_version
        original_orm: Optional[DBArtifact] = None
        try:
            _, original_orm = self._read_artifact(
                artifact.header.identifier, model_and_version
            )
        except errors.ErrorNotFound:
            # It is ok if we don't find it, we will just create it instead of editing.
            pass

        with Session(self.storage.engine) as session:
            # To simulate edition, we delete the current object and create a new one.
            # TODO: Change this so we are actually editing the object in the DB.
            if original_orm:
                session.delete(original_orm)
            updated_orm = main_factory.create_artifact_orm(
                artifact,
                model_id,
                version_id,
                artifact.header.level,
                session,
            )
            session.add(updated_orm)

            # Create or edit changes in DB.
            session.commit()

        return self.read(artifact.header.identifier, model_and_version)
