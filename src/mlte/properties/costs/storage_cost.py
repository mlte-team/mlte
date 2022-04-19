"""
StorageCost property definition.
"""

from ..property import Property


class StorageCost(Property):
    """
    The StorageCost property reflects the cost of model storage.
    """

    def __init__(self):
        """Initialize a StorageCost instance."""
        super().__init__("StorageCost")

    def __repr__(self) -> str:
        """Return the representation needed to reconstruct the object."""
        return f"{self.name}()"
