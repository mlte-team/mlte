"""
Identifier class implementation.
"""

from __future__ import annotations


class Identifier:
    """
    Identifier is a simple class that standardizes
    the manner in which Measurements, Values, and
    Results are uniquely identified throughout
    their lifetimes.
    """

    def __init__(self, name: str):
        """
        Initialize a new Identifier instance.

        :param name: A unique name
        :type name: str
        """
        self.name = name

    def to_json(self) -> str:
        """Serialize to JSON document."""
        return self.name

    @staticmethod
    def from_json(json: str) -> Identifier:
        """Deserialize from JSON document."""
        return Identifier(name=json)

    def __eq__(self, other: object) -> bool:
        """Compare two Identifier instances for equality."""
        if not isinstance(other, Identifier):
            return False
        return self.name == other.name

    def __neq__(self, other: object) -> bool:
        """Compare two Identifier instances for inequality."""
        return not self.__eq__(other)

    def __str__(self) -> str:
        """Return a string representation of Identifier."""
        return f"{self.name}"
