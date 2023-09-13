"""
Robustness property definition.
"""

from mlte._private.text import cleantext
from mlte.property import Property


class Robustness(Property):
    """
    The Robustness property focuses on checking that the model performance does not vary with respect to noise.
    """

    def __init__(self, rationale: str):
        """Initialize a Robustness instance."""
        super().__init__(
            self.__class__.__name__,
            cleantext(
                """
                The Robustness property  focuses on checking that the model performance does not vary with respect to noise
                (or small changes in the input data that do not change the data label). Robustness is evaluating model
                performance as something is happening during the collection of the data that will not affect a data attribute
                but will affect how the object may be perceived.
                """
            ),
            rationale,
        )
