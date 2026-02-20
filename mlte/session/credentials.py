"""Credentials used in a session."""

from dataclasses import dataclass


@dataclass
class Credentials:
    """
    A data class to hold user credentials.
    """

    user: str
    password: str
