"""
An opaque evaluation value, without semantics.
"""

from __future__ import annotations

from typing import Dict, Any, List

from .value import Value
from mlte.measurement_metadata.measurement_metadata import MeasurementMetadata


class Opaque(Value):
    """
    The 'default' Value instance for
    measurements that do not provide their own.
    """

    def __init__(
        self, measurement_metadata: MeasurementMetadata, data: Dict[str, Any]
    ):
        """
        Initialize an Opaque instance.

        :param measurement_metadata: The generating measurement's metadata
        :type measurement: MeasurementMetadata
        :param data: The output of the measurement
        :type data: Dict
        """
        super().__init__(self, measurement_metadata)

        self.data = data
        """The raw output from measurement execution."""

    def serialize(self) -> Dict[str, Any]:
        """
        Serialize an Opaque to a JSON object.

        :return: The JSON object
        :rtype: Dict[str, Any]
        """
        return {"data": self.data}

    @staticmethod
    def deserialize(
        measurement_metadata: MeasurementMetadata, json: Dict[str, Any]
    ) -> Opaque:
        """
        Deserialize an Opaque from a JSON object.

        :param measurement_metadata: The generating measurement's metadata
        :type measurement_metadata: MeasurementMetadata
        :param json: The JSON object
        :type json: Dict[str, Any]

        :return: The deserialized instance
        :rtype: Opaque
        """
        return Opaque(measurement_metadata, json["data"])

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
    return (
        a.measurement_typename == b.measurement_typename
        and a.identifier == b.identifier
        and _equal_helper_dict(a.data, b.data)
    )


def _equal_helper_dict(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
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


def _equal_helper_list(a: List[Any], b: List[Any]) -> bool:
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
