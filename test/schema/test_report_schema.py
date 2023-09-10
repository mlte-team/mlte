"""
test/schema/test_report_schema.py

Unit tests for report schema validation.
"""

import pytest
from jsonschema import ValidationError

from mlte.report.artifact import Report

from . import util as util


def test_empty_instance() -> None:  # noqa
    report = Report()

    doc = report.to_model().to_json()
    util.validate_report_schema(doc["body"])


@pytest.mark.skip("Pending artifact protocol implementation.")
def test_valid_instance() -> None:
    assert True


def test_invalid_instance():
    with pytest.raises(ValidationError):
        util.validate_report_schema({})
