"""
mlte/user/model.py

Model implementation for a User.
"""

from typing import Optional

from mlte.model import BaseModel


class User(BaseModel):
    """A model class representing a user of the system"""

    username: str
    """The username to uniquely identify a user."""

    email: Optional[str] = None
    """An optional email associated to the user."""

    full_name: Optional[str] = None
    """The full name of the user."""

    disabled: bool = False
    """Whether the user is disabled."""


class StoredUser(User):
    """User with additional information only used locally when stored."""

    hashed_password: str
    """The hashed password of the user."""
