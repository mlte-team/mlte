"""
A unique identifier for instances of the Property class.
"""

import uuid


class PropertyToken:
    """
    A PropertyToken is a unique identifier for a Property instance.
    The PropertyToken goes beyond identifying the name of the
    property, and actually identifies the particular instance to
    which it is attached. Two instances of the same property with
    identical attributes will have distinct PropertyTokens.
    """

    def __init__(self, property_name: str):
        """
        Initialize a PropertyToken instance.

        :param property_name: The name of the property
        to which this token is attached
        :type property_name: str
        """
        # The name of the owning property
        self.property_name = property_name
        # A random, unique identifier for the instance
        self.hash = uuid.uuid4().hex

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PropertyToken):
            return False
        return (
            self.property_name == other.property_name
            and self.hash == other.hash
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        """Return a string representation of the PropertyToken."""
        return f"{self.property_name}, {self.hash}"
