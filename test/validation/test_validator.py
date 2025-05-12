"""
test/validation/test_validator.py

Unit tests for Validator.
"""

from __future__ import annotations

from typing import Any

import pytest

from mlte._private.fixed_json import json
from mlte._private.function_info import FunctionInfo
from mlte.evidence.metadata import EvidenceMetadata
from mlte.evidence.types.integer import Integer
from mlte.measurement.model import MeasurementMetadata
from mlte.measurement.units import Units
from mlte.model.serialization_error import SerializationError
from mlte.validation.model import ValidatorModel
from mlte.validation.validator import Validator

# -----------------------------------------------------------------------------
# Helpers.
# -----------------------------------------------------------------------------


def get_sample_validator(add_creator: bool = False) -> Validator:
    """Returns a sample validator to be used in tests."""
    validator = Validator(
        bool_exp=lambda x, y: x > y,  # type: ignore
        success="Test was succesful!",
        failure="Test failed :(",
        info="Only data was attached",
        input_types=["builtins.int", "builtins.int"],
    )

    if add_creator:
        validator.creator = FunctionInfo.get_function_info()

    return validator


class JsonValue:
    """A non serializable value that imports __json__"""

    value: Any

    def __json__(self):
        """Hack method to make Artifacts serializable to JSON if importing json-fix before json.dumps."""
        return {"value": "myvalue"}


class TestValue:
    """Test value class to test build_validator method."""

    data: Any

    @classmethod
    def in_between(cls, arg1: float, arg2: float) -> Validator:
        """Checks if the value is in between the arguments."""
        validator: Validator = Validator.build_validator(
            bool_exp=lambda real: real.value > arg1 and real.value < arg2,
            thresholds=[arg1 * Units.meter, arg2],
            success=f"Real magnitude is between {arg1} and {arg2}",
            failure=f"Real magnitude is not between {arg1} and {arg2}",
        )
        return validator

    @classmethod
    def in_between_complex(cls, arg1: float, arg2: TestValue) -> Validator:
        """Checks if the value is in between the arguments."""
        validator: Validator = Validator.build_validator(
            bool_exp=lambda real: real.value > arg1 and arg2.data == str(real),
            thresholds=[arg1 * Units.meter, arg2],
            success=f"Real magnitude is between {arg1} and {arg2}",
            failure=f"Real magnitude is not between {arg1} and {arg2}",
        )
        return validator

    @classmethod
    def json_method(cls, arg1: JsonValue) -> Validator:
        """Checks if the value is in between the arguments."""
        validator: Validator = Validator.build_validator(
            bool_exp=lambda real: real == arg1,
            thresholds=[arg1],
            success=f"Success: {arg1}",
            failure=f"Failure: {arg1}",
        )
        return validator


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


def test_validator_model() -> None:
    """A Validator model can be serialized and deserialized."""
    validators = [
        ValidatorModel(
            bool_exp="ASJDH12384jahsd",
            thresholds=[str(3 * Units.meter)],
            bool_exp_str="test()",
            success="Test was succesful!",
            failure="Test failed :(",
            info="Only data was attached",
        ),
        ValidatorModel(
            bool_exp="ASJDH12384jahsd",
            bool_exp_str="test()",
            thresholds=[str(4 * Units.meter)],
            success="Test was succesful!",
            failure="Test failed :(",
            info="Only data was attached",
            creator_entity="TestClass",
            creator_function="test_validator_model",
            creator_args=[2.3],
        ),
    ]

    for object in validators:
        s = object.to_json()
        d = ValidatorModel.from_json(s)
        assert d == object


def test_round_trip() -> None:
    """Validator can be converted to model and back."""

    validator = get_sample_validator()
    model = validator.to_model()
    loaded_validator = Validator.from_model(model)
    assert validator == loaded_validator

    validator2 = get_sample_validator(add_creator=True)
    model = validator2.to_model()
    loaded_validator = Validator.from_model(model)
    assert validator2 == loaded_validator


