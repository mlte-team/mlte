
from mlte.property.base import Property


class Accuracy(Property):
    """
    The Accuracy property reflects the overall functional accuracy of a model.
    """

    def __init__(self, rationale: str):
        """Initialize a Accuracy instance."""
        super().__init__(
            instance=self,
            description="""
            The Accuracy property assesses the total predictive performance requirements of a
            model and system. These requirements are typically given as a single real valued number. 
            """,
            rationale=rationale,
        )