"""
The superclass for all model properties.
"""

import abc
from typing import List

from ..measurement import Measurement


def _unique(collection: List[str]) -> bool:
    """
    Determine if all elements of a collection are unique.

    :param collection: The collection
    :type collection: Iterable

    :return: `True` if all elements are unique, `False` otherwise
    :rtype: bool
    """
    return len(set(collection)) == len(collection)


def _has_callable(type, name) -> bool:
    """Determine if `type` has a callable attribute with the given name."""
    return hasattr(type, name) and callable(getattr(type, name))


class Property(metaclass=abc.ABCMeta):
    """The Property type represents an abstract model property."""

    @classmethod
    def __subclasshook__(cls, subclass):
        """Define the interface for all concrete properties."""
        return all(_has_callable(subclass, method) for method in ["__init__"])

    def __init__(self, name: str, *measurements: Measurement):
        """
        Initialize a Property instance.

        :param name: The name of the property
        :type name: str
        :param measurements: The collection of measurements for the property
        :type measurements: Measurement
        """
        self.name: str = name
        """The name of the property."""
        self.measurements: List[Measurement] = [m for m in measurements]
        """The collection of measurements for the property."""

        if not _unique([m.name for m in measurements]):
            raise RuntimeError(
                "All measurements for a property must be unique."
            )

    def add_measurement(self, measurement: Measurement):
        """
        Add a measurement for the property instance.

        :param measurement: The measurement instance
        :type measurement: Measurement
        """
        self.measurements.append(measurement)
        if not _unique([m.name for m in self.measurements]):
            raise RuntimeError(
                "All measurements for a property must be unique."
            )
