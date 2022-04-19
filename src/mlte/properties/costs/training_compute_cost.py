"""
TrainingComputeCost property definition.
"""

from ..property import Property


class TrainingComputeCost(Property):
    """
    The TrainingComputeCost property reflects the costs
    of model training associated with compute resources.
    """

    def __init__(self):
        """
        Initialize a TrainingComputeCost instance.
        """
        super().__init__("TrainingComputeCost")

    def __repr__(self) -> str:
        """Return the representation needed to reconstruct the object."""
        return f"{self.name}()"
