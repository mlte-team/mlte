"""
PredictingMemoryCost QACategory definition.
"""

from mlte.qa_category.base import QACategory


class PredictingMemoryCost(QACategory):
    """
    The PredictingMemoryCost QACategory reflects the cost
    of model predicting associated with memory resources.
    """

    def __init__(self, rationale: str):
        """
        Initialize a PredictingMemoryCost instance.
        """
        super().__init__(
            instance=self,
            description="""
                The PredictingMemoryCost QACategory assesses the
                memory requirements of model predicting. This might
                be measured by the memory requirements of QACategory
                processes that run locally, or the cost of memory
                resources required for QACategory processes that run
                on on-demand cloud infrastructure.
                """,
            rationale=rationale,
        )
