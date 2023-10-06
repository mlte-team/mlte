"""
mlte/property/functionality/task_efficacy.py

TaskEfficacy property definition.
"""

from mlte.property.base import Property


class TaskEfficacy(Property):
    """
    The TaskEfficacy property assesses the ability of
    a model to perform the task for which it is designed.
    """

    def __init__(self, rationale: str):
        """Initialize a TaskEfficacy instance."""
        super().__init__(
            instance=self,
            description="""
                The TaskEfficacy property assesses a model's ability
                to correctly perform instances of its task. The means
                of measurement for this property will vary by both
                domain and task. Examples include accuracy, error rate,
                and average precision, but many others are possible.
                """,
            rationale=rationale,
        )
