"""
DB utils for getting artifact related data from the DB.
"""

from __future__ import annotations

from typing import Tuple, Union

from sqlalchemy import ScalarResult, select
from sqlalchemy.orm import Session

import mlte.store.error as errors
from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.context.model import Model, Version
from mlte.negotiation.model import DataClassification, ProblemType
from mlte.store.artifact.underlying.rdbs import main_factory
from mlte.store.artifact.underlying.rdbs.card_metadata import (
    DBDataClassification,
    DBNegotiationCard,
    DBProblemType,
)
from mlte.store.artifact.underlying.rdbs.evidence_metadata import DBEvidence
from mlte.store.artifact.underlying.rdbs.main_metadata import (
    DBArtifact,
    DBArtifactType,
    DBModel,
    DBVersion,
)
from mlte.store.artifact.underlying.rdbs.report_metadata import DBReport
from mlte.store.artifact.underlying.rdbs.result_metadata import DBTestResults
from mlte.store.artifact.underlying.rdbs.tests_metadata import DBTestSuite


class DBReader:
    """Class encapsulating functions to read artifact related data from the DB."""

    # Artifact Type - DB Object mapping.
    SUPPORTED_ARTIFACT_DB_CLASSES: dict[
        ArtifactType,
        Union[
            type[DBTestSuite],
            type[DBTestResults],
            type[DBNegotiationCard],
            type[DBReport],
            type[DBEvidence],
        ],
    ] = {
        ArtifactType.TEST_SUITE: DBTestSuite,
        ArtifactType.TEST_RESULTS: DBTestResults,
        ArtifactType.NEGOTIATION_CARD: DBNegotiationCard,
        ArtifactType.REPORT: DBReport,
        ArtifactType.EVIDENCE: DBEvidence,
    }

    @staticmethod
    def get_model(model_id: str, session: Session) -> Tuple[Model, DBModel]:
        """Reads the model with the given identifier using the provided session, and returns a Model and DBModel object."""
        model_obj = session.scalar(
            select(DBModel).where(DBModel.name == model_id)
        )

        if model_obj is None:
            raise errors.ErrorNotFound(
                f"Model with identifier {model_id} was not found in the artifact store."
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

    @staticmethod
    def get_version(
        model_id: str,
        version_id: str,
        session: Session,
    ) -> Tuple[Version, DBVersion]:
        """Reads the version with the given identifier using the provided session, and returns a Version and DBVersion object. Raises ErrorNotFound if not found."""
        version_obj = session.scalar(
            select(DBVersion)
            .where(DBVersion.name == version_id)
            .where(DBVersion.model_id == DBModel.id)
            .where(DBModel.name == model_id)
        )

        if version_obj is None:
            raise errors.ErrorNotFound(
                f"Version with identifier {version_id}  and associated to model {model_id} was not found in the artifact store."
            )
        else:
            return (Version(identifier=version_obj.name)), version_obj

    @staticmethod
    def get_artifact_type(
        type: ArtifactType, session: Session
    ) -> DBArtifactType:
        """Gets the artifact type DB object corresponding to the given internal type."""
        artifact_type_obj = session.scalar(
            select(DBArtifactType).where(DBArtifactType.name == type)
        )

        if artifact_type_obj is None:
            raise Exception(f"Unknown artifact type requested: {type}")
        return artifact_type_obj

    @staticmethod
    def get_artifact(
        model_id: str,
        version_id: str,
        artifact_id: str,
        session: Session,
    ) -> Tuple[
        ArtifactModel,
        Union[
            DBTestSuite, DBTestResults, DBNegotiationCard, DBReport, DBEvidence
        ],
    ]:
        """Reads the artifact with the given identifier using the provided session, and returns an internal object."""
        # First get the class of the artifact we are trying to read, so we can use the ORM by passing the DB object type.
        artifact_header_obj = DBReader.get_artifact_header(artifact_id, session)
        artifact_type = ArtifactType(artifact_header_obj.type.name)

        # Get artifact.
        artifact_class = DBReader.get_artifact_class(artifact_type)
        artifact_obj: Union[
            DBTestSuite, DBTestResults, DBNegotiationCard, DBReport, DBEvidence
        ] = session.scalar(
            select(artifact_class)
            .where(DBVersion.model_id == DBModel.id)
            .where(DBVersion.name == version_id)
            .where(DBModel.name == model_id)
            .where(DBArtifact.id == artifact_class.artifact_id)
            .where(DBArtifact.identifier == artifact_id)
            .where(DBArtifact.version_id == DBVersion.id)
        )

        if artifact_obj is None:
            raise errors.ErrorNotFound(
                f"Artifact with identifier {artifact_id}  and associated to model {model_id}, and version {version_id} was not found in the artifact store."
            )
        else:
            return (
                main_factory.create_artifact_from_db(artifact_header_obj),
                artifact_obj,
            )

    @staticmethod
    def get_artifacts_for_type(
        model_id: str,
        version_id: str,
        artifact_type: ArtifactType,
        session: Session,
    ) -> list[ArtifactModel]:
        """Loads and returns a list with all the artifacts of the given type, for the given model/version."""
        artifact_class = DBReader.get_artifact_class(artifact_type)
        artifact_objs: ScalarResult[
            Union[
                DBTestSuite,
                DBTestResults,
                DBNegotiationCard,
                DBReport,
                DBEvidence,
            ]
        ] = session.scalars(
            (
                select(artifact_class)
                .where(DBVersion.model_id == DBModel.id)
                .where(DBVersion.name == version_id)
                .where(DBModel.name == model_id)
                .where(DBArtifact.id == artifact_class.artifact_id)
                .where(DBArtifact.version_id == DBVersion.id)
            )
        )
        artifacts = []
        for artifact_obj in artifact_objs:
            if artifact_obj.artifact:
                artifact = main_factory.create_artifact_from_db(
                    artifact_obj.artifact
                )
                artifacts.append(artifact)
        return artifacts

    @staticmethod
    def get_artifact_header(artifact_id: str, session: Session) -> DBArtifact:
        """Gets the artifact header object of the artifact identifier provided."""
        artifact_header_obj = session.scalar(
            select(DBArtifact).where(DBArtifact.identifier == artifact_id)
        )
        if artifact_header_obj is None:
            raise errors.ErrorNotFound(
                f"Artifact with identifier {artifact_id} was not found in the artifact store."
            )
        else:
            return artifact_header_obj

    @staticmethod
    def get_artifact_class(
        artifact_type: ArtifactType,
    ) -> Union[
        type[DBTestSuite],
        type[DBTestResults],
        type[DBNegotiationCard],
        type[DBReport],
        type[DBEvidence],
    ]:
        """Gets the DB class of the artifact header provided."""
        if artifact_type in DBReader.SUPPORTED_ARTIFACT_DB_CLASSES:
            return DBReader.SUPPORTED_ARTIFACT_DB_CLASSES[
                ArtifactType(artifact_type)
            ]
        else:
            raise Exception(f"Unsupported artifact type: {artifact_type.value}")

    @staticmethod
    def get_test_suite(
        test_suite_identifier: str, version_id: int, session: Session
    ) -> DBTestSuite:
        """Gets the TestSuit with the given identifier."""
        property_obj = session.scalar(
            select(DBTestSuite)
            .where(DBTestSuite.artifact_id == DBArtifact.id)
            .where(DBArtifact.identifier == test_suite_identifier)
            .where(DBArtifact.version_id == version_id)
        )
        if property_obj is None:
            raise errors.ErrorNotFound(
                f"TestSuite with identifier {test_suite_identifier} was not found in the artifact store."
            )
        else:
            return property_obj

    @staticmethod
    def get_test_results(
        test_results_identifier: str, version_id: int, session: Session
    ) -> DBTestResults:
        """Gets the TestSuite with the given identifier."""
        property_obj = session.scalar(
            select(DBTestResults)
            .where(DBTestResults.artifact_id == DBArtifact.id)
            .where(DBArtifact.identifier == test_results_identifier)
            .where(DBArtifact.version_id == version_id)
        )
        if property_obj is None:
            raise errors.ErrorNotFound(
                f"TestResults with identifier {test_results_identifier} was not found in the artifact store."
            )
        else:
            return property_obj

    @staticmethod
    def get_problem_type(type: ProblemType, session: Session) -> DBProblemType:
        """Gets the problem type DB object corresponding to the given internal type."""
        artifact_type_obj = session.scalar(
            select(DBProblemType).where(DBProblemType.name == type)
        )

        if artifact_type_obj is None:
            raise Exception(f"Unknown problem type requested: {type}")
        return artifact_type_obj

    @staticmethod
    def get_classification_type(
        type: DataClassification, session: Session
    ) -> DBDataClassification:
        """Gets the data classification DB object corresponding to the given internal type."""
        artifact_type_obj = session.scalar(
            select(DBDataClassification).where(
                DBDataClassification.name == type
            )
        )

        if artifact_type_obj is None:
            raise Exception(f"Unknown data classification requested: {type}")
        return artifact_type_obj
