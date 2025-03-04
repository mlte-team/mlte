"""
test/value/test_extension.py

Unit tests for extension of the MLTE value system.
"""

from __future__ import annotations

from typing import Any, Tuple

import pytest

from mlte.context.context import Context
from mlte.evidence.external import ExternalEvidence
from mlte.store.artifact.store import ArtifactStore
from test.evidence.types.helper import get_sample_evidence_metadata
from test.store.artifact.fixture import store_with_context  # noqa


class ConfusionMatrix(ExternalEvidence):
    """A sample extension value type."""

    def __init__(self, matrix: list[list[int]]):
        super().__init__()

        self.matrix = matrix
        """Underlying matrix represented as two-dimensional array."""

    def serialize(self) -> dict[str, Any]:
        return {"matrix": self.matrix}

    @staticmethod
    def deserialize(data: dict[str, Any]) -> ConfusionMatrix:
        return ConfusionMatrix(data["matrix"])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ConfusionMatrix):
            return False
        return self._equal(other)


class BadInteger(ExternalEvidence):
    """An extension evidence that does not implement the interface."""

    def __init__(self, integer: int):
        super().__init__()

        self.integer = integer


def test_serde() -> None:
    """Confusion matrix can be serialized and deserialized."""
    cm = ConfusionMatrix([[1, 2], [3, 4]]).with_metadata(
        get_sample_evidence_metadata()
    )

    serialized = cm.serialize()

    deserialized = ConfusionMatrix.deserialize(serialized)
    assert deserialized == cm


def test_model() -> None:
    """Confusion matrix can round trip to and from model."""
    cm = ConfusionMatrix([[1, 2], [3, 4]]).with_metadata(
        get_sample_evidence_metadata()
    )

    m = cm.to_model()

    r = ConfusionMatrix.from_model(m)
    assert r == cm


def test_save_load(
    store_with_context: Tuple[ArtifactStore, Context]  # noqa
) -> None:
    """Confusion matrix can be saved to and loaded from artifact store."""
    store, ctx = store_with_context

    cm = ConfusionMatrix([[1, 2], [3, 4]]).with_metadata(
        get_sample_evidence_metadata()
    )

    cm.save_with(ctx, store)

    loaded = ConfusionMatrix.load_with("id.value", context=ctx, store=store)
    assert loaded == cm


def test_subclass_fail() -> None:
    """A value type that fails to meet the interface cannot be instantiated."""
    with pytest.raises(TypeError):
        _ = BadInteger(1).with_metadata(get_sample_evidence_metadata())  # type: ignore
