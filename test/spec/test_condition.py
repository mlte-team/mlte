"""
test/spec/test_condition.py

Unit tests for Conditions.
"""

from __future__ import annotations

from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.spec.condition import Condition
from mlte.spec.model import ConditionModel
from mlte.validation.result import Failure, Success
from mlte.value.types.real import Real


class TestValue:
    """Test value class to test build_condition method."""

    @classmethod
    def in_between(cls, arg1: float, arg2: float) -> Condition:
        """Checks if the value is in between the arguments."""
        condition: Condition = Condition.build_condition(
            lambda real: Success(
                f"Real magnitude {real.value} between {arg1} and {arg2}"
            )
            if real.value > arg1 and real.value < arg2
            else Failure(
                f"Real magnitude {real.value} not between {arg1} and {arg2}"
            )
        )
        return condition


def test_condition_model() -> None:
    """A Condition model can be serialized and deserialized."""
    conditions = [
        ConditionModel(
            name="less_than",
            arguments=[3.0],
            callback="invalid^#*@&^ASD@#",
            value_class="mlte.value.types.real.Real",
        ),
        ConditionModel(
            name="greater_than",
            arguments=[1, 2],
            callback=Condition.encode_callback(
                lambda real: Success("Real magnitude 2 less than threshold 3")
                if 3 < 4
                else Failure("Real magnitude 2 exceeds threshold 1")
            ),
            value_class="mlte.value.types.real.Real",
        ),
    ]

    for object in conditions:
        s = object.to_json()
        d = ConditionModel.from_json(s)
        assert d == object


def test_build_condition():
    """Tests that the build_condition method builds the expected condition."""
    test_value = TestValue()

    condition = test_value.in_between(1, 10)

    assert (
        condition.name == "in_between"
        and condition.arguments == [1, 10]
        and condition.value_class == "test.spec.test_condition.TestValue"
    )


def test_call_condition():
    """Check execution of condition."""
    test_value = TestValue()
    condition = test_value.in_between(1.0, 10.0)
    ev = EvidenceMetadata(
        measurement_type="measure1", identifier=Identifier(name="id")
    )

    result = condition(Real(ev, 3.0))
    assert str(result) == "Success"

    result = condition(Real(ev, 0.0))
    assert str(result) == "Failure"

    result = condition(Real(ev, 1.0))
    assert str(result) == "Failure"
