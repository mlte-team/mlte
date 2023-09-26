"""
Fairness property definition.
"""

from mlte._private.text import cleantext
from mlte.property.property import Property


class Fairness(Property):
    """
    The Fairness property ensures similar model performance across specified subpopulations, groups, or data.
    """

    def __init__(self, rationale: str):
        """Initialize a Fairness instance."""
        super().__init__(
            self.__class__.__name__,
            cleantext(
                """
                The Fairness property ensures similar model performance across specified subpopulations, groups, or data.
                Fairness is measured by evaluating model performance on population data sub-divided by an attribute.
                """
            ),
            rationale,
            __name__
        )
