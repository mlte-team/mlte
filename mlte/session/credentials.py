"""Credentials used in a session."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Credentials:
    """
    A data class to hold user credentials.
    """

    user: str
    password: Optional[str]
