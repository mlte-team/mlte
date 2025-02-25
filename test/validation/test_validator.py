"""
test/validation/test_validator.py

Unit tests for Validator.
"""

from mlte._private.function_info import FunctionInfo
from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.validation.model_condition import ValidatorModel
from mlte.validation.validator import Validator
from mlte.value.types.integer import Integer


def get_sample_validator(add_creator: bool = False) -> Validator:
    validator = Validator(
        bool_exp=lambda x, y: x > y,  # type: ignore
        success="Test was succesful!",
        failure="Test failed :(",
        info="Only data was attached",
    )

    if add_creator:
        validator.creator = FunctionInfo.get_function_info()

    return validator


def test_validator_model() -> None:
    """A Validator model can be serialized and deserialized."""
    conditions = [
        ValidatorModel(
            bool_exp="ASJDH12384jahsd",
            bool_exp_str="test()",
            success="Test was succesful!",
            failure="Test failed :(",
            info="Only data was attached",
        ),
        ValidatorModel(
            bool_exp="ASJDH12384jahsd",
            bool_exp_str="test()",
            success="Test was succesful!",
            failure="Test failed :(",
            info="Only data was attached",
            creator_class="TestClass",
            creator_function="test_validator_model",
            creator_args=[2.3],
        ),
    ]

    for object in conditions:
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
        success="Yay!",
        failure="Aww"
    )
    # fmt: on

    assert validator.bool_exp_str == "lambda x: (x == 1)"
    assert validator.success == "Yay!"
    assert validator.failure == "Aww"
    assert validator.info is None
    assert validator.creator is not None
    assert validator.creator.function_class == ""
    assert validator.creator.function_name == "test_build_validator"
    assert validator.creator.arguments == []


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


def test_validate_success_with_value() -> None:
    """The validate() method works as expected with a Value."""

    validator = Integer.less_or_equal_to(2).validator

    result = validator.validate(
        Integer(
            value=1,
            metadata=EvidenceMetadata(
                measurement_type="test", identifier=Identifier(name="test")
            ),
        )
    )

    assert (
        validator.success is not None
        and result.message == validator.success + ' - values: ["1"]'
    )
