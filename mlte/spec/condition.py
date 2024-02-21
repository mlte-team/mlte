"""
mlte/validation/condition.py

The interface for measurement validation.
"""

from __future__ import annotations

import base64
import inspect
import typing
from typing import Any, Callable, List, Type

import dill

from mlte.spec.model import ConditionModel
from mlte.validation.result import Result
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
        callback: Callable[[Value], Result],
        value_class: str = "",
    ):
        """
        Initialize a Condition instance.

        :param name: The name of the name method, for documenting purposes.
        :param arguments: The list of arguments passed to the callable.
        :param callback: The callable that implements validation.
        :param value_class: The full module + class name of the Value that generated this condition.
        """

        self.name: str = name
        """The human-readable identifier for the name method."""

        self.arguments: List[Any] = arguments
        """The arguments used when validating the condition."""

        self.callback: Callable[[Value], Result] = callback
        """The callback that implements validation."""

        self.value_class: str = (
            value_class
            if value_class != ""
            else f"{Value.__module__}.{Value.__name__}"
        )
        """Value type class where this Condition came from."""

    def __call__(self, value: Value) -> Result:
        """
        Invoke the validation callback

        :param value: The value of measurement evaluation

        :return: The result of measurement validation
        """
        return self.callback(value)._with_evidence_metadata(value.metadata)

    @staticmethod
    def build_condition(test: Callable[[Value], Result]) -> Condition:
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

        # Validation args include all caller arguments except for the value class type.
        validation_args = []
        for arg_key, arg_value in arguments.items():
            if arg_key != "cls":
                validation_args.append(arg_value)

        condition: Condition = Condition(
            validation_name, validation_args, test, cls_str
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
            callback=Condition.encode_callback(self.callback),
            value_class=self.value_class,
        )

    @staticmethod
    def encode_callback(callback: Callable[[Value], Result]) -> str:
        """Encodes the callback as a base64 string."""
        return base64.b64encode(dill.dumps(callback)).decode("utf-8")

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
            dill.loads(base64.b64decode(str(model.callback).encode("utf-8"))),
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

    def __neq__(self, other: Condition) -> bool:
        """Compare Condition instances for inequality."""
        return not self.__eq__(other)
