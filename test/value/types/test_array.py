"""
test/value/types/test_array.py

Unit tests for Array.
"""

from __future__ import annotations

from typing import Tuple

import pytest

from mlte.context.context import Context
from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.measurement import Measurement
from mlte.store.base import Store
from mlte.value.types.array import Array

from ...fixture.store import store_with_context  # noqa


class DummyMeasurementArray(Measurement):
    def __init__(self, identifier: str):
        super().__init__(self, identifier)

    def __call__(self) -> Array:
        return Array(self.metadata, [1, 2, 3])


def test_measurement():
    """Array can be produced by a measurement."""

    m = DummyMeasurementArray("identifier")
    t = m.evaluate()
    assert isinstance(t, Array)

    assert t.array == [1, 2, 3]


def test_equality():
    """Array instances can be compared for equality."""

    m = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )

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
    m = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )
    o = Array(m, [1, 2, 3])

    model = o.to_model()
    e = Array.from_model(model)

    assert e == o


def test_save_load(store_with_context: Tuple[Store, Context]) -> None:  # noqa
    """Array can be saved to and loaded from artifact store."""
    store, ctx = store_with_context

    m = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )
    o = Array(m, [1, 2, 3])
    o.save_with(ctx, store)

    loaded = Array.load_with("id.value", context=ctx, store=store)
    assert loaded == o


def test_get_as_real():
    m = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )

    array = Array(m, [1.0, 2.2, 3.3])
    int_val = array.get_as_integer(0)
    real_val = array.get_as_real(1)

    assert int_val.value == 1
    assert str(int_val.identifier) == "id.value.0"

    assert real_val.value == 2.2
    assert str(real_val.identifier) == "id.value.1"


def test_get_invalid_position():
    m = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )

    array = Array(m, [1.1, 2.2, 3.3])

    with pytest.raises(RuntimeError):
        _ = array.get_as_real(5)
