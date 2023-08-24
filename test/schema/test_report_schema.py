"""
test/schema/test_report_schema.py

Unit tests for report schema validation.
"""

import time

import pytest
from jsonschema import ValidationError

from mlte._private.schema import validate_report_schema
from mlte.report import Dataset, Limitation, Report, UseCase, User
from mlte.spec.spec import Spec
from mlte.validation.result import Ignore
from mlte.validation.validated_spec import ValidatedSpec


@pytest.mark.skip("Pending artifact protocol implementation.")
def test_empty_instance() -> None:  # noqa
    report = Report()
    validate_report_schema(report.to_json())


@pytest.mark.skip("Pending artifact protocol implementation.")
def test_valid_instance() -> None:  # noqa
    report = Report()
    report.metadata.project_name = "ProjectName"
    report.metadata.authors = ["Foo", "Bar"]
    report.metadata.source_url = "https://github.com/mlte-team"
    report.metadata.artifact_url = "https://github.com/mlte-team"
    report.metadata.timestamp = f"{int(time.time())}"

    report.model_details.name = "ModelName"
    report.model_details.overview = "Model overview."
    report.model_details.documentation = "Model documentation."

    report.model_specification.domain = "ModelDomain"
    report.model_specification.architecture = "ModelArchitecture"
    report.model_specification.input = "ModelInput"
    report.model_specification.output = "ModelOutput"
    report.model_specification.data = [
        Dataset("Dataset0", "https://github.com/mlte-team", "Description"),
        Dataset("Dataset1", "https://github.com/mlte-team", "Description."),
    ]

    report.considerations.users = [
        User("User description 0."),
        User("User description 1."),
    ]
    report.considerations.use_cases = [
        UseCase("Use case description 0."),
        UseCase("Use case description 1."),
    ]
    report.considerations.limitations = [
        Limitation("Limitation description 0."),
        Limitation("Limitation description 1."),
    ]

    report.spec = ValidatedSpec(results={"prop": {"test": Ignore("ignore")}})

    validate_report_schema(report.to_json())


@pytest.mark.skip("Pending artifact protocol implementation.")
def test_invalid_instance():
    with pytest.raises(ValidationError):
        validate_report_schema({})
