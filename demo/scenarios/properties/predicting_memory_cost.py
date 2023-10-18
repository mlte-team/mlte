"""
PredictingMemoryCost property definition.
"""

from mlte.property.base import Property


class PredictingMemoryCost(Property):
    """
    The PredictingMemoryCost property reflects the cost
    of model predicting associated with memory resources.
    """

    def __init__(self, rationale: str):
        """
        Initialize a PredictingMemoryCost instance.
        """
        super().__init__(
            instance=self,
            description="""
                The PredictingMemoryCost property assesses the
                memory requirements of model predicting. This might
                be measured by the memory requirements of property
                processes that run locally, or the cost of memory
                resources required for property processes that run
                on on-demand cloud infrastructure.
                """,
            rationale=rationale,
        )
