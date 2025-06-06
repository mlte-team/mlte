"""
test/report/test_model.py

Unit tests for report model.
"""

from mlte.report.model import (
    CommentDescriptor,
    QuantitiveAnalysisDescriptor,
    ReportModel,
)
from test.fixture.artifact import make_complete_report


def test_report() -> None:
    """A report model can be serialized and deserialized."""
    objects = [
        make_complete_report(),
    ]

    for object in objects:
        s = object.to_json()
        d = ReportModel.from_json(s)
        assert d == object


def test_comment() -> None:
    """A comment can be serialized and deserialized."""
    objects = [
        CommentDescriptor(content="content"),
    ]

    for object in objects:
        s = object.to_json()
        d = CommentDescriptor.from_json(s)
        assert d == object


def test_quantitative_analysis() -> None:
    """A quantitative analysis model can be serialized and deserialized."""
    objects = [
        QuantitiveAnalysisDescriptor(content="content"),
        QuantitiveAnalysisDescriptor(),
    ]
    for object in objects:
        s = object.to_json()
        d = QuantitiveAnalysisDescriptor.from_json(s)
        assert d == object
