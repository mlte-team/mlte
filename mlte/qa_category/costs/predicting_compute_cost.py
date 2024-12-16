"""
PredictingComputeCost QACategory definition.
"""

from mlte.qa_category.base import QACategory


class PredictingComputeCost(QACategory):
    """
    The PredictingComputeCost QACategory reflects the costs
    of model predicting associated with compute resources.
    """

    def __init__(self, rationale: str):
        """
        Initialize a PredictingComputeCost instance.
        """
        super().__init__(
            instance=self,
            description="""
                The PredictingComputeCost QACategory assesses the
                computational requirements of model predicting.
                This might be measured in terms of CPU utilization
                for QACategory processes that run locally,
                or the cost of compute resources required for QACategory
                processes that run on on-demand cloud
                infrastructure.
                """,
            rationale=rationale,
        )
