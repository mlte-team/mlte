"""
mlte/spec/validated_spec.py

ValidatedSpec class implementation.
"""

from __future__ import annotations

import typing
from typing import Dict

from mlte.artifact.artifact import Artifact
from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.property.property import Property
from mlte.spec.condition import Condition
from mlte.spec.model import SpecModel
from mlte.spec.spec import Spec
from mlte.validation.model import (
    PropertyAndResultsModel,
    ResultModel,
    ValidatedSpecModel,
)
from mlte.validation.result import Result

DEFAULT_VALIDATED_SPEC_ID = "default.validated_spec"

# -----------------------------------------------------------------------------
# ValidatedSpec
# -----------------------------------------------------------------------------


class ValidatedSpec(Artifact):
    """
    ValidatedSpec represents a spec with validated results.
    """

    def __init__(
        self,
        identifier: str = DEFAULT_VALIDATED_SPEC_ID,
        spec: Spec = Spec(),
        results: Dict[str, Dict[str, Result]] = {},
    ):
        """
        Initialize a ValidatedSpec instance.

        :param spec: The Spec
        :param results: The validation Results for the Spec
        """
        super().__init__(identifier, ArtifactType.VALIDATED_SPEC)

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
        spec_model: SpecModel = typing.cast(SpecModel, model.body)

        # Convert results to model.
        res_model: Dict[str, Dict[str, ResultModel]] = {}
        for property_model in spec_model.properties:
            res_model[property_model.name] = {}
            for measure_id in property_model.conditions.keys():
                result = self.results[property_model.name][measure_id]
                res_model[property_model.name][measure_id] = result.to_model()

        return ArtifactModel(
            header=self.build_artifact_header(),
            body=ValidatedSpecModel(
                artifact_type=ArtifactType.VALIDATED_SPEC,
                properties=[
                    PropertyAndResultsModel(
                        name=property_model.name,
                        description=property_model.description,
                        rationale=property_model.rationale,
                        conditions=property_model.conditions,
                        results=res_model[property_model.name],
                    )
                    for property_model in spec_model.properties
                ],
            ),
        )

    @classmethod
    def from_model(cls, model: ArtifactModel) -> ValidatedSpec:
        """
        Deserialize ValidatedSpec content from model.

        :param model: The model
        :return: The deserialized specification
        """
        assert (
            model.header.type == ArtifactType.VALIDATED_SPEC
        ), "Broken precondition."
        body = typing.cast(ValidatedSpecModel, model.body)

        # Load properties and results from model into internal representations.
        spec_properties: Dict[Property, Dict[str, Condition]] = {}
        results: Dict[str, Dict[str, Result]] = {}
        for prop_model in body.properties:
            curr_prop = Property.from_model(prop_model)
            spec_properties[curr_prop] = {}
            results[prop_model.name] = {}
            for measure_id, condition in prop_model.conditions.items():
                spec_properties[curr_prop][measure_id] = Condition.from_model(
                    condition
                )
                results[prop_model.name][measure_id] = Result.from_model(
                    prop_model.results[measure_id]
                )

        # Build the spec and ValidatedSpec
        spec = Spec(identifier=body.spec_identifier, properties=spec_properties)
        return ValidatedSpec(
            identifier=model.header.identifier, spec=spec, results=results
        )

    @classmethod
    def get_default_id(cls) -> str:
        """Overriden"""
        return DEFAULT_VALIDATED_SPEC_ID

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
