"""
mlte/qa_category/functionality/task_efficacy.py

TaskEfficacy QACategory definition.
"""

from mlte.qa_category.base import QACategory


class TaskEfficacy(QACategory):
    """
    The TaskEfficacy QACategory assesses the ability of
    a model to perform the task for which it is designed.
    """

    def __init__(self, rationale: str):
        """Initialize a TaskEfficacy instance."""
        super().__init__(
            instance=self,
            description="""
                The TaskEfficacy QACategory assesses a model's ability
                to correctly perform instances of its task. The means
                of measurement for this QACategory will vary by both
                domain and task. Examples include accuracy, error rate,
                and average precision, but many others are possible.
                """,
            rationale=rationale,
        )
