"""
Standalone Validators used in this demo.
"""

from typing import Callable

from mlte.evidence.types.array import Array
from mlte.validation.validator import Validator


def passed_percent_more_or_equal_then(threshold: float) -> Validator:
    """
    Checks if an array of pass/fail values have pass above a given threshold.

    :param threshold: The threshold of required pass tests.
    :return: A validator to check against this.
    """
    bool_exp: Callable[[Array], bool] = (
        lambda value: sum(g for g in value.array) / max(len(value.array), 1)
        >= threshold
    )
    validator: Validator = Validator.build_validator(
        bool_exp=bool_exp,
        success=f"The fraction of passes is at or over threshold {threshold}",
        failure=f"The fraction of passes is below threshold  {threshold}",
        input_types=[Array],
    )
    return validator
