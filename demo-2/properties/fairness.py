"""
Fairness property definition.
"""

from mlte.property.base import Property


class Fairness(Property):
    """
    Defintion of the Fairness property.
    """

    def __init__(self, rationale: str):
        """Initialize a Fairness instance."""
        super().__init__(
            instance=self,
            description="""
                Fairness refers to the absence of biases in data and model inaccuracies that lead to models that treat individuals
                or groups unfavorably on the basis of inherent or acquired characteristics (such as race, gender, disabilities,
                or others). For ML models, this means ensuring similar model performance across specified subpopulations, groups,
                or data.
                """,
            rationale=rationale,
        )
