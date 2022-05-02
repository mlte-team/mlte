"""
TrainingMemoryCost property definition.
"""

from ..property import Property
from ..._private.text import cleantext


class TrainingMemoryCost(Property):
    """
    The TrainingMemoryCost property reflects the cost
    of model training associated with memory resources.
    """

    def __init__(self):
        """
        Initialize a TrainingMemoryCost instance.
        """
        super().__init__(
            "TrainingMemoryCost",
            cleantext(
                """
                The TrainingMemoryCost property assesses the
                memory requirements of model training. This might
                be measured by the memory requirements of training
                processes that run locally, or the cost of memory
                resources required for training processes that run
                on on-demand cloud infrastructure.
                """
            ),
        )

    def __repr__(self) -> str:
        """Return the representation needed to reconstruct the object."""
        return f"{self.name}()"
