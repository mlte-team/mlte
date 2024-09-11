"""
mlte/measurement/external_measurement.py

Base class for measurements calculated by external functions.
"""

from __future__ import annotations

from typing import Any, Callable, Optional, Type

from mlte.measurement.measurement import Measurement
from mlte.value.artifact import Value


class ExternalMeasurement(Measurement):
    def __init__(
        self,
        identifier: str,
        value_type: type,
        function: Optional[Callable[..., Any]] = None,
    ):
        """
        Initialize a new ExternalMeasurement measurement.

        :param identifier: A unique identifier for the instance
        :param value_type: The type of the Value this measurement will return.
        :param function: The function to be used when evaluating.
        """
        super().__init__(self, identifier)

        if not issubclass(value_type, Value):
            raise Exception(
                f"Value type provided is not a subtype of Value: {value_type}"
            )
        self.value_type: type = value_type

        if function is not None:
            # Store the function module+name as additional metadata info, for better traceability.
            self.metadata.info = (
                f"function: {function.__module__}.{function.__name__}"
            )

        self.function: Optional[Callable[..., Any]] = function
        """Store the callable function itself."""

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
