"""
mlte/user/authentication.py

Handling of passwords.
"""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
"""Context to be used when hashing passwords."""


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies that a plain password matches a hashed one."""
    match: bool = pwd_context.verify(plain_password, hashed_password)
    return match


def get_password_hash(password: str) -> str:
    """Gets the hash of a given plain password."""
    hash: str = pwd_context.hash(password)
    return hash
