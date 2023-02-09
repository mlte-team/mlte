"""
TaskEfficacy property definition.
"""

from ..property import Property
from ..._private.text import cleantext


class TaskEfficacy(Property):
    """
    The TaskEfficacy property assesses the ability of
    a model to perform the task for which it is designed.
    """

    def __init__(self):
        """Initialize a TaskEfficacy instance."""
        super().__init__(
            "TaskEfficacy",
            cleantext(
                """
                The TaskEfficacy property assesses a model's ability
                to correctly perform instances of its task. The means
                of measurement for this property will vary by both
                domain and task. Examples include accuracy, error rate,
                and average precision, but many others are possible.
                """
            ),
        )

    def __repr__(self) -> str:
        """Return the representation needed to reconstruct the object."""
        return f"{self.name}()"
