"""
mlte/evidence/identifier.py

Identifier class implementation.
"""

from __future__ import annotations

from mlte.model.base_model import BaseModel


class Identifier(BaseModel):
    """
    Identifier is a simple class that standardizes
    the manner in which Measurements, Values, and
    Results are uniquely identified throughout
    their lifetimes.
    """

    name: str
    """The name of the object."""

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
