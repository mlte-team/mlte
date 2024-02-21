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
from mlte.spec.model import SpecModel
from mlte.spec.spec import Spec
from mlte.validation.model import ValidatedSpecModel
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
        spec_artifact_model = self.spec.to_model()
        spec_body_model: SpecModel = typing.cast(
            SpecModel, spec_artifact_model.body
        )

        return ArtifactModel(
            header=self.build_artifact_header(),
            body=ValidatedSpecModel(
                spec_identifier=self.spec.identifier,
                spec=spec_body_model,
                results={
                    prop_name: {
                        measure_id: result.to_model()
                        for measure_id, result in results.items()
                    }
                    for prop_name, results in self.results.items()
                },
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

        # Build the spec and ValidatedSpec
        return ValidatedSpec(
            identifier=model.header.identifier,
            spec=Spec(
                body.spec_identifier,
                Spec.to_property_dict(body.spec.properties)
                if body.spec is not None
                else {},
            ),
            results={
                prop_name: {
                    measure_id: Result.from_model(result)
                    for measure_id, result in results.items()
                }
                for prop_name, results in body.results.items()
            },
        )

    def print_results(self, type: str = "all"):
        """Prints the validated results per property, can be filtered by result type."""
        if type not in ["all", "Success", "Failure", "Ignore"]:
            raise RuntimeError(f"Invalid type: {type}")

        for property, details in self.results.items():
            print(f"Property: {property}")
            for id, result in details.items():
                if type == "all" or type == str(result):
                    print(
                        f" > Measurement: {id}, result: {result}, details: {result.message}"
                    )

    @staticmethod
    def get_default_id() -> str:
        """Overriden"""
        return DEFAULT_VALIDATED_SPEC_ID

    def __eq__(self, other: object) -> bool:
        """Test ValidatedSpec instance for equality."""
        if not isinstance(other, ValidatedSpec):
            return False
        return self._equal(other)
