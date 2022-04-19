"""
TrainingMemoryCost property definition.
"""

from ..property import Property


class TrainingMemoryCost(Property):
    """
    The TrainingMemoryCost property reflects the cost
    of model training associated with memory resources.
    """

    def __init__(self):
        """
        Initialize a TrainingMemoryCost instance.
        """
        super().__init__("TrainingMemoryCost")

    def __repr__(self) -> str:
        """Return the representation needed to reconstruct the object."""
        return f"{self.name}()"
