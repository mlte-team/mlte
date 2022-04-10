"""
Superclass for all model properties.
"""

import abc
import typing
from typing import Dict, Any

# The callable property instance methods
PROPERTY_METHODS = ["evaluate", "__call__", "_evaluate"]

# The callable property class methods
PROPERTY_CLASS_METHODS = ["_semantics"]


def _has_callable(type, name) -> bool:
    """Determine if `type` has a callable attribute with the given name."""
    return hasattr(type, name) and callable(getattr(type, name))


class Property(metaclass=abc.ABCMeta):
    """
    The superclass for all model properties.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        """Define the interface for all concrete properties."""
        return all(
            _has_callable(subclass, method) for method in PROPERTY_METHODS
        ) and all(
            _has_callable(subclass, method) for method in PROPERTY_CLASS_METHODS
        )

    def __init__(self, name: str):
        """
        Initialize a new Property instance.
        :param name The name of the property
        """
        self.name = name

    @abc.abstractmethod
    @typing.no_type_check
    def evaluate(self, *args, **kwargs) -> Any:
        """Evaluate a property and return results with semantics."""
        raise NotImplementedError("Cannot evaluate abstract property.")

    def __call__(self, *args, **kwargs) -> Any:
        """Evaluate a property and return results with semantics."""
        return self.evaluate(*args, **kwargs)

    @abc.abstractmethod
    @typing.no_type_check
    def _evaluate(self, *args, **kwargs) -> Dict[str, Any]:
        """Evaluate a property and return results without semantics."""
        raise NotImplementedError("Cannot evaluate abstract property.")

    @abc.abstractstaticmethod
    def _semantics(self, output: Dict[str, Any]) -> Any:
        """
        Dervice semantics from raw property output.
        :param output: The raw output of the property
        """
