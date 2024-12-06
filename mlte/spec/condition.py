"""
mlte/validation/condition.py

The interface for measurement validation.
"""

from __future__ import annotations

import inspect
import typing
from typing import Any, Callable, List, Optional, Type

from mlte.validation.model_condition import ConditionModel
from mlte.validation.result import Result
from mlte.validation.validator import Validator
from mlte.value.artifact import Value


class Condition:
    """
    The Condition class defines the interface for measurement validators.
    """

    @typing.no_type_check
    def __init__(
        self,
        name: str,
        arguments: List[Any],
        validator: Validator,
        value_class: Optional[str] = None,
    ):
        """
        Initialize a Condition instance.

        :param name: The name of the name method, for documenting purposes.
        :param arguments: The list of arguments passed to the callable.
        :param validator: The Validator that implements validation.
        :param value_class: The full module + class name of the Value that generated this condition, if any.
        """

        self.name: str = name
        """The human-readable identifier for the name method."""

        self.arguments: List[Any] = arguments
        """The arguments used when validating the condition."""

        self.validator: Validator = validator
        """The validator that implements validation."""

        self.value_class: Optional[str] = value_class
        """Value type class where this Condition came from, if any."""

    def __call__(self, value: Value) -> Result:
        """
        Invoke the validation

        :param value: The value of measurement evaluation

        :return: The result of measurement validation
        """
        return self.validator.validate(value)._with_evidence_metadata(
            value.metadata
        )

    @staticmethod
    def build_condition(
        bool_exp: Optional[Callable[[Any], bool]],
        success: str = "Success message not set",
        failure: str = "Failure message not set",
        ignore: str = "Default message not set",
    ) -> Condition:
        """Creates a Condition using the provided test, extracting context info from the method that called us."""
        # Get info about the caller from inspection.
        curr_frame = inspect.currentframe()
        if curr_frame is None:
            raise Exception("Unexpected error reading validation method data.")
        caller_function = curr_frame.f_back
        if caller_function is None:
            raise Exception("Unexpected error reading validation method data.")

        # Get function name and arguments of callers.
        validation_name = caller_function.f_code.co_name
        arguments = caller_function.f_locals

        # Build the class info as a string.
        if "cls" not in arguments:
            raise Exception(
                "'cls' argument is needed in validation method arguments."
            )
        cls: Type[Value] = arguments["cls"]
        cls_str = f"{cls.__module__}.{cls.__name__}"

        # Build the validator. We can't really check at this point if the bool_exp actually returns a bool.
        validator = Validator(
            bool_exp=bool_exp, success=success, failure=failure, ignore=ignore
        )

        # Validation args include all caller arguments except for the value class type.
        validation_args = []
        for arg_key, arg_value in arguments.items():
            if arg_key != "cls":
                validation_args.append(arg_value)

        condition: Condition = Condition(
            validation_name, validation_args, validator, cls_str
        )
        return condition

    def to_model(self) -> ConditionModel:
        """
        Returns this condition as a model.

        :return: The serialized model object.
        """
        return ConditionModel(
            name=self.name,
            arguments=self.arguments,
            validator=self.validator.to_model(),
            value_class=self.value_class,
        )

    @classmethod
    def from_model(cls, model: ConditionModel) -> Condition:
        """
        Deserialize a Condition from a model.

        :param model: The model.

        :return: The deserialized Condition
        """
        condition: Condition = Condition(
            model.name,
            model.arguments,
            Validator.from_model(model.validator),
            model.value_class,
        )
        return condition

    def __str__(self) -> str:
        """Return a string representation of Condition."""
        return f"{self.name} ({self.arguments}) from {self.value_class}"

    # -------------------------------------------------------------------------
    # Equality Testing
    # -------------------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        """Compare Condition instances for equality."""
        if not isinstance(other, Condition):
            return False
        reference: Condition = other
        return self.to_model() == reference.to_model()
