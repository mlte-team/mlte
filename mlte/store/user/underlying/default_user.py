"""
mlte/store/user/underlying/default_user.py

Default user.
"""

from __future__ import annotations

from mlte.user import passwords

DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "admin1234"
DEFAULT_HASHED_PASSWORD = passwords.hash_password(DEFAULT_PASSWORD)
