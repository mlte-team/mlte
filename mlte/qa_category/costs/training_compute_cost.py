"""
mlte/qa_category/costs/training_compute_cost.py

TrainingComputeCost qa category definition.
"""

from mlte.qa_category.base import QACategory


class TrainingComputeCost(QACategory):
    """
    The TrainingComputeCost qa category reflects the costs
    of model training associated with compute resources.
    """

    def __init__(self, rationale: str):
        """
        Initialize a TrainingComputeCost instance.
        """
        super().__init__(
            instance=self,
            description="""
                The TrainingComputeCost qa category assesses the
                computational requirements of model training.
                This might be measured in terms of CPU utilization
                for training processes that run locally, or the cost
                of compute resources required for training processes
                that run on on-demand cloud infrastructure.
                """,
            rationale=rationale,
        )
