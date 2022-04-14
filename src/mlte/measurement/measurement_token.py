"""
A unique identifier for instances of the Measurement class.
"""

import uuid


class MeasurementToken:
    """
    A MeasurementToken is a unique identifier for a measurement instance.
    The MeasurementToken goes beyond identifying the name of the
    measurement, and actually identifies the particular instance to
    which it is attached. Two instances of the same measurement with
    identical attributes will have distinct MeasurementTokens.
    """

    def __init__(self, measurement_name: str):
        """
        Initialize a MeasurementToken instance.

        :param measurement_name: The name of the
        measurement to which this token is attached
        :type measurement_name: str
        """
        # The name of the owning measurement
        self.measurement_name = measurement_name
        # A random, unique identifier for the instance
        self.hash = uuid.uuid4().hex

    def __eq__(self, other: object) -> bool:
        """Determine if two MeasurementToken instances are equal."""
        if not isinstance(other, MeasurementToken):
            return False
        return (
            self.measurement_name == other.measurement_name
            and self.hash == other.hash
        )

    def __ne__(self, other: object) -> bool:
        """Determine if two MeasurementToken instances are not equal."""
        return not self.__eq__(other)

    def __str__(self) -> str:
        """Return a string representation of the MeasurementToken."""
        return f"{self.measurement_name}, {self.hash}"
