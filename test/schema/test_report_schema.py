"""
test/schema/test_report_schema.py

Unit tests for report schema validation.
"""

import typing

from mlte.artifact.model import ArtifactModel
from mlte.report.artifact import Report
from test.fixture.artifact import make_complete_report

from . import util as util


def test_empty_instance() -> None:
    """An empty instance validates successfully."""
    report = Report()

    doc = report.to_model().to_json()
    util.validate_report_schema(doc["body"])


def test_valid_instance() -> None:
    """A complete instance validates successfully."""
    report_model: ArtifactModel = typing.cast(
        ArtifactModel, make_complete_report()
    )
    report = Report.from_model(report_model)
    doc = report.to_model().to_json()
    util.validate_report_schema(doc["body"])
