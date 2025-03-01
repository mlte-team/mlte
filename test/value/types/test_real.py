"""
test/value/types/test_real.py

Unit tests for Real.
"""

from __future__ import annotations

from typing import Tuple

import pytest

from mlte.context.context import Context
from mlte.evidence.types.real import Real
from mlte.measurement.measurement import Measurement
from mlte.store.artifact.store import ArtifactStore
from test.store.artifact.fixture import store_with_context  # noqa
from test.value.types.helper import get_sample_evidence_metadata


class DummyMeasurementReal(Measurement):
    def __init__(self, identifier: str):
        super().__init__(identifier)

    def __call__(self) -> Real:
        return Real(3.14).with_metadata(self.evidence_metadata)


def test_success():
    """Integer construction works for valid input."""
    r = Real(3.14).with_metadata(get_sample_evidence_metadata())
    assert r.value == 3.14


def test_fail():
    """Real construction fails for invalid input."""
    with pytest.raises(AssertionError):
        _ = Real(1).with_metadata(get_sample_evidence_metadata())


def test_measurement():
    """Real can be produced by a measurement."""
    m = DummyMeasurementReal("identifier")
    r = m.evaluate()
    assert isinstance(r, Real)
    assert r.value == 3.14


def test_serde() -> None:
    """Real can be converted to model and back."""
    r = Real(3.14).with_metadata(get_sample_evidence_metadata())

    model = r.to_model()
    e = Real.from_model(model)

    assert e == r


def test_save_load(
    store_with_context: Tuple[ArtifactStore, Context]  # noqa
) -> None:
    """Real can be saved to and loaded from artifact store."""
    store, ctx = store_with_context

    i = Real(3.14).with_metadata(get_sample_evidence_metadata())
    i.save_with(ctx, store)

    loaded = Real.load_with("id.value", context=ctx, store=store)
    assert loaded == i


def test_less_than() -> None:
    m = get_sample_evidence_metadata()
    cond = Real.less_than(3.2)

    res = cond.validate(Real(3.1).with_metadata(m))
    assert bool(res)

    res = cond.validate(Real(4.0).with_metadata(m))
    assert not bool(res)

    res = cond.validate(Real(3.2).with_metadata(m))
    assert not bool(res)


def test_less_or_equal_to() -> None:
    m = get_sample_evidence_metadata()
    cond = Real.less_or_equal_to(3.2)

    res = cond.validate(Real(3.1).with_metadata(m))
    assert bool(res)

    res = cond.validate(Real(4.0).with_metadata(m))
    assert not bool(res)

    res = cond.validate(Real(3.2).with_metadata(m))
    assert bool(res)


def test_greater_than() -> None:
    m = get_sample_evidence_metadata()
    cond = Real.greater_than(3.2)

    res = cond.validate(Real(3.1).with_metadata(m))
    assert not bool(res)

    res = cond.validate(Real(4.0).with_metadata(m))
    assert bool(res)

    res = cond.validate(Real(3.2).with_metadata(m))
    assert not bool(res)


def test_greater_or_equal_to() -> None:
    m = get_sample_evidence_metadata()
    cond = Real.greater_or_equal_to(3.2)

    res = cond.validate(Real(3.1).with_metadata(m))
    assert not bool(res)

    res = cond.validate(Real(4.0).with_metadata(m))
    assert bool(res)

    res = cond.validate(Real(3.2).with_metadata(m))
    assert bool(res)
