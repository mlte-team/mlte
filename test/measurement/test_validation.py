"""
Unit tests for measurement validation functionality.
"""

from typing import Dict, Any

from mlte.measurement import Measurement
from mlte.measurement.validation import Bound, Unbound


class DummyMeasurement0(Measurement):
    def __init__(self):
        super().__init__("DummyMeasurement0")

    def __call__(self) -> Dict[str, Any]:
        return {"value": True}


class DummyMeasurement1(Measurement):
    def __init__(self):
        super().__init__("DummyMeasurement1")

    def __call__(self) -> Dict[str, Any]:
        return {"value": True}


def test_unbound_equality():
    assert Unbound() == Unbound()


def test_bound_equality():
    m = DummyMeasurement0()
    a = Bound(m, "p0", "p1")
    b = Bound(m, "p0", "p1")
    assert a == b

    # Order does not matter
    a = Bound(m, "p1", "p0")
    b = Bound(m, "p0", "p1")
    assert a == b


def test_bound_inequality():
    m = DummyMeasurement0()
    a = Bound(m, "p0", "p1")
    b = Bound(m, "p0")
    assert a != b

    k = DummyMeasurement1()
    a = Bound(m, "p0", "p1")
    b = Bound(k, "p0", "p1")
    assert a != b
