"""
Conversions between schema and internal models.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from mlte._private.fixed_json import json
from mlte.evidence.metadata import EvidenceMetadata
from mlte.measurement.model import MeasurementMetadata
from mlte.results.model import ResultModel, TestResultsModel
from mlte.store.artifact.underlying.rdbs.metadata import DBArtifactHeader
from mlte.store.artifact.underlying.rdbs.metadata_spec import (
    DBEvidenceMetadata,
    DBResult,
    DBTestCase,
    DBTestResults,
    DBTestSuite,
)
from mlte.store.artifact.underlying.rdbs.reader import DBReader
from mlte.tests.model import TestCaseModel, TestSuiteModel
from mlte.validation.model import ValidatorModel

# -------------------------------------------------------------------------
# TestSuite Factory Methods
# -------------------------------------------------------------------------


def create_spec_db_from_model(
    test_suite: TestSuiteModel, artifact_header: DBArtifactHeader
) -> DBTestSuite:
    """Creates the DB object from the corresponding internal model."""
    test_suite_obj = DBTestSuite(artifact_header=artifact_header, test_cases=[])
    for test_case in test_suite.test_cases:
        test_case_obj = DBTestCase(
            identifier=test_case.identifier,
            goal=test_case.goal,
            measurement_metadata=(
                test_case.measurement.to_json_string()
                if test_case.measurement
                else None
            ),
            validator=(
                test_case.validator.to_json_string()
                if test_case.validator
                else None
            ),
            qas_list=json.dumps(test_case.qas_list),
        )
        test_suite_obj.test_cases.append(test_case_obj)

    return test_suite_obj


def create_test_suite_model_from_db(
    test_suite_obj: DBTestSuite,
) -> TestSuiteModel:
    """Creates the internal model object from the corresponding DB object."""
    # Creating a TestSuite from DB data.
    body = TestSuiteModel(
        test_cases=[
            TestCaseModel(
                identifier=test_case_obj.identifier,
                goal=test_case_obj.goal,
                measurement=(
                    MeasurementMetadata.from_json_string(
                        test_case_obj.measurement_metadata
                    )
                    if test_case_obj.measurement_metadata
                    else None
                ),
                validator=(
                    ValidatorModel.from_json_string(test_case_obj.validator)
                    if test_case_obj.validator
                    else None
                ),
                qas_list=json.loads(test_case_obj.qas_list),
            )
            for test_case_obj in test_suite_obj.test_cases
        ],
    )
    return body


# -------------------------------------------------------------------------
# TestResults Factory Methods
# -------------------------------------------------------------------------


def create_test_results_db_from_model(
    test_results: TestResultsModel,
    artifact_header: DBArtifactHeader,
    session: Session,
) -> DBTestResults:
    """Creates the DB object from the corresponding internal model."""
    test_results_obj = DBTestResults(
        artifact_header=artifact_header,
        results=[],
        test_suite=(
            DBReader.get_test_suite(
                test_results.test_suite_id,
                artifact_header.version_id,
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
            test_results_obj.test_suite.artifact_header.identifier
            if test_results_obj.test_suite is not None
            else ""
        ),
        test_suite=(
            create_test_suite_model_from_db(test_results_obj.test_suite)
        ),
    )
    return body
