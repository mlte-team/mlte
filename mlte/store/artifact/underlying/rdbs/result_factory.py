"""Conversions between schema and internal models."""

from __future__ import annotations

from sqlalchemy.orm import Session

from mlte.evidence.metadata import EvidenceMetadata
from mlte.measurement.model import MeasurementMetadata
from mlte.results.model import ResultModel, TestResultsModel
from mlte.store.artifact.underlying.rdbs.evidence_metadata import (
    DBEvidenceMetadata,
)
from mlte.store.artifact.underlying.rdbs.main_metadata import DBArtifact
from mlte.store.artifact.underlying.rdbs.reader import DBReader
from mlte.store.artifact.underlying.rdbs.result_metadata import (
    DBResult,
    DBTestResults,
)
from mlte.store.artifact.underlying.rdbs.tests_factory import (
    create_test_suite_model_from_db,
)

# -------------------------------------------------------------------------
# TestResults Factory Methods
# -------------------------------------------------------------------------


def create_test_results_db_from_model(
    test_results: TestResultsModel,
    artifact: DBArtifact,
    session: Session,
) -> DBTestResults:
    """Creates the DB object from the corresponding internal model."""
    test_results_obj = DBTestResults(
        artifact=artifact,
        results=[],
        test_suite=(
            DBReader.get_test_suite(
                test_results.test_suite_id,
                artifact.version_id,
                session,
            )
            if test_results.test_suite_id != ""
            else None
        ),
    )
    for test_case_id, result in test_results.results.items():
        result_obj = DBResult(
            type=result.type,
            message=result.message,
            test_results=test_results_obj,
            evidence_metadata=(
                DBEvidenceMetadata(
                    test_case_id=test_case_id,
                    measurement=result.evidence_metadata.measurement.to_json_string(),
                )
                if result.evidence_metadata is not None
                else None
            ),
        )
        test_results_obj.results.append(result_obj)
    return test_results_obj


def create_test_results_model_from_db(
    test_results_obj: DBTestResults,
) -> TestResultsModel:
    """Creates the internal model object from the corresponding DB object."""
    body = TestResultsModel(
        results=(
            {
                result.evidence_metadata.test_case_id: ResultModel(
                    type=result.type,
                    message=result.message,
                    evidence_metadata=EvidenceMetadata(
                        test_case_id=result.evidence_metadata.test_case_id,
                        measurement=MeasurementMetadata.from_json_string(
                            result.evidence_metadata.measurement
                        ),
                    ),
                )
                for result in test_results_obj.results
            }
        ),
        test_suite_id=(
            test_results_obj.test_suite.artifact.identifier
            if test_results_obj.test_suite is not None
            else ""
        ),
        test_suite=(
            create_test_suite_model_from_db(test_results_obj.test_suite)
        ),
    )
    return body
