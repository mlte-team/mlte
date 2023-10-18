"""
PredictingComputeCost property definition.
"""

from mlte.property.base import Property


class PredictingComputeCost(Property):
    """
    The PredictingComputeCost property reflects the costs
    of model predicting associated with compute resources.
    """

    def __init__(self, rationale: str):
        """
        Initialize a PredictingComputeCost instance.
        """
        super().__init__(
            instance=self,
            description="""
                The PredictingComputeCost property assesses the
                computational requirements of model predicting.
                This might be measured in terms of CPU utilization
                for property processes that run locally, or the cost
                of compute resources required for property processes
                that run on on-demand cloud infrastructure.
                """,
            rationale=rationale,
        )
