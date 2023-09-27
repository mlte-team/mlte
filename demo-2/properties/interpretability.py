"""
Interpretability property definition.
"""

from mlte._private.text import cleantext
from mlte.property.property import Property


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
                Interpretability is the degree to which a human can understand the cause of a decision. 
                For ML models, it is about providing information for a human user to interpret and understand 
                what data was influential in the ML model's result. A model developer should return interpretability 
                evidence along with the model inference result.
                """
            ),
            rationale,
            __name__
        )
