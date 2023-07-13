"""
mlte/serde/json.py

Common serialization / deserialization functionality for JSON documents.
"""

from __future__ import annotations

import dataclasses
from enum import Enum
from typing import Any

from mlte.serde.error import DeserializationError


def _serialize_value(v: Any) -> Any:
    """
    Serialize a value. Use a custom serializer, to_json(), if
    present; otherwise, rely on default serailization ability.
    :param value: The input value
    :return: The serialized value
    """
    return v.to_json() if hasattr(v, "to_json") else v


def _dict_factory(properties: list[tuple[str, Any]]) -> dict[str, Any]:
    """
    The factory function to convert class properties to document.
    :param properties: A list of (property_name, property_value)
    :return: The corresponding document representation
    """
    return {k: _serialize_value(v) for k, v in properties if v}


@dataclasses.dataclass
class JsonableDataclass:
    """A simple base class for dataclasses that can be converted to JSON."""

    def to_json(self) -> dict[str, Any]:
        """
        Convert a JsonableDataclass instance to a JSON document.
        :return: The converted document
        :rtype: Dict[str, Any]
        """
        document: dict[str, Any] = dataclasses.asdict(
            self,
            dict_factory=_dict_factory,
        )
        return document


class JsonableEnum(Enum):
    """A simple serialization scheme for enumerations that can be converted to JSON."""

    def to_json(self) -> dict[str, Any]:
        """
        Convert the enumeration to a JSON document.
        :return: The JSON document
        """
        return {"value": self.value}

    @classmethod
    def from_json(cls, document: dict[str, Any]) -> JsonableEnum:
        """
        Parse enumeration from JSON document.
        :param document: The JSON document
        :raises DeserializationError: If the document is malformed
        :raises RuntimeError: If the enumeration cannot be identified
        :return: The enumeration instance
        """
        if "value" not in document:
            raise DeserializationError("value")

        value = document["value"]
        for _, enum in cls._member_map_.items():
            if value == enum.value:
                return enum

        raise RuntimeError(
            f"Unrecognized enumeration value: '{document['value']}'."
        )
