"""
mlte/validation/validator.py

The validation base class.
"""

from __future__ import annotations

import inspect
import typing
from types import FrameType
from typing import Any, Callable, Optional

from mlte._private import reflection, serializing
from mlte._private.fixed_json import json
from mlte._private.function_info import FunctionInfo
from mlte.model.base_model import BaseModel
from mlte.model.serializable import Serializable
from mlte.validation.model_validator import ValidatorModel
from mlte.validation.result import Failure, Info, Result, Success


class Validator(Serializable):
    """
    Class that represents a validation, including condition, and results for success or failure.
    """

    def __init__(
        self,
        *,
        bool_exp: Optional[Callable[[Any], bool]] = None,
        success: Optional[str] = None,
        failure: Optional[str] = None,
        info: Optional[str] = None,
        creator: Optional[FunctionInfo] = None,
    ):
        """
        Constructor.

        :param bool_exp: A boolean expression that can be used to test the actual condition we want to validate.
        :param success: A string indicating the message to record in case of success (bool_exp evaluating to True).
        :param failure: A string indicating the message to record in case of failure (bool_exp evaluating to False).
        :param info: A string indicating the message to record in case no bool expression is passed (no condition, just recording information).
        :param creator: Information about the class and method that created this validator, if any.
        """
        if success is not None and failure is None:
            raise ValueError(
                "If success message is defined, failure message has to be defined as well"
            )
        if success is None and failure is not None:
            raise ValueError(
                "If failure message is defined, success message has to be defined as well"
            )
        if success is None and failure is None and info is None:
            raise ValueError(
                "All messages can't be empty, either info or success and failure have to be defined"
            )

        self.bool_exp = bool_exp
        self.success = success
        self.failure = failure
        self.info = info
        self.creator = creator

        self.bool_exp_str = (
            reflection.get_lambda_code(bool_exp)
            if bool_exp is not None
            else None
        )
        """We also store the bool expression as a string from its code, for tracking purposes."""

    @staticmethod
    def build_validator(
        bool_exp: Optional[Callable[[Any], bool]] = None,
        success: Optional[str] = None,
        failure: Optional[str] = None,
        info: Optional[str] = None,
        caller_function: Optional[FrameType] = None,
    ) -> Validator:
        """
        Creates a Validator using the provided test, extracting context info from the function that called us.

        :param bool_exp: A boolean expression that can be used to test the actual condition we want to validate.
        :param success: A string indicating the message to record in case of success (bool_exp evaluating to True).
        :param failure: A string indicating the message to record in case of failure (bool_exp evaluating to False).
        :param info: A string indicating the message to record in case no bool expression is passed (no condition, just recording information).
        :param caller_function: A FrameType with data about function that originally called this function. SHOULD BE REMOVED WHEN CONDITIONS ARE.

        :returns: A Validator, potentially with caller creator information.
        """
        # Get function info, passing our caller as argument.
        if caller_function is None:
            curr_frame = inspect.currentframe()
            caller_function = (
                curr_frame.f_back if curr_frame is not None else None
            )
        function_info = FunctionInfo.get_function_info(caller_function)

        # Build the validator. We can't really check at this point if the bool_exp actually returns a bool.
        validator = Validator(
            bool_exp=bool_exp,
            success=success,
            failure=failure,
            info=info,
            creator=function_info,
        )
        return validator

    def validate(self, *args, **kwargs) -> Result:
        """
        Generates a result based on the arguments received, and the configured attributes in the Validator.

        :param args, kwargs: Arguments to pass to the boolean expression to be evaluated in this specific case.
        :return: A Result, including a message with details about the validation result.
        """
        if self.bool_exp is None and self.info is None:
            raise RuntimeError(
                "Can't validate, Validator has no bool expression and is also missing informational message that is used in those cases."
            )

        # First execute bool expression (if any), and get its boolean result.
        executed_bool_exp_value: Optional[bool] = None
        if self.bool_exp is not None:
            executed_bool_exp_value = self.bool_exp(*args, **kwargs)
            if not isinstance(executed_bool_exp_value, bool):
                raise ValueError(
                    "Configured bool expression does not return a bool."
                )

        # Create the result to be returned.
        values_str = self._args_to_string(*args, **kwargs)
        result = (
            Info(self.info)
            if self.bool_exp is None and self.info is not None
            else (
                Success(f"{self.success} {values_str}")
                if executed_bool_exp_value
                else Failure(f"{self.failure} {values_str}")
            )
        )
        return result

    def _args_to_string(self, *args, **kwargs) -> str:
        """
        Stringify arguments so that result's message can include generic information about arguments used when validating.
        """
        # First ensure args are turned to string separately, to allow them to use their own str()
        MAX_STRING_LENGTH = 300
        str_args = [
            (
                str(arg)
                if len(str(arg)) < MAX_STRING_LENGTH
                else str(arg)[:MAX_STRING_LENGTH] + "..."
            )
            for arg in args
        ]
        str_kwargs = {key: str(arg) for key, arg in kwargs.items()}

        # Now string them together, depending on whether we got args of each type.
        values = "- values: "
        if len(args) > 0:
            values = values + f"{json.dumps(str_args)}"
        if len(args) > 0 and len(kwargs) > 0:
            values = values + f"{', '}"
        if len(kwargs) > 0:
            values = values + f"{json.dumps(str_kwargs)}"

        return values

    # -------------------------------------------------------------------------
    # Model handling.
    # -------------------------------------------------------------------------

    def to_model(self) -> ValidatorModel:
        """
        Returns this validator as a model.

        :return: The serialized model object.
        """
        return ValidatorModel(
            bool_exp=(
                serializing.encode_callable(self.bool_exp)
                if self.bool_exp
                else None
            ),
            success=self.success,
            failure=self.failure,
            info=self.info,
            bool_exp_str=self.bool_exp_str,
            creator_class=(
                self.creator.function_class
                if self.creator is not None
                else None
            ),
            creator_function=(
                self.creator.function_name if self.creator is not None else None
            ),
            creator_args=(
                self.creator.arguments if self.creator is not None else []
            ),
        )

    @classmethod
    def from_model(cls, model: BaseModel) -> Validator:
        """
        Deserialize a Validator from a model.

        :param model: The model.

        :return: The deserialized Validator
        """
        model = typing.cast(ValidatorModel, model)
        validator: Validator = Validator(
            bool_exp=(
                typing.cast(
                    Callable[[Any], bool],
                    serializing.decode_callable(model.bool_exp),
                )
                if model.bool_exp
                else None
            ),
            success=model.success,
            failure=model.failure,
            info=model.info,
            creator=(
                FunctionInfo(
                    model.creator_function,
                    model.creator_args,
                    model.creator_class,
                )
                if model.creator_function is not None
                and model.creator_class is not None
                else None
            ),
        )
        return validator

    # -------------------------------------------------------------------------
    # Equality Testing
    # -------------------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        """Test instance for equality."""
        if not isinstance(other, Validator):
            return False
        return self._equal(other)
