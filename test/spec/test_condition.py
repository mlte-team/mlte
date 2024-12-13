"""
test/spec/test_condition.py

Unit tests for Conditions.
"""

from __future__ import annotations

from typing import Any

import pytest

from mlte._private.fixed_json import json
from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.model.serialization_error import SerializationError
from mlte.spec.condition import Condition
from mlte.validation.model_condition import ConditionModel
from mlte.validation.validator import Validator
from mlte.value.types.integer import Integer
from mlte.value.types.real import Real


class JsonValue:
    """A non serializable value that imports __json__"""

    value: Any

    def __json__(self):
        """Hack method to make Artifacts serializable to JSON if importing json-fix before json.dumps."""
        return {"value": "myvalue"}


class TestValue:
    """Test value class to test build_condition method."""

    data: Any

    @classmethod
    def in_between(cls, arg1: float, arg2: float) -> Condition:
        """Checks if the value is in between the arguments."""
        condition: Condition = Condition.build_condition(
            bool_exp=lambda real: real.value > arg1 and real.value < arg2,
            success=f"Real magnitude is between {arg1} and {arg2}",
            failure=f"Real magnitude is not between {arg1} and {arg2}",
        )
        return condition

    @classmethod
    def in_between_complex(cls, arg1: float, arg2: TestValue) -> Condition:
        """Checks if the value is in between the arguments."""
        condition: Condition = Condition.build_condition(
            bool_exp=lambda real: real.value > arg1 and real.value < arg2,
            success=f"Real magnitude is between {arg1} and {arg2}",
            failure=f"Real magnitude is not between {arg1} and {arg2}",
        )
        return condition

    @classmethod
    def json_method(cls, arg1: JsonValue) -> Condition:
        """Checks if the value is in between the arguments."""
        condition: Condition = Condition.build_condition(
            bool_exp=lambda real: real == 1,
            success=f"Success: {arg1}",
            failure=f"Failure: {arg1}",
        )
        return condition


def test_condition_model() -> None:
    """A Condition model can be serialized and deserialized."""
    conditions = [
        ConditionModel(
            name="less_than",
            arguments=[3.0],
            validator=Validator(success="Yay", failure="oh").to_model(),
            value_class="mlte.value.types.real.Real",
        ),
        ConditionModel(
            name="greater_than",
            arguments=[1, 2],
            validator=Validator(success="Yay", failure="oh").to_model(),
            value_class="mlte.value.types.real.Real",
        ),
    ]

    for object in conditions:
        s = object.to_json()
        d = ConditionModel.from_json(s)
        assert d == object


def test_build_condition():
    """Tests that the build_condition method builds the expected condition."""
    condition = TestValue.in_between(1, 10)

    assert (
        condition.name == "in_between"
        and condition.arguments == [1, 10]
        and condition.value_class == "test.spec.test_condition.TestValue"
    )


def test_save_load_condition():
    """Tests that the build_condition method generates a condition that can be saved and loaded."""
    condition = TestValue.in_between(1.0, 10.0)

    json_str = condition.to_model().to_json()
    loaded = Condition.from_model(ConditionModel.from_json(json_str))

    assert condition == loaded


def test_call_condition():
    """Check execution of condition."""
    condition = TestValue.in_between(1.0, 10.0)
    ev = EvidenceMetadata(
        measurement_type="measure1", identifier=Identifier(name="id")
    )

    result = condition(Real(ev, 3.0))
    assert str(result) == "Success"

    result = condition(Real(ev, 0.0))
    assert str(result) == "Failure"

    result = condition(Real(ev, 11.0))
    assert str(result) == "Failure"


def test_round_trip() -> None:
    """Condition can be converted to model and back."""

    condition = TestValue.in_between(1, 10)

    model = condition.to_model()
    loaded = Condition.from_model(model)

    assert condition == loaded

    condition = Integer.less_than(3)
    model = condition.to_model()
    loaded = Condition.from_model(model)

    assert condition == loaded


def test_non_serializable_argument():
    condition = TestValue.in_between_complex(1.0, TestValue())

    with pytest.raises(SerializationError):
        _ = condition.to_model().to_json()


def test_json_fix_serializable_argument():
    test_value = JsonValue()
    condition = TestValue.json_method(test_value)

    json_data = condition.to_model().to_json()
    _ = json.dumps(json_data)
