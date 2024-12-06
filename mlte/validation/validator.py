"""
mlte/validation/validator.py

The validation base class.
"""

from __future__ import annotations

import json
import typing
from typing import Any, Callable, Optional

from mlte._private import serializing
from mlte.validation.model_condition import ValidatorModel
from mlte.validation.result import Failure, Ignore, Result, Success


class Validator:
    def __init__(
        self,
        bool_exp: Optional[Callable[[Any], bool]] = None,
        success: str = "Success message not set",
        failure: str = "Failure message not set",
        ignore: str = "Default message not set",
    ):
        """
        Constructor.

        :param bool_exp: A boolean expression that can be used to test the actual condition we want to validate.
        :param success: A string indicating the message to record in case of success (bool_exp evaluating to True).
        :param failure: A string indicating the message to record in case of failure (bool_exp evaluating to False).
        :param ignore: A string indicating the message to record in case no bool expression is passed (no condition, just recording information).
        """
        self.bool_exp = bool_exp
        self.success = success
        self.failure = failure
        self.ignore = ignore

    def validate(self, *args, **kwargs) -> Result:
        """
        Generates a result based on the arguments received, and the configured params in the Validator.

        :param args, kwargs: Arguments to pass to the boolean expression to be evaluated in this specific case.
        :return: A Result with a message with details of the validation result.
        """
        values = f"- values: {json.dumps(args) if len(args)>0 else ''}{', ' if len(args)>0 and len(kwargs)>0 else''}{json.dumps(kwargs) if len(kwargs)>0 else ''}"
        result = (
            Ignore(self.ignore)
            if self.bool_exp is None
            else Success(f"{self.success} {values}")
            if self.bool_exp(*args, **kwargs)
            else Failure(f"{self.failure} {values}")
        )
        return result

    # -------------------------------------------------------------------------
    # Model handling.
    # -------------------------------------------------------------------------

    def to_model(self) -> ValidatorModel:
        """
        Returns this validator as a model.

        :return: The serialized model object.
        """
        return ValidatorModel(
            bool_exp=serializing.encode_callable(self.bool_exp)
            if self.bool_exp
            else None,
            success=self.success,
            failure=self.failure,
            ignore=self.ignore,
        )

    @classmethod
    def from_model(cls, model: ValidatorModel) -> Validator:
        """
        Deserialize a Validator from a model.

        :param model: The model.

        :return: The deserialized Validator
        """
        validator: Validator = Validator(
            bool_exp=typing.cast(
                Callable[[Any], bool],
                serializing.decode_callable(model.bool_exp),
            )
            if model.bool_exp
            else None,
            success=model.success,
            failure=model.failure,
            ignore=model.ignore,
        )
        return validator

    # -------------------------------------------------------------------------
    # Equality Testing
    # -------------------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        """Compare Validator instances for equality."""
        if not isinstance(other, Validator):
            return False
        reference: Validator = other
        return self.to_model() == reference.to_model()
