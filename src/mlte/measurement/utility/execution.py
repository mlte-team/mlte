"""
Utilities for execution of measurements.
"""

import concurrent.futures
from typing import Callable, Any, List


def concurrently(*callables: Callable[[], Any]) -> List[Any]:
    """
    Run an arbitrary number of functions concurrently.

    :param callables: The callables to execute
    :type callables: Callable[[], Any]

    :return: The results of all callables, in
    the order in which they were passed to call
    :rtype: List[Any]
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(callable) for callable in callables]
        return [future.result() for future in futures]
