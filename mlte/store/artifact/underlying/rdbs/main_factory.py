"""Creation of metadata objects from pydantic models."""

import typing
from typing import Optional

from sqlalchemy.orm import Session

from mlte.artifact.model import (
    ArtifactHeaderModel,
    ArtifactLevel,
    ArtifactModel,
)
from mlte.artifact.type import ArtifactType
from mlte.evidence.model import EvidenceModel
from mlte.negotiation.model import NegotiationCardModel
from mlte.report.model import ReportModel
from mlte.results.model import TestResultsModel
from mlte.store.artifact.underlying.rdbs import (
    card_factory,
    evidence_factory,
    report_factory,
    result_factory,
    suite_factory,
)
from mlte.store.artifact.underlying.rdbs.card_metadata import DBNegotiationCard
from mlte.store.artifact.underlying.rdbs.evidence_metadata import DBEvidence
from mlte.store.artifact.underlying.rdbs.main_metadata import DBArtifact
from mlte.store.artifact.underlying.rdbs.reader import DBReader
from mlte.store.artifact.underlying.rdbs.report_metadata import DBReport
from mlte.store.artifact.underlying.rdbs.result_metadata import DBTestResults
from mlte.store.artifact.underlying.rdbs.suite_metadata import DBTestSuite
from mlte.suite.model import TestSuiteModel

# -------------------------------------------------------------------------
# DB artifact factory.
# -------------------------------------------------------------------------


def create_artifact_orm(
    artifact: ArtifactModel,
    model_id: str,
    version_id: str,
    level: ArtifactLevel,
    session: Session,
    artifact_orm: Optional[DBArtifact] = None,
) -> typing.Union[DBArtifact]:
    """
    Converts an internal model to its corresponding DB object for artifacts.
    Can edit an existing ORM if provided.
    """
    # Get type and version info from DB.
    artifact_type_orm = DBReader.get_artifact_type(
        artifact.header.type, session
    )
    if level == ArtifactLevel.VERSION:
        _, version_orm = DBReader.get_version(model_id, version_id, session)
        version_orm_id = version_orm.id
        model_orm_id = None
    else:
        _, model_orm = DBReader.get_model(model_id, session)
        model_orm_id = model_orm.id
        version_orm_id = None

    # Create the artifact object, without the specific body.
    if not artifact_orm:
        artifact_orm = DBArtifact(
            identifier=artifact.header.identifier,
            type=artifact_type_orm,
            timestamp=artifact.header.timestamp,
            username=artifact.header.creator,
            level=artifact.header.level,
            version_id=version_orm_id,
            model_id=model_orm_id,
        )
    else:
        # If we are using existing orm, update it.
        artifact_orm.type = artifact_type_orm
        artifact_orm.timestamp = artifact.header.timestamp
        artifact_orm.username = artifact.header.creator
        artifact_orm.level = artifact.header.level
        artifact_orm.version_id = version_orm_id
        artifact_orm.model_id = model_orm_id

    # Create the body ORM object and return it.
    if artifact.header.type == ArtifactType.NEGOTIATION_CARD:
        card = typing.cast(NegotiationCardModel, artifact.body)
        artifact_orm.body_negotiation_card = card_factory.create_card_orm(
            card, session
        )
    elif artifact.header.type == ArtifactType.TEST_SUITE:
        test_suite = typing.cast(TestSuiteModel, artifact.body)
        artifact_orm.body_test_suite = suite_factory.create_suite_orm(
            test_suite
        )
    elif artifact.header.type == ArtifactType.EVIDENCE:
        value = typing.cast(EvidenceModel, artifact.body)
        artifact_orm.body_evidence = evidence_factory.create_evidence_orm(value)
    elif artifact.header.type == ArtifactType.TEST_RESULTS:
        test_results = typing.cast(TestResultsModel, artifact.body)
        artifact_orm.body_test_results = result_factory.create_results_orm(
            test_results
        )
    elif artifact.header.type == ArtifactType.REPORT:
        report = typing.cast(ReportModel, artifact.body)
        artifact_orm.body_report = report_factory.create_report_orm(
            report, session
        )
    else:
        raise Exception(
            f"Unsupported artifact type for conversion: {artifact.header.type}"
        )

    return artifact_orm


# -------------------------------------------------------------------------
# Artifact model factory.
# -------------------------------------------------------------------------


def create_artifact_model(artifact_orm: DBArtifact) -> ArtifactModel:
    """
    Creates an Artifact model from the corresponding DB object and DB header.

    :param artifact_orm: A DBArtifactHeader object from the DB with header info.
    :return: the DB data converted into an ArtifactModel.
    """
    artifact_header = ArtifactHeaderModel(
        identifier=artifact_orm.identifier,
        type=ArtifactType(artifact_orm.type.name),
        level=ArtifactLevel(artifact_orm.level),
        timestamp=artifact_orm.timestamp,
        creator=artifact_orm.username,
    )

    # Create the body for the artifact from the ORM DB data.
    body: typing.Union[
        TestSuiteModel,
        TestResultsModel,
        NegotiationCardModel,
        ReportModel,
        EvidenceModel,
    ]
    if artifact_header.type == ArtifactType.NEGOTIATION_CARD:
        card_orm = typing.cast(
            DBNegotiationCard, artifact_orm.body_negotiation_card
        )
        body = card_factory.create_card_model(card_orm)
    elif artifact_header.type == ArtifactType.TEST_SUITE:
        suite_orm = typing.cast(DBTestSuite, artifact_orm.body_test_suite)
        body = suite_factory.create_suite_model(suite_orm)
    elif artifact_header.type == ArtifactType.EVIDENCE:
        evidence_orm = typing.cast(DBEvidence, artifact_orm.body_evidence)
        body = evidence_factory.create_evidence_model(evidence_orm)
    elif artifact_header.type == ArtifactType.TEST_RESULTS:
        results_orm = typing.cast(DBTestResults, artifact_orm.body_test_results)
        body = result_factory.create_results_model(results_orm)
    elif artifact_header.type == ArtifactType.REPORT:
        report_orm = typing.cast(DBReport, artifact_orm.body_report)
        body = report_factory.create_report_model(report_orm)
    else:
        raise Exception(
            f"Unsupported artifact type for conversion: {artifact_header.type}"
        )

    return ArtifactModel(header=artifact_header, body=body)
