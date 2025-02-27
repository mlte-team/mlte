"""
test/value/types/test_array.py

Unit tests for Array.
"""

from __future__ import annotations

from typing import Tuple

from mlte.context.context import Context
from mlte.evidence.types.array import Array
from mlte.measurement.measurement import Measurement
from mlte.store.artifact.store import ArtifactStore
from test.store.artifact.fixture import store_with_context  # noqa
from test.value.types.helper import get_sample_evidence_metadata


class DummyMeasurementArray(Measurement):
    def __init__(self, identifier: str):
        super().__init__(identifier)

    def __call__(self) -> Array:
        return Array(self.evidence_metadata, [1, 2, 3])


def test_measurement():
    """Array can be produced by a measurement."""

    m = DummyMeasurementArray("identifier")
    t = m.evaluate()
    assert isinstance(t, Array)

    assert t.array == [1, 2, 3]


def test_equality():
    """Array instances can be compared for equality."""

    m = get_sample_evidence_metadata()

    a = Array(m, [1, 2, 3])
    b = Array(m, [1, 2, 3])
    assert a == b

    a = Array(m, [1.1, 2.2, 3.3])
    b = Array(m, [1.1, 2.2, 3.3])
    assert a == b

    a = Array(m, ["a", "b", "c"])
    b = Array(m, ["a", "b", "c"])
    assert a == b


def test_serde() -> None:
    """Array can be converted to model and back."""
    o = Array(get_sample_evidence_metadata(), [1, 2, 3])

    model = o.to_model()
    e = Array.from_model(model)

    assert e == o


def test_save_load(
    store_with_context: Tuple[ArtifactStore, Context]  # noqa
) -> None:
    """Array can be saved to and loaded from artifact store."""
    store, ctx = store_with_context

    o = Array(get_sample_evidence_metadata(), [1, 2, 3])
    o.save_with(ctx, store)

    loaded = Array.load_with("id.value", context=ctx, store=store)
    assert loaded == o
