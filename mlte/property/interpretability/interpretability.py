"""
Interpretability property definition.
"""

from mlte.property.base import Property


class Interpretability(Property):
    """
    The Interpretability property
    """

    def __init__(self, rationale: str):
        """Initialize a Interpretability instance."""
        super().__init__(
            instance=self,
            description="""
                Interpretability is the degree to which a human can understand the cause of a decision.
                For ML models, it is about providing information for a human user to interpret and understand
                what data was influential in the ML model's result. A model developer should return interpretability
                evidence along with the model inference result.
                """,
            rationale=rationale,
        )
