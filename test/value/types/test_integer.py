"""
test/value/types/test_integer.py

Unit tests for Integer.
"""

import pytest

from mlte.context.context import Context
from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.measurement import Measurement
from mlte.store.base import Store
from mlte.value.types.integer import Integer

from ...fixture.store import store_with_context  # noqa


class DummyMeasurementInteger(Measurement):
    def __init__(self, identifier: str):
        super().__init__(self, identifier)

    def __call__(self) -> Integer:
        return Integer(self.metadata, 1)


def test_success():
    """Integer construction works for valid input type."""
    m = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )
    i = Integer(m, 1)
    assert i.value == 1


def test_fail():
    """Integer construction fails for invalid input type."""
    m = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )
    with pytest.raises(AssertionError):
        _ = Integer(m, 3.14)  # type: ignore


def test_measurement():
    """Integer can be produced by measurement."""

    m = DummyMeasurementInteger("identifier")
    i = m.evaluate()
    assert isinstance(i, Integer)
    assert i.value == 1


def test_serde() -> None:
    """Integer can be converted to model and back."""
    m = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )
    i = Integer(m, 1)

    model = i.to_model()
    e = Integer.from_model(model)

    assert e == i


def test_save_load(store_with_context: tuple[Store, Context]) -> None:  # noqa
    """Integer can be saved to and loaded from artifact store."""
    store, ctx = store_with_context

    m = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )
    i = Integer(m, 1)
    i.save_with(ctx, store)

    loaded = Integer.load_with("id.value", ctx, store)
    assert loaded == i
