"""
mlte/property/costs/training_compute_cost.py

TrainingComputeCost property definition.
"""

from mlte.property.base import Property


class TrainingComputeCost(Property):
    """
    The TrainingComputeCost property reflects the costs
    of model training associated with compute resources.
    """

    def __init__(self, rationale: str):
        """
        Initialize a TrainingComputeCost instance.
        """
        super().__init__(
            instance=self,
            description="""
                The TrainingComputeCost property assesses the
                computational requirements of model training.
                This might be measured in terms of CPU utilization
                for training processes that run locally, or the cost
                of compute resources required for training processes
                that run on on-demand cloud infrastructure.
                """,
            rationale=rationale,
        )
