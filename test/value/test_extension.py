"""
test/value/test_extension.py

Unit tests for extension of the MLTE value system.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

import pytest

from mlte.context.context import Context
from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.store.artifact.store import ArtifactStore
from mlte.value.base import ValueBase

from ..fixture.store import store_with_context  # noqa


class ConfusionMatrix(ValueBase):
    """A sample extension value type."""

    def __init__(self, metadata: EvidenceMetadata, matrix: List[List[int]]):
        super().__init__(self, metadata)

        self.matrix = matrix
        """Underlying matrix represented as two-dimensional array."""

    def serialize(self) -> Dict[str, Any]:
        return {"matrix": self.matrix}

    @staticmethod
    def deserialize(
        metadata: EvidenceMetadata, data: Dict[str, Any]
    ) -> ConfusionMatrix:
        return ConfusionMatrix(metadata, data["matrix"])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ConfusionMatrix):
            return False
        return self._equal(other)


class BadInteger(ValueBase):
    """An extension value that does not implement the interface."""

    def __init__(self, metadata: EvidenceMetadata, integer: int):
        super().__init__(self, metadata)

        self.integer = integer


def test_serde() -> None:
    """Confusion matrix can be serialized and deserialized."""
    em = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )
    cm = ConfusionMatrix(em, [[1, 2], [3, 4]])

    serialized = cm.serialize()

    deserialized = ConfusionMatrix.deserialize(em, serialized)
    assert deserialized == cm


def test_model() -> None:
    """Confusion matrix can round trip to and from model."""
    em = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )
    cm = ConfusionMatrix(em, [[1, 2], [3, 4]])

    m = cm.to_model()

    r = ConfusionMatrix.from_model(m)
    assert r == cm


def test_save_load(
    store_with_context: Tuple[ArtifactStore, Context]  # noqa
) -> None:
    """Confusion matrix can be saved to and loaded from artifact store."""
    store, ctx = store_with_context

    em = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )
    cm = ConfusionMatrix(em, [[1, 2], [3, 4]])

    cm.save_with(ctx, store)

    loaded = ConfusionMatrix.load_with("id.value", context=ctx, store=store)
    assert loaded == cm


def test_subclass_fail() -> None:
    """A value type that fails to meet the interface cannot be instantiated."""
    em = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )
    with pytest.raises(TypeError):
        _ = BadInteger(em, 1)  # type: ignore
