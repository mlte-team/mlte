"""
mlte/measurement/external_measurement.py

Base class for measurements calculated by external functions.
"""

from __future__ import annotations

from typing import Type

from mlte.value import Value
from .measurement import Measurement


class ExternalMeasurement(Measurement):
    def __init__(self, identifier: str, value_type: type):
        """
        Initialize a new ExternalMeasurement measurement.

        :param identifier: A unique identifier for the instance
        :type identifier: str
        :param value_type: The type of the Value this measurement will return.
        :type value_type: Type
        """
        super().__init__(self, identifier)
        if not issubclass(Value, value_type):
            raise Exception(
                f"Value type provided is not a subtype of Value: {self.value_type}"
            )
        self.value_type: type = value_type

    def __call__(self, *args, **kwargs) -> Value:
        """Evaluate a measurement and return values without semantics."""
        value: Value = self.value_type(self.metadata, *args, **kwargs)
        return value

    def ingest(self, *args, **kwargs) -> Value:
        """Ingest data without evaluating a function, to wrap it as the configured Value type. Currently works the same as evaluate()."""
        value: Value = self.value_type(self.metadata, *args, **kwargs)
        return value

    @classmethod
    def value(self) -> Type[Value]:
        """Returns the class type object for the Value produced by the Measurement."""
        return self.value_type
