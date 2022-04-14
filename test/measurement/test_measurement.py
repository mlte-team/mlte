"""
Unit tests for base Measurement functionality.
"""

import pytest
from typing import Dict, Any

from mlte.measurement import Measurement
from mlte.measurement.evaluation import EvaluationResult
from mlte.measurement.validation import Validator, Success


class DummyEvaluationResult(EvaluationResult):
    def __init__(self, measurement, value: bool):
        super().__init__(measurement)
        self.value = value


class DummyMeasurement(Measurement):
    """A dummy measurement for unit tests."""

    def __init__(self):
        super().__init__("DummyMeasurement")

    def __call__(self, value: bool) -> Dict[str, Any]:
        return {"value": value}

    def semantics(self, data: Dict[str, Any]) -> DummyEvaluationResult:
        return DummyEvaluationResult(self, data["value"])


def test_execution():
    p = DummyMeasurement()
    r = p(True)
    assert "value" in r
    assert r["value"]

    p = DummyMeasurement()
    r = p(False)
    assert "value" in r
    assert not r["value"]


def test_evaluation():
    p = DummyMeasurement()
    r = p.evaluate(True)
    assert isinstance(r, DummyEvaluationResult)
    assert r.value

    p = DummyMeasurement()
    r = p.evaluate(False)
    assert isinstance(r, DummyEvaluationResult)
    assert not r.value


def test_validation():
    # Attempt to add duplicate validators
    p = DummyMeasurement()
    p.add_validator(Validator("Test", lambda _: Success()))
    with pytest.raises(RuntimeError):
        p.add_validator(Validator("Test", lambda _: Success()))

    # Attempt to ignore a measurement with a validator
    p = DummyMeasurement()
    p.add_validator(Validator("Test", lambda _: Success()))
    with pytest.raises(RuntimeError):
        p.ignore("I don't care about validation.")

    # Attempt to add validator to ignored measurement
    p = DummyMeasurement()
    p.ignore("I don't care about validation.")
    with pytest.raises(RuntimeError):
        p.add_validator(Validator("Test", lambda _: Success()))
