"""
mlte/validation/validator.py

The validation base class.
"""

from __future__ import annotations

import json
import typing
from typing import Any, Callable, Optional

# The json-fix library is loaded to patch json.dumps so it automatically calls
#  a .__json__ method if defined in a class being serialized.
import json_fix  # noqa

from mlte._private import serializing
from mlte.validation.model_condition import ValidatorModel
from mlte.validation.result import Failure, Ignore, Result, Success


class Validator:
    def __init__(
        self,
        bool_exp: Optional[Callable[[Any], bool]] = None,
        success: Optional[str] = None,
        failure: Optional[str] = None,
        ignore: Optional[str] = None,
    ):
        """
        Constructor.

        :param bool_exp: A boolean expression that can be used to test the actual condition we want to validate.
        :param success: A string indicating the message to record in case of success (bool_exp evaluating to True).
        :param failure: A string indicating the message to record in case of failure (bool_exp evaluating to False).
        :param ignore: A string indicating the message to record in case no bool expression is passed (no condition, just recording information).
        """
        if success is not None and failure is None:
            raise ValueError(
                "If success message is defined, failure message has to be defined as well"
            )
        if success is None and failure is not None:
            raise ValueError(
                "If failure message is defined, success message has to be defined as well"
            )
        if success is None and failure is None and ignore is None:
            raise ValueError(
                "All messages can't be empty, either ignore or success and failure have to be defined"
            )

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
        result_value: Optional[bool]
        if self.bool_exp is None:
            result_value = None
        else:
            result_value = self.bool_exp(*args, **kwargs)
            if not isinstance(result_value, bool):
                raise ValueError(
                    "Configured bool expression does not return a bool."
                )

        values = f"- values: {json.dumps(args) if len(args)>0 else ''}{', ' if len(args)>0 and len(kwargs)>0 else''}{json.dumps(kwargs) if len(kwargs)>0 else ''}"
        result = (
            Ignore(self.ignore)
            if self.bool_exp is None and self.ignore is not None
            else Success(f"{self.success} {values}")
            if result_value
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
