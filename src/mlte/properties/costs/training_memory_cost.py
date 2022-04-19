"""
TrainingMemoryCost property definition.
"""

from ..property import Property
from ...measurement import Measurement


class TrainingMemoryCost(Property):
    """
    The TrainingMemoryCost property reflects the cost
    of model training associated with memory resources.
    """

    def __init__(self, *measurements: Measurement):
        """
        Initialize a TrainingMemoryCost instance.

        :param measurements: The measurements associated with the property
        :type measurements: Measurement
        """
        super().__init__("TrainingMemoryCost", *measurements)
