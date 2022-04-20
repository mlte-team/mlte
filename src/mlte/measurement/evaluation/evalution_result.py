"""
Indicates the outcome of measurement evaluation.
"""

import abc


class EvaluationResult(metaclass=abc.ABCMeta):
    """
    The EvaluationResult class serves as the base class of
    all semantically-enriched measurement evaluation results.
    The EvaluationResult provides a common interface for
    inspecting the results of measurement evaluation, and also
    encapsulates the functionality required to uniquely
    associate evaluation results with the originating measurement.
    """

    def __init__(self, measurement):
        """
        Initialize an EvaluationResult instance.

        :param measurement: The generating measurement
        :type measurement: Measurement
        """
        # Store the name of the generating measurement
        self.measurement_name = measurement.name
