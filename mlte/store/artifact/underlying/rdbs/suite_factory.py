"""Conversions between schema and internal models."""

from __future__ import annotations

from typing import Optional

from mlte._private.fixed_json import json
from mlte.measurement.model import MeasurementMetadata
from mlte.store.artifact.underlying.rdbs.main_metadata import DBArtifact
from mlte.store.artifact.underlying.rdbs.suite_metadata import (
    DBTestCase,
    DBTestSuite,
)
from mlte.tests.model import TestCaseModel, TestSuiteModel
from mlte.validation.model import ValidatorModel

# -------------------------------------------------------------------------
# TestSuite Factory Methods
# -------------------------------------------------------------------------


def create_suite_orm(
    test_suite: TestSuiteModel, artifact_orm: Optional[DBArtifact]
) -> DBTestSuite:
    """Creates the DB object from the corresponding internal model."""
    test_suite_orm = DBTestSuite(artifact=artifact_orm, test_cases=[])
    for test_case in test_suite.test_cases:
        test_case_orm = DBTestCase(
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
        test_suite_orm.test_cases.append(test_case_orm)

    return test_suite_orm


def create_suite_model(
    test_suite_orm: DBTestSuite,
) -> TestSuiteModel:
    """Creates the internal model object from the corresponding DB object."""
    # Creating a TestSuite from DB data.
    body = TestSuiteModel(
        test_cases=[
            TestCaseModel(
                identifier=test_case_orm.identifier,
                goal=test_case_orm.goal,
                measurement=(
                    MeasurementMetadata.from_json_string(
                        test_case_orm.measurement_metadata
                    )
                    if test_case_orm.measurement_metadata
                    else None
                ),
                validator=(
                    ValidatorModel.from_json_string(test_case_orm.validator)
                    if test_case_orm.validator
                    else None
                ),
                qas_list=json.loads(test_case_orm.qas_list),
            )
            for test_case_orm in test_suite_orm.test_cases
        ],
    )
    return body
