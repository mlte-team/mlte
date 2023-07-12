"""
mlte/serde/json.py

Common serialization / deserialization functionality for JSON documents.
"""

import dataclasses
from typing import Any


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
            dict_factory=lambda properties: {k: v for k, v in properties if v},
        )
        return document
