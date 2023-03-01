from typing import Type

from .result import Result
from .measurement import Measurement


class ExternalMeasurement(Measurement):

    def __init__(self, identifier: str, result_type: Type):
        """
        Initialize a new ExternalMeasurement measurement.

        :param identifier: A unique identifier for the instance
        :type identifier: str
        :param result_type: The type of the Result this measurement will return.
        :type result_type: Type        
        """
        super().__init__(self, identifier)
        self.result_type: Type = result_type
    
    def __call__(self, *args, **kwargs) -> Result:
        """Evaluate a measurement and return results without semantics."""
        return self.result_type(self.metadata, *args, **kwargs)
