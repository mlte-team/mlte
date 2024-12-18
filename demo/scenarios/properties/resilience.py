from mlte.qa_category.base import QACategory


class Resilience(QACategory):
    """
    The Resilience QA category reflects ...
    """

    def __init__(self, rationale: str):
        """Initialize a Resilience instance."""
        super().__init__(
            instance=self,
            description="""
                The Resilience QA category assesses if a component is able to continue
                to carry out its mission in the face of adversity (i.e., if it provides required
                capabilities despite excessive stresses that can cause disruptions).
                """,
            rationale=rationale,
        )
