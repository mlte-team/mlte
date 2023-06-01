"""
An opaque evaluation value, without semantics.
"""
from __future__ import annotations

from typing import Any

from ..value import Value
from mlte.evidence.evidence_metadata import EvidenceMetadata


class Opaque(Value):
    """
    The 'default' Value instance for
    measurements that do not provide their own.
    """

    def __init__(
        self, evidence_metadata: EvidenceMetadata, data: dict[str, Any]
    ):
        """
        Initialize an Opaque instance.

        :param evidence_metadata: The generating measurement's metadata
        :type evidence_metadata: EvidenceMetadata
        :param data: The output of the measurement
        :type data: dict
        """
        super().__init__(self, evidence_metadata)

        self.data = data
        """The raw output from measurement execution."""

    def serialize(self) -> dict[str, Any]:
        """
        Serialize an Opaque to a JSON object.

        :return: The JSON object
        :rtype: dict[str, Any]
        """
        return {"data": self.data}

    @staticmethod
    def deserialize(
        evidence_metadata: EvidenceMetadata, json: dict[str, Any]
    ) -> Opaque:
        """
        Deserialize an Opaque from a JSON object.

        :param evidence_metadata: The generating measurement's metadata
        :type evidence_metadata: EvidenceMetadata
        :param json: The JSON object
        :type json: dict[str, Any]

        :return: The deserialized instance
        :rtype: Opaque
        """
        return Opaque(evidence_metadata, json["data"])

    def __getitem__(self, key: str) -> Any:
        """
        Access an item from the wrapped data object.

        :param key: The key that identifies the item to access
        :type key: str

        :return: The value associated with `key`.
        :rtype: Any

        :raises KeyError: If the key is not present
        """
        if key not in self.data:
            raise KeyError(f"Key {key} not found.")
        return self.data[key]

    def __setitem__(self, key: str, value: str) -> None:
        """Raise ValueError to indicate Opaque is read-only."""
        raise ValueError("Opaque is read-only.")

    def __eq__(self, other: object) -> bool:
        """Compare Opaque instances for equality."""
        if not isinstance(other, Opaque):
            return False
        reference: Opaque = other
        return _equal(self, reference)

    def __neq__(self, other: object) -> bool:
        """Compare Opaque instances for inequality."""
        return not self.__eq__(other)


def _equal(a: Opaque, b: Opaque) -> bool:
    return a.metadata == b.metadata and _equal_helper_dict(a.data, b.data)


def _equal_helper_dict(a: dict[str, Any], b: dict[str, Any]) -> bool:
    akeys = set(a.keys())
    bkeys = set(b.keys())
    if not (len(akeys) == len(bkeys) == len(akeys.intersection(bkeys))):
        return False

    for k in akeys:
        assert k in a and k in b, "Broken invariant."
        if not isinstance(a[k], type(b[k])):
            return False

        # NOTE(Kyle): This only considers dict and list for
        # custom comparison; expand to include other containers
        if isinstance(a[k], dict):
            if not _equal_helper_dict(a[k], b[k]):
                return False
        elif isinstance(a[k], list):
            if not _equal_helper_list(a[k], b[k]):
                return False
        else:
            if a[k] != b[k]:
                return False

    return True


def _equal_helper_list(a: list[Any], b: list[Any]) -> bool:
    if len(a) != len(b):
        return False

    for i in range(len(a)):
        aitem = a[i]
        bitem = b[i]

        if type(aitem) != type(bitem):
            return False

        if isinstance(aitem, dict):
            if not _equal_helper_dict(aitem, bitem):
                return False
        elif isinstance(aitem, list):
            if not _equal_helper_list(aitem, bitem):
                return False
        else:
            if aitem != bitem:
                return False

    return True
