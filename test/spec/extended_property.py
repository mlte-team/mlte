"""
test/spec/test_model.py

ExtendedProperty definition, for testing purposes.
"""

from mlte.property.property import Property


class ExtendedProperty(Property):
    """
    The ExtendedProperty property is a property not defined in the default property package.
    """

    def __init__(self, rationale: str):
        """Initialize a ExtendedProperty instance."""
        super().__init__(
            instance=self,
            description="""
                The ExtendedProperty property is just for testing purposes.
                """,
            rationale=rationale,
        )
