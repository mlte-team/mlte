"""
Unit tests for specification model.
"""

from __future__ import annotations

import typing

from mlte.artifact.type import ArtifactType
from mlte.suite.model import TestSuiteModel
from test.fixture.artifact import ArtifactModelFactory


def test_spec_body() -> None:
    """A TestSuite model can be serialized and deserialized."""
    objects = [
        typing.cast(
            TestSuiteModel,
            ArtifactModelFactory.make(ArtifactType.TEST_SUITE).body,
        ),
        TestSuiteModel(),
    ]

    for object in objects:
        s = object.to_json()
        d = TestSuiteModel.from_json(s)
        assert d == object
