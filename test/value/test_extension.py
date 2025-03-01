"""
test/value/test_extension.py

Unit tests for extension of the MLTE value system.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

import pytest

from mlte.context.context import Context
from mlte.evidence.base import ValueBase
from mlte.evidence.metadata import EvidenceMetadata
from mlte.store.artifact.store import ArtifactStore
from test.store.artifact.fixture import store_with_context  # noqa
from test.value.types.helper import get_sample_evidence_metadata


class ConfusionMatrix(ValueBase):
    """A sample extension value type."""

    def __init__(self, matrix: List[List[int]]):
        self.matrix = matrix
        """Underlying matrix represented as two-dimensional array."""

    def serialize(self) -> Dict[str, Any]:
        return {"matrix": self.matrix}

    @staticmethod
    def deserialize(
        metadata: EvidenceMetadata, data: Dict[str, Any]
    ) -> ConfusionMatrix:
        return ConfusionMatrix(data["matrix"]).with_metadata(metadata)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ConfusionMatrix):
            return False
        return self._equal(other)


class BadInteger(ValueBase):
    """An extension value that does not implement the interface."""

    def __init__(self, integer: int):
        self.integer = integer


def test_serde() -> None:
    """Confusion matrix can be serialized and deserialized."""
    cm = ConfusionMatrix(get_sample_evidence_metadata(), [[1, 2], [3, 4]])

    serialized = cm.serialize()

    deserialized = ConfusionMatrix.deserialize(
        get_sample_evidence_metadata(), serialized
    )
    assert deserialized == cm


def test_model() -> None:
    """Confusion matrix can round trip to and from model."""
    cm = ConfusionMatrix(get_sample_evidence_metadata(), [[1, 2], [3, 4]])

    m = cm.to_model()

    r = ConfusionMatrix.from_model(m)
    assert r == cm


def test_save_load(
    store_with_context: Tuple[ArtifactStore, Context]  # noqa
) -> None:
    """Confusion matrix can be saved to and loaded from artifact store."""
    store, ctx = store_with_context

    cm = ConfusionMatrix(get_sample_evidence_metadata(), [[1, 2], [3, 4]])

    cm.save_with(ctx, store)

    loaded = ConfusionMatrix.load_with("id.value", context=ctx, store=store)
    assert loaded == cm


def test_subclass_fail() -> None:
    """A value type that fails to meet the interface cannot be instantiated."""
    with pytest.raises(TypeError):
        _ = BadInteger(get_sample_evidence_metadata(), 1)  # type: ignore
