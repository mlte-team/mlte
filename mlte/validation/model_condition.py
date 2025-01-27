"""
mlte/validation/model_condition.py

Model implementation for the Validator and Condition.
"""

from typing import Any, Optional

from mlte._private.fixed_json import json
from mlte.model.base_model import BaseModel


class ValidatorModel(BaseModel):
    """A description of a validator for a test."""

    bool_exp: Optional[str]
    """A text-encoded, dilled-serialized version of the function to execute when checking the bool condition."""

    bool_exp_str: Optional[str]
    """A string representation of the code for the bool expression to check for."""

    success: Optional[str]
    """A string to be used when recording that the validation was succesful."""

    failure: Optional[str]
    """A string to be used when recording that the validation was not succesful."""

    info: Optional[str]
    """A string to be used when recording that the validation was not checked against a condition, just recorded information."""

    creator_class: Optional[str] = None
    """The name of the class used to create this validator, if any."""

    creator_function: Optional[str] = None
    """The name of the function used to create this validator, if any."""

    creator_args: list[Any] = []
    """The arguments of the function used to create this validator, if any."""


class ConditionModel(BaseModel):
    """A description of a condition for a property."""

    name: str
    """A decriptive name for the condition, usually the method name used to call it."""

    arguments: list[Any] = []
    """The arguments used when validating the condition."""

    validator: ValidatorModel
    """A serialized version of the validator to execute when validating this condition."""

    value_class: Optional[str]
    """A string indicating the full module and class name of the Value used to generate this condition, if any."""

    def args_to_json_str(self) -> str:
        """
        Serialize the model arguments field into a string.
        :return: The JSON str representation of the model
        """
        # First convert whole thing, to see if arguments will trigger error (and if so, just let it bubble up).
        self.to_json()

        # Now convert only the actual arguments not only to JSON, but to a JSON string.
        json_str_args = json.dumps(self.arguments)
        return json_str_args
