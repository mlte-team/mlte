"""
mlte/spec/validated_spec.py

ValidatedSpec class implementation.
"""

from __future__ import annotations

from typing import Dict, cast

from mlte.artifact.artifact import Artifact
from mlte.artifact.model import ArtifactModel
from mlte.spec.model import SpecModel
from mlte.spec.spec import Spec
from mlte.validation.result import Result

# -----------------------------------------------------------------------------
# ValidatedSpec
# -----------------------------------------------------------------------------


class ValidatedSpec(Artifact):
    """
    ValidatedSpec represents a spec with validated results.
    """

    def __init__(self, spec: Spec, results: Dict[str, Dict[str, Result]]):
        """
        Initialize a ValidatedSpec instance.

        :param spec: The Spec
        :param results: The validation Results for the Spec
        """

        self.spec = spec
        """The spec that we validated."""

        self.results = results
        """The validation results for the spec, by property."""

        # Check that all conditions have results.
        for property, conditions in self.spec.properties.items():
            for measurement_id in conditions.keys():
                if (
                    property.name not in self.results
                    or measurement_id not in self.results[property.name]
                ):
                    raise RuntimeError(
                        f"Id '{measurement_id}' does not have a result."
                    )

    def to_model(self) -> ArtifactModel:
        """
        Generates a model representation of the ValidatedSpec.

        :return: The serialized model
        """
        model = self.spec.to_model()
        model.header.identifier = f"{model.header.identifier}.validated"

        # Add results to main model.
        spec_model: SpecModel = cast(SpecModel, model.body)
        for property_model in spec_model.properties:
            for measurement_id in property_model.conditions.keys():
                result = self.results[property_model.name][measurement_id]
                property_model.results[measurement_id] = result.to_model()

        return model

    @classmethod
    def from_model(cls, model: ArtifactModel) -> ValidatedSpec:
        """
        Deserialize ValidatedSpec content from model.

        :param model: The model
        :return: The deserialized specification
        """
        spec = Spec.from_model(model)

        # Load results from full model.
        results: Dict[str, Dict[str, Result]] = {}
        spec_model: SpecModel = cast(SpecModel, model.body)
        for property_model in spec_model.properties:
            results[property_model.name] = {}
            for measurement_id in property_model.conditions.keys():
                results[property_model.name][
                    measurement_id
                ] = Result.from_model(property_model.results[measurement_id])

        return ValidatedSpec(spec, results)

    def __eq__(self, other: object) -> bool:
        """Test ValidatedSpec instance for equality."""
        if not isinstance(other, ValidatedSpec):
            return False
        return _equal(self, other)

    def __neq__(self, other: object) -> bool:
        """Test ValidatedSpec instance for inequality."""
        return not self.__eq__(other)


def _equal(a: ValidatedSpec, b: ValidatedSpec) -> bool:
    """
    Determine if two ValidatedSpec instances are equal.

    :param a: Input instance
    :param b: Input instance
    :return: `True` if instances are equal, `False` otherwise
    """
    return a.spec == b.spec and a.results == b.results
