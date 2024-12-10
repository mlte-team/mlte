"""
PredictingComputeCost qa category definition.
"""

from mlte.qa_category.base import QACategory


class PredictingComputeCost(QACategory):
    """
    The PredictingComputeCost qa category reflects the costs
    of model predicting associated with compute resources.
    """

    def __init__(self, rationale: str):
        """
        Initialize a PredictingComputeCost instance.
        """
        super().__init__(
            instance=self,
            description="""
                The PredictingComputeCost qa category assesses the
                computational requirements of model predicting.
                This might be measured in terms of CPU utilization
                for qa category processes that run locally,
                or the cost of compute resources required for qa
                category processes that run on on-demand cloud
                infrastructure.
                """,
            rationale=rationale,
        )
