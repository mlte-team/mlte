"""
mlte/validation/condition.py

The interface for measurement validation.
"""

from __future__ import annotations

import inspect
import typing
from typing import Any, Callable, List, Optional

from mlte._private.method_info import ClassMethodInfo
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
        :param arguments: The list of arguments/thresholds passed to the callable.
        :param validator: The Validator that implements validation.
        :param value_class: The full module + class name of the Value that generated this condition, if any.
        """

        self.name: str = name
        """The human-readable identifier for the name method."""

        self.arguments: List[Any] = arguments
        """The threshold arguments used when creating the condition."""

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
        bool_exp: Optional[Callable[[Any], bool]] = None,
        success: Optional[str] = None,
        failure: Optional[str] = None,
        info: Optional[str] = None,
    ) -> Condition:
        """Creates a Condition using the provided test, extracting context info from the method that called us."""
        # Get method info, passing our caller as argument.
        curr_frame = inspect.currentframe()
        caller_function = curr_frame.f_back if curr_frame is not None else None
        method_info = ClassMethodInfo.get_class_method_data(caller_function)

        # Build the validator. We can't really check at this point if the bool_exp actually returns a bool.
        validator = Validator.build_validator(
            bool_exp=bool_exp,
            success=success,
            failure=failure,
            info=info,
            caller_function=caller_function,
        )

        condition: Condition = Condition(
            method_info.method_name,
            method_info.arguments,
            validator,
            method_info.method_class,
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
