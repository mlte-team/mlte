"""
test/value/types/test_integer.py

Unit tests for Integer.
"""

from __future__ import annotations

from typing import Optional, Tuple

import pytest

from mlte.context.context import Context
from mlte.evidence.types.integer import Integer
from mlte.measurement.measurement import Measurement
from mlte.measurement.units import Unit, Units
from mlte.store.artifact.store import ArtifactStore
from test.evidence.types.helper import get_sample_evidence_metadata
from test.store.artifact.fixture import store_with_context  # noqa


class DummyMeasurementInteger(Measurement):
    def __init__(self, identifier: str):
        super().__init__(identifier)

    def __call__(self) -> Integer:
        return Integer(1)


@pytest.mark.parametrize("number,unit", [(1, None), (2, Units.meter)])
def test_success(number: int, unit: Optional[Unit]):
    """Integer construction works for valid input type."""
    i = Integer(number, unit).with_metadata(get_sample_evidence_metadata())
    assert i.value == number
    assert i.unit == unit


def test_fail():
    """Integer construction fails for invalid input type."""

    with pytest.raises(AssertionError):
        _ = Integer(3.14).with_metadata(get_sample_evidence_metadata())  # type: ignore


def test_measurement():
    """Integer can be produced by measurement."""

    m = DummyMeasurementInteger("identifier")
    i = m.evaluate()
    assert isinstance(i, Integer)
    assert i.value == 1


def test_serde() -> None:
    """Integer can be converted to model and back."""
    i = Integer(1, unit=Units.meter).with_metadata(
        get_sample_evidence_metadata()
    )

    model = i.to_model()
    e = Integer.from_model(model)

    assert e == i


def test_save_load(
    store_with_context: Tuple[ArtifactStore, Context]  # noqa
) -> None:
    """Integer can be saved to and loaded from artifact store."""
    store, ctx = store_with_context

    i = Integer(1, unit=Units.kilobyte).with_metadata(
        get_sample_evidence_metadata()
    )
    i.save_with(ctx, store)

    loaded = Integer.load_with("evidence.test_id", context=ctx, store=store)
    assert loaded == i


def test_less_than() -> None:
    m = get_sample_evidence_metadata()

    validator = Integer.less_than(3)

    res = validator.validate(Integer(2).with_metadata(m))
    assert bool(res)

    res = validator.validate(Integer(4).with_metadata(m))
    assert not bool(res)

    res = validator.validate(Integer(3).with_metadata(m))
    assert not bool(res)


def test_less_or_equal_to() -> None:
    m = get_sample_evidence_metadata()

    validator = Integer.less_or_equal_to(3)

    res = validator.validate(Integer(2).with_metadata(m))
    assert bool(res)

    res = validator.validate(Integer(4).with_metadata(m))
    assert not bool(res)

    res = validator.validate(Integer(3).with_metadata(m))
    assert bool(res)
