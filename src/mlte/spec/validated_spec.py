"""
ValidatedSpec class implementation.
"""

from __future__ import annotations

from typing import Any

from mlte._global import global_state
from mlte.api import read_validatedspec, write_validatedspec


# -----------------------------------------------------------------------------
# ValidatedSpec
# -----------------------------------------------------------------------------


class ValidatedSpec:
    """
    ValidatedSpec represents a spec with validated results.
    """

    def __init__(self, document: dict[str, Any]):
        """
        Initialize a ValidatedSpec instance.

        :param document: The data produced by the Spec
        :type document: dict[str, Any]]
        """
        self.document = document
        """The document produced by the Spec."""

    def save(self):
        """Save ValidatedSpec instance to artifact store."""
        state = global_state()
        state.ensure_initialized()

        model_identifier, model_version = state.get_model()
        artifact_store_uri = state.get_artifact_store_uri()
        write_validatedspec(
            artifact_store_uri, model_identifier, model_version, self.document
        )

    @staticmethod
    def load() -> ValidatedSpec:
        """
        Load ValidatedSpec instance from artifact store.

        :return: The ValidatedSpec instance
        :rtype: ValidatedSpec
        """
        state = global_state()
        state.ensure_initialized()

        model_identifier, model_version = state.get_model()
        artifact_store_uri = state.get_artifact_store_uri()

        return ValidatedSpec(
            document=read_validatedspec(
                artifact_store_uri, model_identifier, model_version
            )
        )

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
    # TODO(Kyle): Implement this functionality when ValidatedSpec fleshed out
    akeys = set(a.document.keys())
    bkeys = set(b.document.keys())
    return len(akeys) == len(bkeys) == len(akeys.intersection(bkeys))
