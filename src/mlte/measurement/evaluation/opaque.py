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
