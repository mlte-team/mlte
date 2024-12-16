from mlte.qa_category.base import QACategory


class Accuracy(QACategory):
    """
    The Accuracy QA category reflects the overall functional accuracy of a model.
    """

    def __init__(self, rationale: str):
        """Initialize a Accuracy instance."""
        super().__init__(
            instance=self,
            description="""
                The Accuracy QA category assesses the total predictive performance requirements of a
                model and system. These requirements are typically given as a single real valued number. 
                """,
            rationale=rationale,
        )
