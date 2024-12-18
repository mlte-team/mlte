"""
test/validation/test_validator.py

Unit tests for Validator.
"""

from mlte.validation.model_condition import ValidatorModel
from mlte.validation.validator import Validator


def get_sample_validator() -> Validator:
    validator = Validator(
        bool_exp=lambda x, y: x > y,  # type: ignore
        success="Test was succesful!",
        failure="Test failed :(",
        info="Only data was attached",
    )
    return validator


def test_validator_model() -> None:
    """A Validator model can be serialized and deserialized."""
    conditions = [
        ValidatorModel(
            bool_exp="ASJDH12384jahsd",
            success="Test was succesful!",
            failure="Test failed :(",
            info="Only data was attached",
            bool_exp_str="test()",
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


def test_validate_success() -> None:
    """The validate() method works as expected."""

    validator = get_sample_validator()
    x = 2
    y = 1

    result = validator.validate(x, y)

    assert (
        validator.success is not None
        and result.message == validator.success + f" - values: [{x}, {y}]"
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
        == validator.success + f' - values: {{"x": {x}, "y": {y}}}'
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
        == validator.success + f' - values: [{x}], {{"y": {y}}}'
    )


def test_validate_failure() -> None:
    """The validate() method works as expected."""

    validator = get_sample_validator()
    x = 1
    y = 2

    result = validator.validate(x, y)

    assert (
        validator.failure is not None
        and result.message == validator.failure + f" - values: [{x}, {y}]"
    )


def test_validate_ignore() -> None:
    """The validate() method works as expected."""

    validator = get_sample_validator()
    validator.bool_exp = None
    x = 1
    y = 2

    result = validator.validate(x, y)

    assert result.message == validator.info
