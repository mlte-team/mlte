"""
PredictingMemoryCost qa category definition.
"""

from mlte.qa_category.base import QACategory


class PredictingMemoryCost(QACategory):
    """
    The PredictingMemoryCost qa category reflects the cost
    of model predicting associated with memory resources.
    """

    def __init__(self, rationale: str):
        """
        Initialize a PredictingMemoryCost instance.
        """
        super().__init__(
            instance=self,
            description="""
                The PredictingMemoryCost qa category assesses the
                memory requirements of model predicting. This might
                be measured by the memory requirements of qa category
                processes that run locally, or the cost of memory
                resources required for qa category processes that run
                on on-demand cloud infrastructure.
                """,
            rationale=rationale,
        )
