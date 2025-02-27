"""
test/value/types/test_integer.py

Unit tests for Integer.
"""

from __future__ import annotations

from typing import Tuple

import pytest

from mlte.context.context import Context
from mlte.evidence.types.integer import Integer
from mlte.measurement.measurement import Measurement
from mlte.store.artifact.store import ArtifactStore
from test.store.artifact.fixture import store_with_context  # noqa
from test.value.types.helper import get_sample_evidence_metadata


class DummyMeasurementInteger(Measurement):
    def __init__(self, identifier: str):
        super().__init__(identifier)

    def __call__(self) -> Integer:
        return Integer(self.evidence_metadata, 1)


def test_success():
    """Integer construction works for valid input type."""
    i = Integer(get_sample_evidence_metadata(), 1)
    assert i.value == 1


def test_fail():
    """Integer construction fails for invalid input type."""

    with pytest.raises(AssertionError):
        _ = Integer(get_sample_evidence_metadata(), 3.14)  # type: ignore


def test_measurement():
    """Integer can be produced by measurement."""

    m = DummyMeasurementInteger("identifier")
    i = m.evaluate()
    assert isinstance(i, Integer)
    assert i.value == 1


def test_serde() -> None:
    """Integer can be converted to model and back."""
    i = Integer(get_sample_evidence_metadata(), 1)

    model = i.to_model()
    e = Integer.from_model(model)

    assert e == i


def test_save_load(
    store_with_context: Tuple[ArtifactStore, Context]  # noqa
) -> None:
    """Integer can be saved to and loaded from artifact store."""
    store, ctx = store_with_context

    i = Integer(get_sample_evidence_metadata(), 1)
    i.save_with(ctx, store)

    loaded = Integer.load_with("id.value", context=ctx, store=store)
    assert loaded == i


def test_less_than() -> None:
    m = get_sample_evidence_metadata()

    cond = Integer.less_than(3)

    res = cond(Integer(m, 2))
    assert bool(res)

    res = cond(Integer(m, 4))
    assert not bool(res)

    res = cond(Integer(m, 3))
    assert not bool(res)


def test_less_or_equal_to() -> None:
    m = get_sample_evidence_metadata()

    cond = Integer.less_or_equal_to(3)

    res = cond(Integer(m, 2))
    assert bool(res)

    res = cond(Integer(m, 4))
    assert not bool(res)

    res = cond(Integer(m, 3))
    assert bool(res)
