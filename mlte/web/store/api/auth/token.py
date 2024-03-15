"""
mlte/web/store/api/auth/token.py

Handling of authentication tokens.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import JWTError, jwt

from mlte.model.base_model import BaseModel

SECRET_KEY = "399fd92f61c99e35d7f2f6fdb9d65293c4047f9ac500af1886b8868b495f20b3"
"""Used for signing tokens."""

ALGORITHM = "HS256"
"""Token hashing algorithm."""

ACCESS_TOKEN_EXPIRE_MINUTES = 30
"""Default token expiration time."""

DEFAULT_TOKEN_TYPE = "bearer"
"""Default token type."""

SUBJECT_CLAIM_KEY = "sub"
EXPIRATION_CLAIM_KEY = "exp"
"""Token claim keys."""


class Token(BaseModel):
    """Model for the token to return."""

    access_token: str
    """The actual encoded token."""

    token_type: str = DEFAULT_TOKEN_TYPE
    """The token type, currently only supporting one default value."""


def create_user_token(username: str) -> Token:
    """Creates a user token given a username."""
    data = {SUBJECT_CLAIM_KEY: username}
    access_token = _create_access_token(data)
    return Token(access_token=access_token)


def _create_access_token(
    data: dict[str, Any], expires_delta: Optional[timedelta] = None
):
    """Creates a token given a data dictionary and an expiration time."""
    to_encode = data.copy()
    if expires_delta:
        expiration_time = datetime.now(timezone.utc) + expires_delta
    else:
        expiration_time = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({EXPIRATION_CLAIM_KEY: expiration_time})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_user_token(token: Token) -> str:
    """Decodes the provided user token."""
    try:
        payload = jwt.decode(
            token.access_token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        username: str = payload.get(SUBJECT_CLAIM_KEY)
        if username is None:
            raise Exception("No valid user in token")
        return username
    except JWTError as ex:
        raise Exception(f"Error decoding token: {str(ex)}")
