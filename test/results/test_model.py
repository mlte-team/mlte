"""
Unit tests for TestResults model.
"""

from __future__ import annotations

import typing

from mlte.artifact.type import ArtifactType
from mlte.results.model import TestResultsModel
from test.fixture.artifact import ArtifactModelFactory


def test_test_results_body() -> None:
    """A TestSuite model can be serialized and deserialized."""
    objects = [
        typing.cast(
            TestResultsModel,
            ArtifactModelFactory.make(ArtifactType.TEST_RESULTS).body,
        ),
    ]

    for object in objects:
        s = object.to_json()
        d = TestResultsModel.from_json(s)
        assert d == object
