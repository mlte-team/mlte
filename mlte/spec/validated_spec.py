"""
mlte/spec/validated_spec.py

ValidatedSpec class implementation.
"""

from __future__ import annotations

# from typying import List
from typing import Any, Dict

from mlte.spec.spec import Spec
from mlte.validation.result import Result
from mlte.session import session
from mlte.api import read_validatedspec, write_validatedspec


# -----------------------------------------------------------------------------
# ValidatedSpec
# -----------------------------------------------------------------------------


class ValidatedSpec:
    """
    ValidatedSpec represents a spec with validated results.
    """

    def __init__(self, spec: Spec, results: Dict[str, Result]):
        """
        Initialize a ValidatedSpec instance.

        :param spec: The Spec
        :type spec: Spec
        :param results: The validation Results for the Spec
        :type results: Dict[str, Result]
        """

        self.spec = spec
        """The spec that we validated."""

        self.results = results
        """The validation results for the spec."""

        # Check that all conditions have results.
        for conditions in self.spec.properties.values():
            for measurement_id in conditions.keys():
                if measurement_id not in self.results:
                    raise RuntimeError(
                        f"Id '{measurement_id}' does not have a result."
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

    def to_json(self) -> Dict[str, Any]:
        """
        Generates a JSON representation of the ValidatedSpec.

        :return: The serialized content
        :rtype: Dict[str, Any]
        """
        # Generate the spec document, and add the result for each requirement.
        # spec_document: Dict[
        #    str, List[Dict[str, List[Dict[str, Any]]]]
        # ] = self.spec.to_json()
        # for property in spec_document["properties"]:
        #    for req in property["requirements"]:
        #        req["result"] = self.results[req["identifier"]].to_json()

        # return spec_document
        return {}

    @staticmethod
    def from_json(json: Dict[str, Any]) -> ValidatedSpec:
        """
        Deserialize ValidatedSpec content from JSON document.

        :param json: The json document
        :type json: Dict[str, Any]

        :return: The deserialized specification
        :rtype: ValidatedSpec
        """
        # spec = Spec.from_json(json)
        # results: Dict[str, Result] = {}
        # for property in json["properties"]:
        #    for req in property["requirements"]:
        #        results[req["identifier"]] = Result.from_json(req["result"])

        # return ValidatedSpec(spec, results)
        return ValidatedSpec(Spec("t", {}), {})

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
