"""
mlte/property/costs/training_memory_cost.py

TrainingMemoryCost property definition.
"""

from mlte.property.base import Property


class TrainingMemoryCost(Property):
    """
    The TrainingMemoryCost property reflects the cost
    of model training associated with memory resources.
    """

    def __init__(self, rationale: str):
        """
        Initialize a TrainingMemoryCost instance.
        """
        super().__init__(
            instance=self,
            description="""
                The TrainingMemoryCost property assesses the
                memory requirements of model training. This might
                be measured by the memory requirements of training
                processes that run locally, or the cost of memory
                resources required for training processes that run
                on on-demand cloud infrastructure.
                """,
            rationale=rationale,
        )
