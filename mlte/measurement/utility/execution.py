"""
mlte/measurement/utility/execution.py

Utilities for execution of measurements.
"""

import concurrent.futures
from typing import Any, Callable, List


def concurrently(*callables: Callable[[], Any]) -> List[Any]:
    """
    Run an arbitrary number of functions concurrently.

    :param callables: The callables to execute

    :return: The results of all callables, in
    the order in which they were passed to call
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(callable) for callable in callables]
        return [future.result() for future in futures]
