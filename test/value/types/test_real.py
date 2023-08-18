"""
test/value/types/test_real.py

Unit tests for Real.
"""

from __future__ import annotations

from typing import Tuple

import pytest

from mlte.context.context import Context
from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.measurement import Measurement
from mlte.store.base import Store
from mlte.value.types.real import Real

from ...fixture.store import store_with_context  # noqa


class DummyMeasurementReal(Measurement):
    def __init__(self, identifier: str):
        super().__init__(self, identifier)

    def __call__(self) -> Real:
        return Real(self.metadata, 3.14)


def test_success():
    """Integer construction works for valid input."""
    m = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )
    r = Real(m, 3.14)
    assert r.value == 3.14


def test_fail():
    """Real construction fails for invalid input."""
    m = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )
    with pytest.raises(AssertionError):
        _ = Real(m, 1)


def test_measurement():
    """Real can be produced by a measurement."""
    m = DummyMeasurementReal("identifier")
    r = m.evaluate()
    assert isinstance(r, Real)
    assert r.value == 3.14


def test_serde() -> None:
    """Real can be converted to model and back."""
    m = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )
    r = Real(m, 3.14)

    model = r.to_model()
    e = Real.from_model(model)

    assert e == r


def test_save_load(store_with_context: Tuple[Store, Context]) -> None:  # noqa
    """Real can be saved to and loaded from artifact store."""
    store, ctx = store_with_context

    m = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )
    i = Real(m, 3.14)
    i.save_with(ctx, store)

    loaded = Real.load_with("id.value", ctx, store)
    assert loaded == i
