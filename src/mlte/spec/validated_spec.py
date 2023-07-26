"""
ValidatedSpec class implementation.
"""

from __future__ import annotations

from typing import Any

from mlte.spec import Spec
from mlte.validation import Result
from mlte.session import session
from mlte.api import read_validatedspec, write_validatedspec


# -----------------------------------------------------------------------------
# ValidatedSpec
# -----------------------------------------------------------------------------


class ValidatedSpec:
    """
    ValidatedSpec represents a spec with validated results.
    """

    def __init__(self, spec: Spec, results: dict[str, Result]):
        """
        Initialize a ValidatedSpec instance.

        :param spec: The Spec
        :type spec: Spec
        :param results: The validation Results for the Spec
        :type results: dict[str, Result]
        """

        self.spec = spec
        """The spec that we validated."""

        self.results = results
        """The validation results for the spec."""

        # Check that all requirements have results.
        for _, requirement_list in self.spec.requirements.items():
            for requirement in requirement_list:
                if str(requirement.identifier) not in self.results:
                    raise RuntimeError(
                        f"Requirement '{requirement.identifier}' does not have a result."
                    )

    def save(self):
        """Save ValidatedSpec instance to artifact store."""
        sesh = session()

        write_validatedspec(
            sesh.store.uri.uri,
            sesh.context.model,
            sesh.context.version,
            self.to_json(),
        )

    @staticmethod
    def load() -> ValidatedSpec:
        """
        Load ValidatedSpec instance from artifact store.

        :return: The ValidatedSpec instance
        :rtype: ValidatedSpec
        """
        sesh = session()

        document = read_validatedspec(
            sesh.store.uri.uri, sesh.context.model, sesh.context.version
        )
        return ValidatedSpec.from_json(document)

    def to_json(self) -> dict[str, Any]:
        """
        Generates a JSON representation of the ValidatedSpec.

        :return: The serialized content
        :rtype: dict[str, Any]
        """
        # Generate the spec document, and add the result for each requirement.
        spec_document: dict[
            str, list[dict[str, list[dict[str, Any]]]]
        ] = self.spec.to_json()
        for property in spec_document["properties"]:
            for req in property["requirements"]:
                req["result"] = self.results[req["identifier"]].to_json()

        return spec_document

    @staticmethod
    def from_json(json: dict[str, Any]) -> ValidatedSpec:
        """
        Deserialize ValidatedSpec content from JSON document.

        :param json: The json document
        :type json: dict[str, Any]

        :return: The deserialized specification
        :rtype: ValidatedSpec
        """
        spec = Spec.from_json(json)
        results: dict[str, Result] = {}
        for property in json["properties"]:
            for req in property["requirements"]:
                results[req["identifier"]] = Result.from_json(req["result"])

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
    :type a: ValidatedSpec
    :param b: Input instance
    :type b: ValidatedSpec

    :return: `True` if instances are equal, `False` otherwise
    :rtype: bool
    """
    return a.spec == b.spec and a.results == b.results
