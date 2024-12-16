"""
test/spec/extended_qa_category.py

ExtendedQACategory definition, for testing purposes.
"""

from mlte.qa_category.base import QACategory


class ExtendedQACategory(QACategory):
    """
    The ExtendedQACategory QACategory is a
    QACategory not defined in the default QACategory package.
    """

    def __init__(self, rationale: str):
        """Initialize a ExtendedQACategory instance."""
        super().__init__(
            instance=self,
            description="""
                The ExtendedQACategory QACategory is just for testing purposes.
                """,
            rationale=rationale,
        )
