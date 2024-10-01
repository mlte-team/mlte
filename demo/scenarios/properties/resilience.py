from mlte.property.base import Property


class Resilience(Property):
    """
    The Resilience property reflects ...
    """

    def __init__(self, rationale: str):
        """Initialize a Resilience instance."""
        super().__init__(
            instance=self,
            description="""
                The Resilience property assesses ...
                """,
            rationale=rationale,
        )
