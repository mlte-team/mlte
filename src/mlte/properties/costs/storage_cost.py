"""
StorageCost property definition.
"""

from ..property import Property
from ...internal.text import cleantext


class StorageCost(Property):
    """
    The StorageCost property reflects the cost of model storage.
    """

    def __init__(self):
        """Initialize a StorageCost instance."""
        super().__init__(
            "StorageCost",
            cleantext(
                """
                The StorageCost property assesses the storage requirements of a
                model. These requirements may be expressed in a variety of ways,
                including the physical size of the model when it is persisted
                to stable storage, or the number of parameters it contains.
                """
            ),
        )

    def __repr__(self) -> str:
        """Return the representation needed to reconstruct the object."""
        return f"{self.name}()"
