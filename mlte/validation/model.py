"""
Model implementation for the Validator.
"""

from typing import Any, Optional

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
    """A string to be used when recording that the validation was not checked against a expression, just recorded information."""

    input_types: list[str] = []
    """A list of strings representing the types of inputs to be received when validating."""

    creator_entity: Optional[str] = None
    """The full name of the class or module used to create this validator, if any."""

    creator_function: Optional[str] = None
    """The name of the function used to create this validator, if any."""

    creator_args: list[Any] = []
    """The arguments of the function used to create this validator, if any."""
