"""
Unit tests for base Property functionality.
"""

import pytest
from typing import Dict, Any

from mlte.properties import Property
from mlte.properties.evaluation import EvaluationResult
from mlte.properties.validation import Validator, Success, Failure, Ignore


class DummyEvaluationResult(EvaluationResult):
    def __init__(self, property, value: bool):
        super().__init__(property)
        self.value = value


class DummyProperty(Property):
    """A dummy property for unit tests."""

    def __init__(self):
        super().__init__("DummyProperty")

    def __call__(self, value: bool) -> Dict[str, Any]:
        return {"value": value}

    def semantics(self, data: Dict[str, Any]) -> DummyEvaluationResult:
        return DummyEvaluationResult(self, data["value"])


def test_execution():
    p = DummyProperty()
    r = p(True)
    assert "value" in r
    assert r["value"]

    p = DummyProperty()
    r = p(False)
    assert "value" in r
    assert not r["value"]


def test_evaluation():
    p = DummyProperty()
    r = p.evaluate(True)
    assert isinstance(r, DummyEvaluationResult)
    assert r.value

    p = DummyProperty()
    r = p.evaluate(False)
    assert isinstance(r, DummyEvaluationResult)
    assert not r.value


def test_validation():
    # Attempt to add duplicate validators
    p = DummyProperty()
    p.add_validator(Validator("Test", lambda _: Success()))
    with pytest.raises(RuntimeError):
        p.add_validator(Validator("Test", lambda _: Success()))

    # Attempt to ignore a property with a validator
    p = DummyProperty()
    p.add_validator(Validator("Test", lambda _: Success()))
    with pytest.raises(RuntimeError):
        p.ignore("I don't care about validation.")

    # Attempt to add validator to ignored property
    p = DummyProperty()
    p.ignore("I don't care about validation.")
    with pytest.raises(RuntimeError):
        p.add_validator(Validator("Test", lambda _: Success()))
