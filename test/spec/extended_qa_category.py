"""
test/spec/extended_qa_category.py

ExtendedQACategory definition, for testing purposes.
"""

from mlte.qa_category.base import QACategory


class ExtendedQACategory(QACategory):
    """
    The ExtendedQACategory qa category is a
     qa category not defined in the default qa category package.
    """

    def __init__(self, rationale: str):
        """Initialize a ExtendedQACategory instance."""
        super().__init__(
            instance=self,
            description="""
                The ExtendedQACategory qa category is just for testing purposes.
                """,
            rationale=rationale,
        )
