"""
MeasurementMetadata class definition.
"""

from .identifier import Identifier


class MeasurementMetadata:
    """A simple wrapper for measurement metadata."""

    def __init__(self, typename: str, identifier: Identifier):
        self.typename = typename
        """The name of the measurement class type."""

        self.identifier = identifier
        """The identifier for the measurement."""
