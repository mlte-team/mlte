"""
mlte/property/costs/predicting_compute_cost.py

PredictingComputeCost property definition.
"""

from mlte._private.text import cleantext
from mlte.property.property import Property


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
            self.__class__.__name__,
            cleantext(
                """
                The PredictingComputeCost property assesses the
                computational requirements of model predicting.
                This might be measured in terms of CPU utilization
                for property processes that run locally, or the cost
                of compute resources required for property processes
                that run on on-demand cloud infrastructure.
                """
            ),
            rationale,
            __name__
        )
