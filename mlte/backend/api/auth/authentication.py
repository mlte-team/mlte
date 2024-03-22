"""
mlte/backend/api/auth/authentication.py

Authentication handling.
"""

from mlte.backend.api import dependencies
from mlte.user import passwords


def authenticate_user(username: str, password: str) -> bool:
    """Validates the credentials."""
    user = None
    with dependencies.user_store_session() as handle:
        try:
            user = handle.read_user(username)
        except Exception:
            # Assume any exception means we couldn't load user it.
            return False
    if not passwords.verify_password(password, user.hashed_password):
        return False
    else:
        return True
