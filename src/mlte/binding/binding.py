"""
Implementation of Binding and related types.
"""

from __future__ import annotations
from typing import Dict, List


from mlte._global import global_state, GlobalState
from mlte.store.api import read_binding, write_binding


def _check_global_state(state: GlobalState):
    """
    Ensure that the global state contains
    information necessary to save/load results.
    """
    if not state.has_model():
        raise RuntimeError("Set model context prior to saving result.")
    if not state.has_artifact_store_uri():
        raise RuntimeError("Set artifact store URI prior to saving result.")


def _verify_integrity(description: Dict[str, List[str]]):
    """
    Verify the integrity of a Binding description.

    :param description: The description
    :type description: Dict[str, List[str]]
    """
    # Ensure that all keys are `str`
    for k in description.keys():
        if not isinstance(k, str):
            raise RuntimeError("All property identifiers must be `str`.")
    # Ensure all values are `list`
    for v in description.values():
        if not isinstance(v, list):
            raise RuntimeError("All values in Binding must be `list`.")
    # Ensure all values in each list are `str`
    for v in description.values():
        for e in v:
            if not isinstance(e, str):
                raise RuntimeError("All result identifiers must be `str`.")


class Binding:
    """
    A binding represents a mapping from properties
    to the result identifiers with which they are associated.
    """

    def __init__(self, description: Dict[str, List[str]]):
        """
        Initialize a new Binding instance.

        :param description: Description that maps properties to measurements
        :type description: Dict[str, List[str]]
        """
        _verify_integrity(description)
        self.description = description

    def identifiers_for(self, property_name: str) -> List[str]:
        """
        Return the identifiers corresponding to a particular property name.

        :param property_name: The name of the property\
        :type property_name: str
        :return: A collection of result identifiers
        :rtype: List[str]
        """
        # TODO(Kyle): Should this actually not throw on key error?
        return (
            self.description[property_name]
            if property_name in self.description
            else []
        )

    def save(self):
        """Save the Binding instance to artifact store."""
        state = global_state()
        _check_global_state(state)

        model_identifier, model_version = state.get_model()
        artifact_store_uri = state.get_artifact_store_uri()

        # Write the binding to the artifact store
        write_binding(
            artifact_store_uri,
            model_identifier,
            model_version,
            self.description,
        )

    @staticmethod
    def load() -> Binding:
        """
        Load a binding from the artifact store.

        :return: The saved binding
        :rtype: Binding
        """
        state = global_state()
        _check_global_state(state)

        model_identifier, model_version = state.get_model()
        artifact_store_uri = state.get_artifact_store_uri()

        # Read the binding from the artifact store
        data = read_binding(artifact_store_uri, model_identifier, model_version)
        return Binding(description=data)

    def __eq__(self, other: Binding) -> bool:
        """Compare Binding instances for equality."""
        return _equal(self, other)

    def __neq__(self, other: Binding) -> bool:
        """Compare binding instances for inequality."""
        return not self.__eq__(other)


def _equal(a: Binding, b: Binding) -> bool:
    """
    Determine if two binding instances are equivalent.

    :param a: Binding instance
    :type a: Binding
    :param b: Binding instance
    :type b: Binding

    :return: `True` if equal, `False` otherwise
    :rtype: bool
    """
    ad = a.description
    bd = b.description

    # Determine if keys are equivalent
    if (
        not len(ad)
        == len(bd)
        == len(set(ad.keys()).intersection(set(bd.keys())))
    ):
        return False

    # Determine if all values are equivalent
    for k in ad.keys():
        assert k in bd.keys(), "Broken invariant."
        if not _list_equal(ad[k], bd[k]):
            return False

    return True


def _list_equal(a: List[str], b: List[str]) -> bool:
    """
    Determine if the contents of two lists are equivalent, ignoring order.

    :param a: List instance
    :type a: List[str]
    :param b: List instance
    :type b: List[str]

    :return: `True` if equal, `False` otherwise
    :rtype: bool
    """
    if not len(a) == len(b):
        return False
    return len(set(a)) == len(set(b)) == len(set(a).intersection(set(b)))
