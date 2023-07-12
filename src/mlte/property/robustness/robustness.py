"""
Robustness property definition.
"""

from mlte.property import Property
from mlte._private.text import cleantext


class Robustness(Property):
    """
    The Robustness property reflects the cost of model storage.
    """

    def __init__(self, rationale: str):
        """Initialize a Robustness instance."""
        super().__init__(
            self.__class__.__name__,
            cleantext(
                """
                TODO
                """
            ),
            rationale,
        )
