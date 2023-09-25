"""
test/spec/test_model.py

ExtendedProperty definition, for testing purposes.
"""

from mlte._private.text import cleantext
from mlte.property.property import Property


class ExtendedProperty(Property):
    """
    The ExtendedProperty property is a property not defined in the default property package.
    """

    def __init__(self, rationale: str):
        """Initialize a ExtendedProperty instance."""
        super().__init__(
            self.__class__.__name__,
            cleantext(
                """
                The ExtendedProperty property is just for testing purposes.
                """
            ),
            rationale,
            __name__,
        )
