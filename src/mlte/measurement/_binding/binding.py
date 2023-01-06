"""
Type definitions for binding state.
"""

from __future__ import annotations

from enum import Enum
from typing import Dict, Any

from mlte.property import Property


class BindingType(Enum):
    """Possible binding states."""

    BOUND = 0
    UNBOUND = 1


class Binding:
    def __init__(self, type: BindingType):
        """Initialize a new Binding instance with type."""
        self.type = type

    def is_bound(self) -> bool:
        """Determine if the instance is bound."""
        return self.type == BindingType.BOUND

    @staticmethod
    def from_json(json: Dict[str, Any]) -> Binding:
        """Deserialize a Binding instance from JSON."""
        assert "state" in json, "Broken precondition."
        if json["state"] == "bound":
            return Bound(json["property_name"])
        elif json["state"] == "unbound":
            return Unbound()
        else:
            assert False, "Unreachable."


class Bound(Binding):
    """Represents a bound entity."""

    def __init__(self, property_name: Property):
        super().__init__(BindingType.BOUND)
        self.property_name = property_name

    def to_json(self) -> Dict[str, Any]:
        """Serialization."""
        return {"state": "bound", "property_name": self.property_name}

    def is_bound_to(self, property: Property) -> bool:
        return self.property_name == property.name

    def __str__(self) -> str:
        return f"Bound to {self.property_name}"


class Unbound(Binding):
    """Represents an unbound entity."""

    def __init__(self):
        super().__init__(BindingType.UNBOUND)

    def to_json(self) -> Dict[str, Any]:
        """Serialization."""
        return {"state": "unbound"}

    def __str__(self) -> str:
        return "Unbound"
