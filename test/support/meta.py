"""
Meta-support.
"""

from os.path import abspath, dirname


def path_to_support() -> str:
    """
    Get the path to the test `support` directory.
    :return The path
    """
    return abspath(dirname(__file__))
