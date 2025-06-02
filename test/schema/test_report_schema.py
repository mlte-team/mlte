"""
test/schema/test_report_schema.py

Unit tests for report schema validation.
"""

from mlte.artifact.type import ArtifactType
from mlte.report.artifact import Report
from test.fixture.artifact import ArtifactFactory

from . import util as util


def test_valid_instance() -> None:
    """A complete instance validates successfully."""
    artifact_model = ArtifactFactory.make(ArtifactType.REPORT, id="id0")
    report = Report.from_model(artifact_model)
    doc = report.to_model().to_json()
    util.validate_report_schema(doc["body"])
