"""
mlte/web/store/api/auth/authentication.py

Handling of authentication and passwords.
"""
from passlib.context import CryptContext

from mlte.web.store.api.auth import fake_db as db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
"""Context to be used when hashing passwords."""


def authenticate_user(username: str, password: str) -> bool:
    """Validates the credentials."""
    user_in_db = db.get_user_in_db(username)
    if user_in_db is None:
        return False
    elif not _verify_password(password, user_in_db.hashed_password):
        return False
    else:
        return True


def _verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies that a plain password matches a hashed one."""
    match: bool = pwd_context.verify(plain_password, hashed_password)
    return match


def get_password_hash(password: str) -> str:
    """Gets the hash of a given plain password."""
    hash: str = pwd_context.hash(password)
    return hash
