"""
mlte/model/base_model.py

Base model implementation for all MLTE models.
"""

from __future__ import annotations

from typing import Any, Dict

import pydantic


class BaseModel(pydantic.BaseModel):
    """The base model for all MLTE models."""

    def to_json(self) -> Dict[str, Any]:
        """
        Serialize the model.
        :return: The JSON representation of the model
        """
        return self.model_dump()

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> BaseModel:
        """
        Deserialize a model from data.
        :param data: The raw input data
        :return: A deserialized model instance
        """
        return cls(**data)

    def _equal(a: BaseModel, b: BaseModel) -> bool:
        """
        Compare model instances for equality.

        :param a: Input instance
        :param b: Input instance
        :return: `True` if `a` and `b` are equal, `False` otherwise
        """
        return a.to_json() == b.to_json()

    def __eq__(self, other: object) -> bool:
        """Test instance for equality."""
        if not isinstance(other, BaseModel):
            return False
        return self._equal(other)

    def __neq__(self, other: object) -> bool:
        """Test instance for inequality."""
        return not self.__eq__(other)
