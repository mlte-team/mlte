"""
mlte/property/costs/storage_cost.py

StorageCost property definition.
"""

from mlte.property.base import Property


class StorageCost(Property):
    """
    The StorageCost property reflects the cost of model storage.
    """

    def __init__(self, rationale: str):
        """Initialize a StorageCost instance."""
        super().__init__(
            instance=self,
            description="""
                The StorageCost property assesses the storage requirements of a
                model. These requirements may be expressed in a variety of ways,
                including the physical size of the model when it is persisted
                to stable storage, or the number of parameters it contains.
                """,
            rationale=rationale,
        )
