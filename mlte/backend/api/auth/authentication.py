"""
mlte/backend/api/auth/authentication.py

Authentication handling.
"""

from mlte.store.user.store import UserStoreSession
from mlte.user import passwords


def authenticate_user(
    username: str, password: str, user_store_session: UserStoreSession
) -> bool:
    """Validates the credentials."""
    user = None
    try:
        user = user_store_session.read_user(username)
    except Exception as ex:
        # Assume any exception means we couldn't load user it.
        print(f"Error reading user: {ex}")
        return False
    if not passwords.verify_password(password, user.hashed_password):
        print("Could not verify password")
        return False
    else:
        return True
