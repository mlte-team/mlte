"""Conversions between schema and internal models."""

from __future__ import annotations

from typing import Optional

from mlte._private.fixed_json import json
from mlte.measurement.model import MeasurementMetadata
from mlte.store.artifact.underlying.rdbs.main_metadata import DBArtifact
from mlte.store.artifact.underlying.rdbs.tests_metadata import (
    DBTestCase,
    DBTestSuite,
)
from mlte.tests.model import TestCaseModel, TestSuiteModel
from mlte.validation.model import ValidatorModel

# -------------------------------------------------------------------------
# TestSuite Factory Methods
# -------------------------------------------------------------------------


def create_test_suite_db_from_model(
    test_suite: TestSuiteModel, artifact: Optional[DBArtifact]
) -> DBTestSuite:
    """Creates the DB object from the corresponding internal model."""
    test_suite_obj = DBTestSuite(artifact=artifact, test_cases=[])
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
