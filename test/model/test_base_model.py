"""
test/model/test_base_model.py

Unit tests for base model functionality.
"""

from __future__ import annotations

from typing import Any

import pytest

from mlte.model.base_model import BaseModel
from mlte.model.serialization_error import SerializationError


class ModelTest(BaseModel):
    int_num: int = 1
    float_num: float = 1.2
    str_obj: str = "test"
    bool_obj: bool = False
    obj: Any = ""


class NonSerializable:
    attr3: str = "test"
    attr1: dict[str, Any] = {"baz": ModelTest()}


def test_to_json():
    test_obj = ModelTest()
    json_obj = test_obj.to_json()
    reconstructed = ModelTest.from_json(json_obj)

    assert test_obj == reconstructed


def test_to_json_to_str_not_serializable():
    test_obj = ModelTest()
    test_obj.obj = NonSerializable()

    with pytest.raises(SerializationError):
        _ = test_obj.to_json()
