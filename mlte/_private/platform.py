"""
mlte/_private/platform.py

Platform discovery.
"""

import os
import sys


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


def is_macos():
    """
    Determine if the platform is macOS.

    :return: `True` if the OS is macOS, `False` otherwise.
    :rtype: bool
    """
    return sys.platform == "darwin"
