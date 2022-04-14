"""
An opaque evaluation result, without semantics.
"""

from typing import Dict, Any

from .evalution_result import EvaluationResult


class Opaque(EvaluationResult):
    """
    The 'default' EvaluationResult instance for custom
    properties that do not define a `semantics()` method.
    """

    def __init__(self, property, data: Dict[str, Any]):
        """
        Initialize an Opaque instance.

        :param property: The generating property
        :type property: Property
        :param data: The output of the property
        :type data: Dict
        """
        super().__init__(property)
        # The raw output dictionary from property invocation
        self.data = data
