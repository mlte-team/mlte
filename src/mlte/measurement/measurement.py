"""
Superclass for all measurements.
"""

from __future__ import annotations

import abc
import typing

from .result import Result
from .measurement_metadata import MeasurementMetadata


def _has_callable(type, name) -> bool:
    """Determine if `type` has a callable attribute with the given name."""
    return hasattr(type, name) and callable(getattr(type, name))


class Measurement(metaclass=abc.ABCMeta):
    """
    The superclass for all model measurements.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        """Define the interface for all concrete measurements."""
        return all(_has_callable(subclass, method) for method in ["__call__"])

    def __init__(self, instance: Measurement, identifier: str):
        """
        Initialize a new Measurement instance.

        :param instance: The invoking instance (Measurement subclass)
        :type instance: Measurement
        :param identifier: A human-readable, unique identifier for the instance
        :type identifier: str
        """
        self.metadata = MeasurementMetadata(type(instance).__name__, identifier)
        """The metadata for the measurement instance."""

    @abc.abstractmethod
    @typing.no_type_check
    def __call__(self, *args, **kwargs) -> Result:
        """Evaluate a measurement and return results without semantics."""
        raise NotImplementedError("Cannot evaluate abstract measurement.")

    @typing.no_type_check
    def evaluate(self, *args, **kwargs) -> Result:
        """
        Evaluate a measurement and return results with semantics.

        :return: The result of measurement execution, with semantics
        :rtype: Result
        """
        # Evaluate the measurement
        return self.__call__(*args, **kwargs)
