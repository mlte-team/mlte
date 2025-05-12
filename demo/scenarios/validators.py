"""
Standalone Validators used in this demo.
"""

from typing import Callable

from mlte.evidence.types.array import Array
from mlte.validation.validator import Validator


def all_accuracies_more_or_equal_than(threshold: float) -> Validator:
    """
    Checks if the accuracy for multiple populations is fair by checking if all of them are over the given threshold.

    :param threshold: The threshold of accuracy to check against. Its value has to be equivalent to the values later passed in the array.
    :return: A Validator to check against this.
    """
    bool_exp: Callable[[Array], bool] = lambda value: sum(
        g >= threshold for g in value.array
    ) == len(value.array)
    validator: Validator = Validator.build_validator(
        bool_exp=bool_exp,
        success=f"All accuracies are equal to or over threshold {threshold}",
        failure=f"One or more accuracies are below threshold {threshold}",
        input_types=[Array],
    )
    return validator


def p_value_greater_or_equal_to(threshold: float) -> Validator:
    """
    A RankSums array is an array with the results of the ranksums function (stat on first pos, p-value on second).

    :param threshold: The p-value we want to check against.
    :return: A Validator that checks for this.
    """
    P_VALUE_POS = 1
    bool_exp: Callable[[Array], bool] = (
        lambda value: value.array[P_VALUE_POS] >= threshold
    )
    validator: Validator = Validator.build_validator(
        bool_exp=bool_exp,
        success=f"P-Value is greater or equal to {threshold}",
        failure=f"P-Value is less than threshold {threshold}",
        input_types=[Array],
    )
    return validator
