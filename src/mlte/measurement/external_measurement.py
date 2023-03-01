"""
Base class for measurements calculated by external functions.
"""

from __future__ import annotations

from .result import Result
from .measurement import Measurement


class ExternalMeasurement(Measurement):
    def __init__(self, identifier: str, result_type: type):
        """
        Initialize a new ExternalMeasurement measurement.

        :param identifier: A unique identifier for the instance
        :type identifier: str
        :param result_type: The type of the Result this measurement will return.
        :type result_type: Type
        """
        super().__init__(self, identifier)
        if not issubclass(Result, result_type):
            raise Exception(
                f"Result type provided is not a subtype of Result: {self.result_type}"
            )
        self.result_type: type = result_type       

    def __call__(self, *args, **kwargs) -> Result:
        """Evaluate a measurement and return results without semantics."""
        result: Result = self.result_type(self.metadata, *args, **kwargs)
        return result
