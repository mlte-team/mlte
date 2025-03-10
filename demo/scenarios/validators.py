"""
Standalone Validators used in this demo.
"""

from mlte.validation.validator import Validator


def all_accuracies_more_or_equal_than(threshold: float) -> Validator:
    """Checks if the accuracy for multiple populations is fair by checking if all of them are over the given threshold."""
    validator: Validator = Validator.build_validator(
        bool_exp=lambda value: sum(g >= threshold for g in value.array)
        == len(value.array),
        success=f"All accuracies are equal to or over threshold {threshold}",
        failure=f"One or more accuracies are below threshold {threshold}",
    )
    return validator


def p_value_greater_or_equal_to(threshold: float) -> Validator:
    """A RankSums array is an array with the results of the ranksums function (stat on first pos, p-value on second)."""
    validator: Validator = Validator.build_validator(
        bool_exp=lambda value: value.array[1] >= threshold,
        success=f"P-Value is greater or equal to {threshold}",
        failure=f"P-Value is less than threshold {threshold}",
    )
    return validator
