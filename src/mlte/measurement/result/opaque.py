"""
An opaque evaluation result, without semantics.
"""

from __future__ import annotations

from typing import Dict, Any

from .result import Result
from ..measurement_metadata import MeasurementMetadata


class Opaque(Result):
    """
    The 'default' Result instance for measurements that do not provide their own.
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
