"""
mlte/validation/model_condition.py

Model implementation for the Validator and Condition.
"""

import json
from typing import Any, Optional

# The json-fix library is loaded to patch json.dumps so it automatically calls
#  a .__json__ method if defined in a class being serialized.
import json_fix  # noqa

from mlte.model.base_model import BaseModel


class ValidatorModel(BaseModel):
    """A description of a validator for a test."""

    bool_exp: Optional[str]
    """A text-encoded, dilled-serialized version of the function to execute when checking the bool condition."""

    success: Optional[str]
    """A string to be used when recording that the validation was succesful."""

    failure: Optional[str]
    """A string to be used when recording that the validation was not succesful."""

    ignore: Optional[str]
    """A string to be used when recording that the validation was not checked against a condition, just recorded information."""


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