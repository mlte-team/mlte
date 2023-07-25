"""
TrainingComputeCost property definition.
"""

from ..property import Property
from ..._private.text import cleantext


class TrainingComputeCost(Property):
    """
    The TrainingComputeCost property reflects the costs
    of model training associated with compute resources.
    """

    def __init__(self, rationale: str):
        """
        Initialize a TrainingComputeCost instance.
        """
        super().__init__(
            self.__class__.__name__,
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
            rationale,
        )
