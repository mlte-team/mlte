"""
A more detailed collection of properties and their measurements, based on the basic Spec.
"""

from __future__ import annotations

from typing import Any

from mlte.measurement import Measurement
from mlte.property import Property
from mlte.spec import Spec

# -----------------------------------------------------------------------------
# DetailedSpec
# -----------------------------------------------------------------------------


class DetailedSpec(Spec):
    """
    The DetailedSpec class integrates properties, measurements,
    validation details, without the actual results for a specific instance.
    """

    def __init__(self, properties: dict[Property, list[Measurement]]):
        """
        Initialize a DetailedSpec instance.

        :param properties: The collection of properties that compose the spec
        :type properties: Property
        """
        super().__init__(*list(properties.keys()))

        # Stored the measurements indexed by property name.
        self.measurements: dict[str, list[Measurement]] = {
            property.name: [str(m) for m in measurements]
            for (property, measurements) in properties.items()
        }

        # TODO: How to indicate validations and thresholds? Separately?

        # TODO: Generate BoundSpec-similar document but for this DetailedSpec.

    def generate_document(self) -> dict[str, Any]:
        """Generates a document with the detailed spec."""
        property_docs = [
            self._property_document(property, self.measurements[property.name])
            for property in self.properties
        ]
        document = self._spec_document(property_docs)
        return document
