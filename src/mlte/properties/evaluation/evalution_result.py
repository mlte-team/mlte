"""
Indicates the outcome of property evaluation.
"""

import abc


class EvaluationResult(metaclass=abc.ABCMeta):
    """
    The EvaluationResult class serves as the base class of
    all semantically-enriched property evaluation results.
    The EvaluationResult provides a common interface for
    inspecting the results of property evaluation, and also
    encapsulates the functionality required to uniquely
    associate evaluation results with the originating property.
    """

    def __init__(self, property):
        """
        Initialize an EvaluationResult instance.

        :param property: The generating property
        :type property: Property
        """
        # Store the token of the generating property
        self.token = property.token
