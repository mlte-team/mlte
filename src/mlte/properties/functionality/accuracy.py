"""
Accuracy property definition.
"""

from ..property import Property
from ...internal.text import cleantext


class Accuracy(Property):
    """
    The Accuracy property reflects the accuracy of the model.
    """

    def __init__(self):
        """Initialize a Accuracy instance."""
        super().__init__(
            "Accuracy",
            cleantext(
                """
                The Accuracy property assesses a model's ability
                to correctly perform instances of its task.
                Measurements for accuracy will vary by domain.
                """
            ),
        )

    def __repr__(self) -> str:
        """Return the representation needed to reconstruct the object."""
        return f"{self.name}()"
