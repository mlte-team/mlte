"""
mlte/model/base_model.py

Base model implementation for all MLTE models.
"""

from __future__ import annotations

from typing import Any, Optional

import pydantic

from mlte._private.fixed_json import json
from mlte.model.serialization_error import SerializationError


class BaseModel(pydantic.BaseModel):
    """The base model for all MLTE models."""

    def to_json(self) -> dict[str, Any]:
        """
        Serialize the model. Also check if the result is serializable.
        :return: The JSON representation of the model
        """
        json_object = self.model_dump()

        # Check if object can't be serialized.
        try:
            _ = json.dumps(json_object)
        except TypeError as e:
            raise SerializationError(e, str(type(self)))

        return json_object

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> BaseModel:
        """
        Deserialize a model from data.
        :param data: The raw input data
        :return: A deserialized model instance
        """
        return cls(**data)

    def to_json_string(self) -> str:
        """Serialize to a json string."""
        return json.dumps(self.to_json())

    @classmethod
    def from_json_string(cls, json_str: str) -> Any:
        """Deserialize from a json string."""
        return cls.from_json(json.loads(json_str))

    def post_validation_hook(self, data: Optional[Any] = None) -> Any:
        """Called after validation, lets submodels do any needed post-processing."""
        pass

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
