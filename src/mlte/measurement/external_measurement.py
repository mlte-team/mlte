"""
Base class for measurements calculated by external functions.
"""

from __future__ import annotations

from typing import Type, Callable, Optional
import typing

from mlte.value import Value
from .measurement import Measurement


class ExternalMeasurement(Measurement):
    @typing.no_type_check
    def __init__(
        self,
        identifier: str,
        value_type: type,
        function: Optional[Callable] = None,
    ):
        """
        Initialize a new ExternalMeasurement measurement.

        :param identifier: A unique identifier for the instance
        :type identifier: str
        :param value_type: The type of the Value this measurement will return.
        :type value_type: Type
        :param value_type: The function to be used when evaluating.
        :type value_type: Callable
        """
        super().__init__(self, identifier)

        if not issubclass(Value, value_type):
            raise Exception(
                f"Value type provided is not a subtype of Value: {value_type}"
            )
        self.value_type: type = value_type

        if function is not None:
            if not callable(function):
                raise Exception(
                    f"Function type provided is not a function: {function}"
                )
            else:
                self.metadata.additional_info = (
                    f"function: {function.__module__}.{function.__name__}"
                )

        self.function: Optional[Callable] = function  # type: ignore

    def __call__(self, *args, **kwargs) -> Value:
        """Evaluate a measurement and return values without semantics."""
        if self.function is None:
            raise Exception("Can't evaluate, no function was set.")

        value: Value = self.value_type(
            self.metadata, self.function(*args, **kwargs)
        )
        return value

    def ingest(self, *args, **kwargs) -> Value:
        """Ingest data without evaluating a function, to wrap it as the configured Value type. Currently works the same as evaluate()."""
        value: Value = self.value_type(self.metadata, *args, **kwargs)
        return value

    @classmethod
    def value(self) -> Type[Value]:
        """Returns the class type object for the Value produced by the Measurement."""
        return self.value_type
