"""
test/serde/test_json.py

Unit tests for JSON serialization / deserialization.
"""

from dataclasses import dataclass

from mlte.serde.json import JsonableDataclass, JsonableEnum


@dataclass
class Item(JsonableDataclass):
    """A dummy class for tests."""

    name: str
    """The name of the item."""

    count: int
    """The associated count."""


class Color(JsonableEnum):
    RED = "red"
    WHITE = "white"
    BLUE = "blue"


def test_jsonable_dataclass() -> None:
    item = Item(name="hello", count=1)
    json = item.to_json()

    assert "name" in json
    assert "count" in json

    assert json["name"] == "hello"
    assert json["count"] == 1


def test_jsonable_enum() -> None:
    for color in Color:
        s = color.to_json()
        d = Color.from_json(s)
        assert d == color
