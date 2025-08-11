"""
test/report/test_model.py

Unit tests for report model.
"""

import typing

from mlte.artifact.type import ArtifactType
from mlte.report.model import CommentDescriptor, ReportModel
from test.fixture.artifact import ArtifactModelFactory


def test_report() -> None:
    """A report model can be serialized and deserialized."""
    objects = [
        typing.cast(
            ReportModel, ArtifactModelFactory.make(ArtifactType.REPORT).body
        ),
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
