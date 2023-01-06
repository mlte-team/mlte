"""
Superclass for all measurements.
"""

from __future__ import annotations

import abc
import typing

from mlte.property import Property
from ._binding import Bound, Unbound
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

        self.binding = Unbound()
        """The measurement's binding."""

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
        # Evaluate the measurement, and propagate binding
        return self.__call__(*args, **kwargs)._with_binding(self.binding)

    def bind(self, property: Property):
        """
        Bind the Measurement instance to Property `property`.

        Binding a Measurement has a slightly different meaning from
        binding a Result. Precisely, binding a Measurement entails
        that the Result produced by the Measurement inherits the binding,
        meaning that the result need not be bound after it is produced.

        :param property: The property to which the measurement is bound
        :type property: Property
        """
        if self.binding.is_bound():
            raise RuntimeError("Attempt to bind a previously-bound entity.")
        self.binding = Bound(property.name)
