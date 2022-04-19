"""
StorageCost property definition.
"""

from ..property import Property
from ...measurement import Measurement


class StorageCost(Property):
    """
    The StorageCost property reflects the cost of model storage.
    """

    def __init__(self, *measurements: Measurement):
        """
        Initialize a StorageCost instance.

        :param measurements: The measurements associated with the property
        :type measurements: Measurement
        """
        super().__init__("StorageCost", *measurements)
