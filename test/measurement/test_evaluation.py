"""
Unit tests for measurement evaluation functionality.
"""

import pytest
from typing import Dict, Any

from mlte.measurement import Measurement
from mlte.measurement.evaluation import Opaque, Integer, Real


class DummyMeasurementOpaque(Measurement):
    def __init__(self):
        super().__init__("DummyMeasurementOpaque")

    def __call__(self) -> Dict[str, Any]:
        return {"value": 1}


def test_opaque():
    m = DummyMeasurementOpaque()
    t = m.evaluate()
    assert isinstance(t, Opaque)

    assert "value" in t.data
    assert t.data["value"] == 1

    # Opaque is subscriptable, like a dictionary
    assert t["value"] == t.data["value"]

    # Opaque raises for invalid key
    with pytest.raises(KeyError):
        _ = t["foo"]

    # Opaque is read-only
    with pytest.raises(ValueError):
        t["value"] = 2  # type: ignore


class DummyMeasurementInteger(Measurement):
    def __init__(self):
        super().__init__("DummyMeasurementInteger")

    def __call__(self) -> Dict[str, Any]:
        return {"value": 1}

    def semantics(self, data: Dict[str, Any]) -> Integer:
        return Integer(self, data["value"])


def test_integer_success():
    # Ensure instantiation succeeds for valid type
    m = DummyMeasurementInteger()
    i = Integer(m, 1)
    assert i.value == 1


def test_integer_fail():
    # Ensure instantiation fails for invalid type
    m = DummyMeasurementInteger()
    with pytest.raises(AssertionError):
        _ = Integer(m, 3.14)  # type: ignore


def test_integer_e2e():
    m = DummyMeasurementInteger()
    i = m.evaluate()
    assert isinstance(i, Integer)
    assert i.value == 1


class DummyMeasurementReal(Measurement):
    def __init__(self):
        super().__init__("DummyMeasurementReal")

    def __call__(self) -> Dict[str, Any]:
        return {"value": 3.14}

    def semantics(self, data: Dict[str, Any]) -> Real:
        return Real(self, data["value"])


def test_real_success():
    # Ensure instantiation succeeds for valid type
    m = DummyMeasurementReal()
    r = Real(m, 3.14)
    assert r.value == 3.14


def test_real_fail():
    m = DummyMeasurementReal()
    with pytest.raises(AssertionError):
        _ = Real(m, 1)


def test_real_e2e():
    m = DummyMeasurementReal()
    r = m.evaluate()
    assert isinstance(r, Real)
    assert r.value == 3.14
