"""
An opaque evaluation result, without semantics.
"""

from typing import Dict, Any

from .evalution_result import EvaluationResult


class Opaque(EvaluationResult):
    """
    The 'default' EvaluationResult instance for custom
    measurements that do not define a `semantics()` method.
    """

    def __init__(self, measurement, data: Dict[str, Any]):
        """
        Initialize an Opaque instance.

        :param measurement: The generating measurement
        :type measurement: Measurement
        :param data: The output of the measurement
        :type data: Dict
        """
        super().__init__(measurement)

        self.data = data
        """The raw output from measurement execution."""

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
