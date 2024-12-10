"""
mlte/qa_category/costs/storage_cost.py

StorageCost qa category definition.
"""

from mlte.qa_category.base import QACategory


class StorageCost(QACategory):
    """
    The StorageCost qa category reflects the cost of model storage.
    """

    def __init__(self, rationale: str):
        """Initialize a StorageCost instance."""
        super().__init__(
            instance=self,
            description="""
                The StorageCost qa category assesses the storage requirements of a
                model. These requirements may be expressed in a variety of ways,
                including the physical size of the model when it is persisted
                to stable storage, or the number of parameters it contains.
                """,
            rationale=rationale,
        )
