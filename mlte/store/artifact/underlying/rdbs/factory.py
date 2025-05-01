"""
mlte/store/artifact/underlying/rdbs/factory.py

Creation of metadata objects from pydantic models.
"""

import typing

from sqlalchemy.orm import Session

from mlte.artifact.model import ArtifactHeaderModel, ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.evidence.model import EvidenceModel
from mlte.negotiation.model import NegotiationCardModel
from mlte.report.model import ReportModel
from mlte.results.model import TestResultsModel
from mlte.store.artifact.underlying.rdbs.factory_nc import (
    create_negotiation_db_from_model,
    create_negotiation_model_from_db,
    create_report_db_from_model,
    create_report_model_from_db,
)
from mlte.store.artifact.underlying.rdbs.factory_spec import (
    create_spec_db_from_model,
    create_test_results_db_from_model,
    create_test_results_model_from_db,
    create_test_suite_model_from_db,
)
from mlte.store.artifact.underlying.rdbs.factory_value import (
    create_evidence_db_from_model,
    create_evidence_model_from_db,
)
from mlte.store.artifact.underlying.rdbs.metadata import (
    DBArtifactHeader,
    DBArtifactType,
)
from mlte.store.artifact.underlying.rdbs.metadata_evidence import DBEvidence
from mlte.store.artifact.underlying.rdbs.metadata_nc import (
    DBNegotiationCard,
    DBReport,
)
from mlte.store.artifact.underlying.rdbs.metadata_spec import (
    DBTestResults,
    DBTestSuite,
)
from mlte.tests.model import TestSuiteModel

# -------------------------------------------------------------------------
# DB artifact factory.
# -------------------------------------------------------------------------


def create_db_artifact(
    artifact: ArtifactModel,
    artifact_type_obj: DBArtifactType,
    version_id: int,
    session: Session,
) -> typing.Union[
    DBTestSuite, DBTestResults, DBNegotiationCard, DBReport, DBEvidence
]:
    """Converts an internal model to its corresponding DB object for artifacts."""
    artifact_header = DBArtifactHeader(
        identifier=artifact.header.identifier,
        type=artifact_type_obj,
        timestamp=artifact.header.timestamp,
        username=artifact.header.creator,
        version_id=version_id,
    )

    if artifact.header.type == ArtifactType.TEST_SUITE:
        # Create a DBTestSuite and its internal TestResult list.
        test_suite = typing.cast(TestSuiteModel, artifact.body)
        return create_spec_db_from_model(test_suite, artifact_header)
    elif artifact.header.type == ArtifactType.TEST_RESULTS:
        # Create a DBTestResults db object.
        test_results = typing.cast(TestResultsModel, artifact.body)
        return create_test_results_db_from_model(
            test_results, artifact_header, session
        )
    elif artifact.header.type == ArtifactType.NEGOTIATION_CARD:
        # Create a DBNegotiationCard object and all its subpieces.
        negotiation_card = typing.cast(NegotiationCardModel, artifact.body)
        return create_negotiation_db_from_model(
            negotiation_card, artifact_header, session
        )
    elif artifact.header.type == ArtifactType.REPORT:
        # Create a DBReport object and all its subpieces.
        report = typing.cast(ReportModel, artifact.body)
        return create_report_db_from_model(report, artifact_header, session)
    elif artifact.header.type == ArtifactType.EVIDENCE:
        # Create a DBValue object and all its subpieces.
        value = typing.cast(EvidenceModel, artifact.body)
        return create_evidence_db_from_model(value, artifact_header)
    else:
        raise Exception(
            f"Unsupported artifact type for conversion: {artifact.header.type}"
        )


# -------------------------------------------------------------------------
# Artifact model factory.
# -------------------------------------------------------------------------


def create_artifact_from_db(
    artifact_header_obj: DBArtifactHeader, session: Session
) -> ArtifactModel:
    """
    Creates an Artifact model from the corresponding DB object and DB header.

    :param artifact_header_obj: A DBArtifactHeader object from the DB with header info.
    :param session: The DB session to use.
    :return: the DB data converted into an ArtifactModel.
    """
    artifact_header = ArtifactHeaderModel(
        identifier=artifact_header_obj.identifier,
        type=ArtifactType(artifact_header_obj.type.name),
        timestamp=artifact_header_obj.timestamp,
        creator=artifact_header_obj.username,
    )

    body: typing.Union[
        TestSuiteModel,
        TestResultsModel,
        NegotiationCardModel,
        ReportModel,
        EvidenceModel,
    ]
    if artifact_header.type == ArtifactType.TEST_SUITE:
        # Creating a TestSuit from DB data.
        test_suite_obj = typing.cast(
            DBTestSuite, artifact_header_obj.body_test_suite
        )
        body = create_test_suite_model_from_db(test_suite_obj)
    elif artifact_header.type == ArtifactType.TEST_RESULTS:
        # Creating a TestResults from DB data.
        test_results_obj = typing.cast(
            DBTestResults, artifact_header_obj.body_test_results
        )
        body = create_test_results_model_from_db(test_results_obj)
    elif artifact_header.type == ArtifactType.NEGOTIATION_CARD:
        # Creating a NegotiationCard from DB data.
        negotiation_obj = typing.cast(
            DBNegotiationCard, artifact_header_obj.body_negotiation_card
        )
        body = create_negotiation_model_from_db(negotiation_obj)
    elif artifact_header.type == ArtifactType.REPORT:
        # Creating a Report from DB data.
        report_obj = typing.cast(DBReport, artifact_header_obj.body_report)
        body = create_report_model_from_db(report_obj)
    elif artifact_header.type == ArtifactType.EVIDENCE:
        # Creating a Value from DB data.
        value_obj = typing.cast(DBEvidence, artifact_header_obj.body_evidence)
        body = create_evidence_model_from_db(value_obj)

    else:
        raise Exception(
            f"Unsupported artifact type for conversion: {artifact_header.type}"
        )

    return ArtifactModel(header=artifact_header, body=body)
