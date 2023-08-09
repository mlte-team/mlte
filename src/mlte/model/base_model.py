"""
mlte/model/base_model.py

Base model implementation for all MLTE models.
"""

from __future__ import annotations

from typing import Any

import pydantic


class BaseModel(pydantic.BaseModel):
    """The base model for all MLTE models."""

    def to_json(self) -> dict[str, Any]:
        """
        Serialize the model.
        :return: The JSON representation of the model
        """
        return self.dict()

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> BaseModel:
        """
        Deserialize a model from data.
        :param data: The raw input data
        :return: A deserialized model instance
        """
        return cls(**data)
