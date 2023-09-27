"""
Robustness property definition.
"""

from mlte._private.text import cleantext
from mlte.property.property import Property


class Robustness(Property):
    """
    Definition of the Robustness property.
    """

    def __init__(self, rationale: str):
        """Initialize a Robustness instance."""
        super().__init__(
            self.__class__.__name__,
            cleantext(
                """
                Robustness in general is the degree to which a system continues to function in the presence of 
                invalid inputs or stressful environmental conditions. For ML models, this means checking that 
                model performance does not deteriorate significantly in the presence of noise.
                """
            ),
            rationale,
            __name__
        )
