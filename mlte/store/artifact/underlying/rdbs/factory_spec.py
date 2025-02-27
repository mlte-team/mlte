"""
mlte/store/artifact/underlying/rdbs/factory_spec.py

Conversions between schema and internal models.
"""

from __future__ import annotations

import typing

from sqlalchemy.orm import Session

from mlte._private.fixed_json import json
from mlte.evidence.metadata import EvidenceMetadata
from mlte.measurement.model import MeasurementMetadata
from mlte.spec.model import QACategoryModel, TestSuiteModel
from mlte.store.artifact.underlying.rdbs.metadata import DBArtifactHeader
from mlte.store.artifact.underlying.rdbs.metadata_spec import (
    DBCondition,
    DBEvidenceMetadata,
    DBQACategory,
    DBResult,
    DBSpec,
    DBTestResults,
)
from mlte.store.artifact.underlying.rdbs.reader import DBReader
from mlte.validation.model import ResultModel, TestResultsModel
from mlte.validation.model_condition import ConditionModel

# -------------------------------------------------------------------------
# Spec Factory Methods
# -------------------------------------------------------------------------


def create_spec_db_from_model(
    spec: TestSuiteModel, artifact_header: DBArtifactHeader
) -> DBSpec:
    """Creates the DB object from the corresponding internal model."""
    spec_obj = DBSpec(artifact_header=artifact_header, qa_categories=[])
    for qa_category in spec.qa_categories:
        qa_category_obj = DBQACategory(
            name=qa_category.name,
            description=qa_category.description,
            rationale=qa_category.rationale,
            module=qa_category.module,
            spec=spec_obj,
        )
        spec_obj.qa_categories.append(qa_category_obj)

        for (
            measurement_id,
            condition,
        ) in qa_category.conditions.items():
            condition_obj = DBCondition(
                name=condition.name,
                measurement_id=measurement_id,
                arguments=condition.args_to_json_str(),
                validator=json.dumps(condition.validator.to_json()),
                value_class=condition.value_class,
                qa_category=qa_category_obj,
            )
            qa_category_obj.conditions.append(condition_obj)

    return spec_obj


def create_spec_model_from_db(spec_obj: DBSpec) -> TestSuiteModel:
    """Creates the internal model object from the corresponding DB object."""
    # Creating a Spec from DB data.
    body = TestSuiteModel(
        qa_categories=[
            QACategoryModel(
                name=category.name,
                description=category.description,
                rationale=category.rationale,
                module=category.module,
                conditions={
                    condition.measurement_id: ConditionModel(
                        name=condition.name,
                        validator=json.loads(condition.validator),
                        value_class=condition.value_class,
                        arguments=json.loads(condition.arguments),
                    )
                    for condition in category.conditions
                },
            )
            for category in spec_obj.qa_categories
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
            DBReader.get_spec(
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
                    measurement=json.dumps(
                        result.evidence_metadata.measurement.to_json()
                    ),
                )
                if result.evidence_metadata is not None
                else None
            ),
        )
        test_results_obj.results.append(result_obj)
    return test_results_obj


def create_v_spec_model_from_db(
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
                        measurement=typing.cast(
                            MeasurementMetadata,
                            MeasurementMetadata.from_json(
                                json.loads(result.evidence_metadata.measurement)
                            ),
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
            create_spec_model_from_db(test_results_obj.test_suite)
            if test_results_obj.test_suite is not None
            else None
        ),
    )
    return body
