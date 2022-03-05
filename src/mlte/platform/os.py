"""
Platform discovery.
"""

import os


def is_windows() -> bool:
    """
    Determine if the platform is Windows.

    :return `True` if the OS is Windows, `False` otherwise.
    """
    return os.name == "nt"


def is_nix() -> bool:
    """
    Determine if the platform is *nix.

    :return `True` if the OS is *nix, `False` otherwise.
    """
    return os.name == "posix"
