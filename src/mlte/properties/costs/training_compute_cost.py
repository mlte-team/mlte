"""
TrainingComputeCost property definition.
"""

from ..property import Property
from ...internal.text import cleantext


class TrainingComputeCost(Property):
    """
    The TrainingComputeCost property reflects the costs
    of model training associated with compute resources.
    """

    def __init__(self):
        """
        Initialize a TrainingComputeCost instance.
        """
        super().__init__(
            "TrainingComputeCost",
            cleantext(
                """
                The TrainingComputeCost property assesses the
                computational requirements of model training.
                This might be measured in terms of CPU utilization
                for training processes that run locally, or the cost
                of compute resources required for training processes
                that run on on-demand cloud infrastructure.
                """
            ),
        )

    def __repr__(self) -> str:
        """Return the representation needed to reconstruct the object."""
        return f"{self.name}()"
