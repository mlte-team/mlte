"""
DB utils for getting artifact related data from the DB.
"""

from __future__ import annotations

from typing import Optional

from sqlalchemy import ScalarResult, Select, select
from sqlalchemy.orm import Session

import mlte.store.error as errors
from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.context.model import Model, Version
from mlte.negotiation.model import DataClassification, ProblemType
from mlte.store.artifact.underlying.rdbs import main_factory
from mlte.store.artifact.underlying.rdbs.card_metadata import (
    DBDataClassification,
    DBProblemType,
)
from mlte.store.artifact.underlying.rdbs.main_metadata import (
    DBArtifact,
    DBArtifactType,
    DBModel,
    DBVersion,
)


class DBReader:
    """Class encapsulating functions to read artifact related data from the DB."""

    @staticmethod
    def get_model(model_id: str, session: Session) -> tuple[Model, DBModel]:
        """Reads the model with the given identifier using the provided session, and returns a Model and DBModel object."""
        model_orm = session.scalar(
            select(DBModel).where(DBModel.name == model_id)
        )

        if model_orm is None:
            raise errors.ErrorNotFound(
                f"Model with identifier {model_id} was not found in the artifact store."
            )
        else:
            return (
                Model(
                    identifier=model_orm.name,
                    versions=[
                        Version(identifier=version_orm.name)
                        for version_orm in model_orm.versions
                    ],
                ),
                model_orm,
            )

    @staticmethod
    def get_version(
        model_id: str,
        version_id: str,
        session: Session,
    ) -> tuple[Version, DBVersion]:
        """Reads the version with the given identifier using the provided session, and returns a Version and DBVersion object. Raises ErrorNotFound if not found."""
        version_orm = session.scalar(
            select(DBVersion)
            .where(DBVersion.name == version_id)
            .where(DBVersion.model_id == DBModel.id)
            .where(DBModel.name == model_id)
        )

        if version_orm is None:
            raise errors.ErrorNotFound(
                f"Version with identifier {version_id}  and associated to model {model_id} was not found in the artifact store."
            )
        else:
            return (Version(identifier=version_orm.name)), version_orm

    @staticmethod
    def get_artifact_type(
        type: ArtifactType, session: Session
    ) -> DBArtifactType:
        """Gets the artifact type DB object corresponding to the given internal type."""
        artifact_type_orm = session.scalar(
            select(DBArtifactType).where(DBArtifactType.name == type)
        )

        if artifact_type_orm is None:
            raise Exception(f"Unknown artifact type requested: {type}")
        return artifact_type_orm

    @staticmethod
    def _get_model_level_artifacts_stmt(
        model_id: str,
    ) -> Select[tuple[DBArtifact]]:
        """General statement to get artifacts stored at a model level."""
        return (
            select(DBArtifact)
            .where(DBArtifact.model_id == DBModel.id)
            .where(DBModel.name == model_id)
            .where(DBArtifact.version_id.is_(None))
        )

    @staticmethod
    def _get_version_artifacts_stmt(
        model_id: str,
        version_id: str,
    ) -> Select[tuple[DBArtifact]]:
        """General statement to get artifacts stored at a model and version level."""
        return (
            select(DBArtifact)
            .where(DBArtifact.version_id == DBVersion.id)
            .where(DBVersion.name == version_id)
            .where(DBVersion.model_id == DBModel.id)
            .where(DBModel.name == model_id)
        )

    @staticmethod
    def get_artifact(
        model_id: str,
        version_id: str,
        artifact_id: str,
        session: Session,
    ) -> tuple[ArtifactModel, DBArtifact]:
        """Reads the artifact with the given identifier using the provided session, and returns an internal object."""
        select_stmt = DBReader._get_version_artifacts_stmt(model_id, version_id)
        select_stmt = select_stmt.where(DBArtifact.identifier == artifact_id)
        artifact_orm: Optional[DBArtifact] = session.scalar(select_stmt)

        if artifact_orm is None:
            # Try at model level.
            select_stmt = DBReader._get_model_level_artifacts_stmt(model_id)
            select_stmt = select_stmt.where(
                DBArtifact.identifier == artifact_id
            )
            artifact_orm = session.scalar(select_stmt)

            if artifact_orm is None:
                raise errors.ErrorNotFound(
                    f"Artifact with identifier {artifact_id}  and associated to model {model_id}, and version {version_id} was not found in the artifact store."
                )

        return (
            main_factory.create_artifact_model(artifact_orm),
            artifact_orm,
        )

    @staticmethod
    def get_artifacts(
        model_id: str,
        version_id: str,
        session: Session,
    ) -> list[ArtifactModel]:
        """Loads and returns a list with all the artifacts, for the given model/version."""
        select_stmt = DBReader._get_version_artifacts_stmt(model_id, version_id)
        artifact_models = DBReader._load_artifact_models(select_stmt, session)

        # Also get model level artifacts.
        select_stmt = DBReader._get_model_level_artifacts_stmt(model_id)
        artifact_models.extend(
            DBReader._load_artifact_models(select_stmt, session)
        )

        return artifact_models

    @staticmethod
    def _load_artifact_models(
        select_stmt: Select[tuple[DBArtifact]], session: Session
    ) -> list[ArtifactModel]:
        """Load the artifacts obtained from the given statement into a list as ArtifactModels."""
        artifact_orms: ScalarResult[DBArtifact] = session.scalars(select_stmt)
        artifact_models: list[ArtifactModel] = []
        for artifact_orm in artifact_orms:
            artifact_model = main_factory.create_artifact_model(artifact_orm)
            artifact_models.append(artifact_model)

        return artifact_models

    @staticmethod
    def get_problem_type(type: ProblemType, session: Session) -> DBProblemType:
        """Gets the problem type DB object corresponding to the given internal type."""
        artifact_type_orm = session.scalar(
            select(DBProblemType).where(DBProblemType.name == type)
        )

        if artifact_type_orm is None:
            raise Exception(f"Unknown problem type requested: {type}")
        return artifact_type_orm

    @staticmethod
    def get_classification_type(
        type: DataClassification, session: Session
    ) -> DBDataClassification:
        """Gets the data classification DB object corresponding to the given internal type."""
        artifact_type_orm = session.scalar(
            select(DBDataClassification).where(
                DBDataClassification.name == type
            )
        )

        if artifact_type_orm is None:
            raise Exception(f"Unknown data classification requested: {type}")
        return artifact_type_orm
