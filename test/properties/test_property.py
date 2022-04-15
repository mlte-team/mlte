"""
Unit tests for basic Property functionality.
"""

import pytest
from typing import Dict, Any

from mlte.properties import Property
from mlte.measurement import Measurement


class DummyProperty(Property):
    def __init__(self, *measurements: Measurement):
        super().__init__("DummyProperty", *measurements)


class DummyMeasurement0(Measurement):
    def __init__(self):
        super().__init__("DummyMeasurement0")

    def __call__(self, value: bool) -> Dict[str, Any]:
        return {"value": value}


class DummyMeasurement1(Measurement):
    def __init__(self):
        super().__init__("DummyMeasurement1")

    def __call__(self, value: bool) -> Dict[str, Any]:
        return {"value": value}


def test_multiple_measurements():
    # Construction with multiple, unique measurements should succeed
    _ = DummyProperty(DummyMeasurement0(), DummyMeasurement1())
    assert True


def test_duplicate_measurements_0():
    with pytest.raises(RuntimeError):
        _ = DummyProperty(DummyMeasurement0(), DummyMeasurement0())


def test_duplicate_measurements_1():
    p = DummyProperty(DummyMeasurement0())
    with pytest.raises(RuntimeError):
        p.add_measurement(DummyMeasurement0())
