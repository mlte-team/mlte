"""
mlte/property/costs/predicting_memory_cost.py

PredictingMemoryCost property definition.
"""

from mlte._private.text import cleantext
from mlte.property.property import Property


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
            self.__class__.__name__,
            cleantext(
                """
                The PredictingMemoryCost property assesses the
                memory requirements of model predicting. This might
                be measured by the memory requirements of property
                processes that run locally, or the cost of memory
                resources required for property processes that run
                on on-demand cloud infrastructure.
                """
            ),
            rationale,
            __name__
        )
