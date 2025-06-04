"""Creation of metadata objects from pydantic models."""

import typing

from sqlalchemy.orm import Session

from mlte.artifact.model import ArtifactHeaderModel, ArtifactModel
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
from mlte.tests.model import TestSuiteModel

# -------------------------------------------------------------------------
# DB artifact factory.
# -------------------------------------------------------------------------


def create_artifact_orm(
    artifact: ArtifactModel,
    model_id: str,
    version_id: str,
    session: Session,
) -> typing.Union[
    DBTestSuite, DBTestResults, DBNegotiationCard, DBReport, DBEvidence
]:
    """Converts an internal model to its corresponding DB object for artifacts."""
    # Get type and version info from DB.
    artifact_type_orm = DBReader.get_artifact_type(
        artifact.header.type, session
    )
    _, version_orm = DBReader.get_version(model_id, version_id, session)

    # Create the artifact object, without the specific body.
    artifact_orm = DBArtifact(
        identifier=artifact.header.identifier,
        type=artifact_type_orm,
        timestamp=artifact.header.timestamp,
        username=artifact.header.creator,
        version_id=version_orm.id,
    )

    # Create the body ORM object and return it.
    if artifact.header.type == ArtifactType.NEGOTIATION_CARD:
        card = typing.cast(NegotiationCardModel, artifact.body)
        return card_factory.create_card_orm(card, artifact_orm, session)
    elif artifact.header.type == ArtifactType.TEST_SUITE:
        test_suite = typing.cast(TestSuiteModel, artifact.body)
        return suite_factory.create_suite_orm(test_suite, artifact_orm)
    elif artifact.header.type == ArtifactType.EVIDENCE:
        value = typing.cast(EvidenceModel, artifact.body)
        return evidence_factory.create_evidence_orm(value, artifact_orm)
    elif artifact.header.type == ArtifactType.TEST_RESULTS:
        test_results = typing.cast(TestResultsModel, artifact.body)
        return result_factory.create_results_orm(test_results, artifact_orm)
    elif artifact.header.type == ArtifactType.REPORT:
        report = typing.cast(ReportModel, artifact.body)
        return report_factory.create_report_orm(report, artifact_orm, session)
    else:
        raise Exception(
            f"Unsupported artifact type for conversion: {artifact.header.type}"
        )


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
