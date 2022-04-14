"""
Superclass for all model properties.
"""

import abc
import typing
from typing import Any

from .property_token import PropertyToken
from .result import EvaluationResult, Opaque


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
        return all(_has_callable(subclass, method) for method in ["__call__"])

    def __init__(self, name: str):
        """
        Initialize a new Property instance.
        :param name The name of the property
        """
        # The name of the property (human-readable identifier)
        self.name = name
        # The property token
        self.token = PropertyToken(self.name)

    @abc.abstractmethod
    @typing.no_type_check
    def __call__(self, *args, **kwargs) -> Any:
        """Evaluate a property and return results without semantics."""
        raise NotImplementedError("Cannot evaluate abstract property.")

    @typing.no_type_check
    def evaluate(self, *args, **kwargs) -> EvaluationResult:
        """Evaluate a property and return results with semantics."""
        data = self(*args, **kwargs)
        return (
            self.semantics(data)
            if hasattr(self, "semantics")
            else Opaque(self, data)
        )
