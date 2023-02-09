"""
BoundSpec class implementation.
"""

from __future__ import annotations

from typing import Dict, Any

from mlte._global import global_state, GlobalState
from mlte.store.api import read_boundspec, write_boundspec


def _check_global_state(state: GlobalState):
    """
    Ensure that the global state contains
    information necessary to save/load results.
    """
    if not state.has_model():
        raise RuntimeError("Set model context prior to saving result.")
    if not state.has_artifact_store_uri():
        raise RuntimeError("Set artifact store URI prior to saving result.")


# -----------------------------------------------------------------------------
# BoundSpec
# -----------------------------------------------------------------------------


class BoundSpec:
    """
    BoundSpec represents the result of binding results
    to specific properties within a specification.
    """

    def __init__(self, document: Dict[str, Any]):
        """
        Initialize a BoundSpec instance.

        :param document: The data produced by the Spec
        :type document: Dict[str, Any]]
        """
        self.document = document
        """The document produced by the Spec."""

    def save(self):
        """Save BoundSpec instance to artifact store."""
        state = global_state()
        _check_global_state(state)

        model_identifier, model_version = state.get_model()
        artifact_store_uri = state.get_artifact_store_uri()
        write_boundspec(
            artifact_store_uri, model_identifier, model_version, self.document
        )

    @staticmethod
    def load() -> BoundSpec:
        """
        Load BoundSpec instance from artifact store.

        :return: The BoundSpec instance
        :rtype: BoundSpec
        """
        state = global_state()
        _check_global_state(state)

        model_identifier, model_version = state.get_model()
        artifact_store_uri = state.get_artifact_store_uri()

        return BoundSpec(
            document=read_boundspec(
                artifact_store_uri, model_identifier, model_version
            )
        )

    def __eq__(self, other: object) -> bool:
        """Test BoundSpec instance for equality."""
        if not isinstance(other, BoundSpec):
            return False
        return _equal(self, other)

    def __neq__(self, other: object) -> bool:
        """Test BoundSpec instance for inequality."""
        return not self.__eq__(other)


def _equal(a: BoundSpec, b: BoundSpec) -> bool:
    """
    Determine if two BoundSpec instances are equal.

    :param a: Input instance
    :type a: BoundSpec
    :param b: Input instance
    :type b: BoundSpec

    :return: `True` if instances are equal, `False` otherwise
    :rtype: bool
    """
    # TODO(Kyle): Implement this functionality when BoundSpec fleshed out
    akeys = set(a.document.keys())
    bkeys = set(b.document.keys())
    return len(akeys) == len(bkeys) == len(akeys.intersection(bkeys))
