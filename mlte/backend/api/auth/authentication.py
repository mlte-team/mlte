"""
mlte/backend/api/auth/authentication.py

Authentication handling.
"""

from mlte.store.user.store_session import UserStoreSession
from mlte.user import passwords


def authenticate_user(
    username: str, password: str, user_store_session: UserStoreSession
) -> bool:
    """Validates the credentials."""
    user = None
    try:
        user = user_store_session.user_mapper.read(username)
    except Exception as ex:
        # Assume any exception means we couldn't load user it.
        print(
            f"Error reading user; type is: {ex.__class__.__name__}, error is: {ex}"
        )
        return False
    if not passwords.verify_password(password, user.hashed_password):
        # print(f"Could not verify password <{password}> vs hashed <{user.hashed_password}>")
        return False
    else:
        return True
