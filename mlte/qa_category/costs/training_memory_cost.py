"""
mlte/qa_category/costs/training_memory_cost.py

TrainingMemoryCost qa category definition.
"""

from mlte.qa_category.base import QACategory


class TrainingMemoryCost(QACategory):
    """
    The TrainingMemoryCost qa category reflects the cost
    of model training associated with memory resources.
    """

    def __init__(self, rationale: str):
        """
        Initialize a TrainingMemoryCost instance.
        """
        super().__init__(
            instance=self,
            description="""
                The TrainingMemoryCost qa category assesses the
                memory requirements of model training. This might
                be measured by the memory requirements of training
                processes that run locally, or the cost of memory
                resources required for training processes that run
                on on-demand cloud infrastructure.
                """,
            rationale=rationale,
        )
