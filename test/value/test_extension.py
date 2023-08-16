"""
test/value/test_extension.py

Unit tests for extension of the MLTE value system.
"""

from __future__ import annotations

from typing import Any

from mlte.context.context import Context
from mlte.evidence.identifier import Identifier
from mlte.evidence.metadata import EvidenceMetadata
from mlte.store.store import Store
from mlte.value.base import Value

from ..fixture.store import store_with_context  # noqa


class ConfusionMatrix(Value):
    """A sample extension value type."""

    def __init__(self, metadata: EvidenceMetadata, matrix: list[list[int]]):
        super().__init__(self, metadata)

        self.matrix = matrix
        """Underlying matrix represented as two-dimensional array."""

    def serialize(self) -> dict[str, Any]:
        return {"matrix": self.matrix}

    @staticmethod
    def deserialize(
        metadata: EvidenceMetadata, data: dict[str, Any]
    ) -> ConfusionMatrix:
        return ConfusionMatrix(metadata, data["matrix"])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ConfusionMatrix):
            return False
        return self.matrix == other.matrix


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


def test_save_load(store_with_context: tuple[Store, Context]) -> None:  # noqa
    """Confusion matrix can be saved to and loaded from artifact store."""
    store, ctx = store_with_context

    em = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )
    cm = ConfusionMatrix(em, [[1, 2], [3, 4]])

    cm.save_with(ctx, store)

    loaded = ConfusionMatrix.load_with("id.value", ctx, store)
    assert loaded == cm
