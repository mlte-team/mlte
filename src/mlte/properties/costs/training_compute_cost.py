"""
TrainingComputeCost property definition.
"""

from ..property import Property
from ...measurement import Measurement


class TrainingComputeCost(Property):
    """
    The TrainingComputeCost property reflects the costs
    of model training associated with compute resources.
    """

    def __init__(self, *measurements: Measurement):
        """
        Initialize a TrainingComputeCost instance.

        :param measurements: The measurements associated with the property
        :type measurements: Measurement
        """
        super().__init__("TrainingComputeCost", *measurements)
