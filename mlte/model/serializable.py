"""
Serializable interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import mlte._private.meta as meta
from mlte.model.base_model import BaseModel


class Serializable(ABC):
    """
    Interface to define classes that can be converted into a Pydantic model.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return meta.has_callables(subclass, "to_model", "from_model")

    @abstractmethod
    def to_model(self) -> BaseModel:
        """Serialize an Serializable to its corresponding model."""
        raise NotImplementedError(
            "to_model() not implemented for abstract Serializable."
        )

    @classmethod
    @abstractmethod
    def from_model(cls, model: BaseModel) -> Any:
        """Deserialize an Serializable from its corresponding model."""
        raise NotImplementedError(
            "from_model() not implemented for abstract Serializable."
        )

    def __json__(self):
        """Hack method to make Serializable serializable to JSON if importing json-fix before json.dumps."""
        return self.to_model().to_json()

    def _equal(a: Serializable, b: Serializable) -> bool:
        """
        Compare Serializable instances for equality.

        :param a: Input instance
        :param b: Input instance
        :return: `True` if `a` and `b` are equal, `False` otherwise
        """
        return a.to_model() == b.to_model()

    def __eq__(self, other: object) -> bool:
        """Test instance for equality."""
        if not isinstance(other, Serializable):
            return False
        return self._equal(other)
