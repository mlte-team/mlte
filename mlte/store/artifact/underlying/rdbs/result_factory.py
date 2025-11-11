"""Conversions between schema and internal models."""

from __future__ import annotations

from mlte.evidence.metadata import EvidenceMetadata
from mlte.measurement.model import MeasurementMetadata
from mlte.results.model import ResultModel, TestResultsModel
from mlte.store.artifact.underlying.rdbs import suite_factory
from mlte.store.artifact.underlying.rdbs.evidence_metadata import (
    DBEvidenceMetadata,
)
from mlte.store.artifact.underlying.rdbs.result_metadata import (
    DBResult,
    DBTestResults,
)

# -------------------------------------------------------------------------
# TestResults Factory Methods
# -------------------------------------------------------------------------


def create_results_orm(
    test_results: TestResultsModel,
) -> DBTestResults:
    """Creates the DB object from the corresponding internal model."""
    test_results_orm = DBTestResults(
        results=[],
        test_suite_identifier=test_results.test_suite_id,
        test_suite=suite_factory.create_suite_orm(test_results.test_suite),
    )
    for test_case_id, result in test_results.results.items():
        result_orm = DBResult(
            type=result.type,
            message=result.message,
            test_results=test_results_orm,
            evidence_metadata=(
                DBEvidenceMetadata(
                    test_case_id=test_case_id,
                    measurement=result.evidence_metadata.measurement.to_json_string(),
                )
                if result.evidence_metadata is not None
                else None
            ),
        )
        test_results_orm.results.append(result_orm)
    return test_results_orm


def create_results_model(
    test_results_orm: DBTestResults,
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
                for result in test_results_orm.results
            }
        ),
        test_suite_id=test_results_orm.test_suite_identifier,
        test_suite=(
            suite_factory.create_suite_model(test_results_orm.test_suite)
        ),
    )
    return body
