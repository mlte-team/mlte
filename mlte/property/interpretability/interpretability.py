"""
Interpretability property definition.
"""

from mlte._private.text import cleantext
from mlte.property import Property


class Interpretability(Property):
    """
    The Interpretability property 
    """

    def __init__(self, rationale: str):
        """Initialize a Interpretability instance."""
        super().__init__(
            self.__class__.__name__,
            cleantext(
                """
                The Interpretability property 
                """
            ),
            rationale,
        )