def test_build_validator():
    """Tests that the build_validator method builds the expected validator."""
    # fmt: off
    validator = Validator.build_validator(
        bool_exp=lambda x: x == 1,
        thresholds=[1 * Units.meter],
        success="Yay!",
        failure="Aww"
    )
    # fmt: on

    assert validator.bool_exp_str == "lambda x: (x == 1)"
    assert validator.success == "Yay!"
    assert validator.failure == "Aww"
    assert validator.info is None
    assert validator.creator is not None
    assert validator.creator.function_parent == "test.validation.test_validator"
    assert validator.creator.function_name == "test_build_validator"
    assert validator.creator.arguments == []


def test_serialize_from_build():
    """Tests that the build method generates a validator that can be serialized."""
    # fmt: off
    validator = Validator.build_validator(
        bool_exp=lambda x: x == 1,
        thresholds=[1 * Units.meter],
        success="Yay!",
        failure="Aww"
    )
    # fmt: on

    json_str = validator.to_model().to_json()
    loaded = Validator.from_model(ValidatorModel.from_json(json_str))

    assert validator == loaded


def test_validate_success() -> None:
    """The validate() method works as expected."""

    validator = get_sample_validator()
    x = 2
    y = 1

    result = validator.validate(x, y)

    assert (
        validator.success is not None
        and result.message == validator.success + f' - values: ["{x}", "{y}"]'
    )


def test_validate_success_kwargs() -> None:
    """The validate() method works as expected."""

    validator = get_sample_validator()
    x = 2
    y = 1

    result = validator.validate(x=x, y=y)

    assert (
        validator.success is not None
        and result.message
        == validator.success + f' - values: {{"x": "{x}", "y": "{y}"}}'
    )


def test_validate_success_args_and_kwargs() -> None:
    """The validate() method works as expected."""

    validator = get_sample_validator()
    x = 2
    y = 1

    result = validator.validate(x, y=y)

    assert (
        validator.success is not None
        and result.message
        == validator.success + f' - values: ["{x}"], {{"y": "{y}"}}'
    )


def test_validate_failure() -> None:
    """The validate() method works as expected."""

    validator = get_sample_validator()
    x = 1
    y = 2

    result = validator.validate(x, y)

    assert (
        validator.failure is not None
        and result.message == validator.failure + f' - values: ["{x}", "{y}"]'
    )


def test_validate_ignore() -> None:
    """The validate() method works as expected."""

    validator = get_sample_validator()
    validator.bool_exp = None
    x = 1
    y = 2

    result = validator.validate(x, y)

    assert result.message == validator.info


def test_validate_success_with_evidence() -> None:
    """The validate() method works as expected with Evidence."""

    validator = Integer.less_or_equal_to(2)

    result = validator.validate(
        Integer(value=1).with_metadata(
            evidence_metadata=EvidenceMetadata(
                test_case_id="test",
                measurement=MeasurementMetadata(
                    measurement_class="mlte.measurement.external_measurement.ExternalMeasurement",
                    output_class="mlte.evidence.types.real.Real",
                    additional_data={"function": "skleran.accu()"},
                ),
            ),
        )
    )

    assert (
        validator.success is not None
        and result.message == validator.success + ' - values: ["1"]'
    )


def test_invalid_input_types() -> None:
    """Tests that validate is checking input types."""

    validator = get_sample_validator()
    x = 1

    with pytest.raises(RuntimeError):
        _ = validator.validate(x)

    with pytest.raises(RuntimeError):
        _ = validator.validate(x, x, x)

    with pytest.raises(RuntimeError):
        _ = validator.validate(x, "a")

    with pytest.raises(RuntimeError):
        _ = validator.validate(x, Integer(1))


def test_non_serializable_argument():
    validator = TestValue.in_between_complex(1.0, TestValue())

    with pytest.raises(SerializationError):
        _ = validator.to_model().to_json()


def test_json_fix_serializable_argument():
    test_value = JsonValue()
    validator = TestValue.json_method(test_value)

    json_data = validator.to_model().to_json()
    _ = json.dumps(json_data)
