"""
test/spec/test_condition.py

Unit tests for Conditions.
"""

from __future__ import annotations

from mlte.spec.condition import Condition
from mlte.spec.model import ConditionModel
from mlte.validation.result import Failure, Success


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
