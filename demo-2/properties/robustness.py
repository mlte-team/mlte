"""
Robustness property definition.
"""

from mlte.property.base import Property


class Robustness(Property):
    """
    Definition of the Robustness property.
    """

    def __init__(self, rationale: str):
        """Initialize a Robustness instance."""
        super().__init__(
            instance=self,
            description="""
                Robustness in general is the degree to which a system continues to function in the presence of
                invalid inputs or stressful environmental conditions. For ML models, this means checking that
                model performance does not deteriorate significantly in the presence of noise.
                """,
            rationale=rationale,
        )
