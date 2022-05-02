"""
Platform discovery.
"""

import os


def is_windows() -> bool:
    """
    Determine if the platform is Windows.

    :return: `True` if the OS is Windows, `False` otherwise.
    :rtype: bool
    """
    return os.name == "nt"


def is_nix() -> bool:
    """
    Determine if the platform is UNIX-like.

    :return: `True` if the OS is UNIX-like, `False` otherwise.
    :rtype: bool
    """
    return os.name == "posix"
