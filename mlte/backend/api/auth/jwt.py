"""
mlte/backend/api/auth/jwt.py

Handling of JWT tokens.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional, Union

from jose import JWTError, jwt

from mlte.model.base_model import BaseModel

ALGORITHM = "HS256"
"""Token hashing algorithm."""

DEFAULT_EXPIRATION_MINS = 120
"""Default token expiration time."""

SUBJECT_CLAIM_KEY = "sub"
EXPIRATION_CLAIM_KEY = "exp"
"""Token claim keys."""


class EncodedToken(BaseModel):
    """Model for the encoded token and additional metadata."""

    encoded_token: str
    """The actual encoded token."""

    expires_in: int
    """Lifetime in seconds of the token."""


class DecodedToken(BaseModel):
    """Model for the claims inside the token."""

    username: str
    """The user name."""

    expiration_time: datetime
    """The date and time the token expires."""


def create_user_token(
    username: str, key: str, expires_delta: Optional[timedelta] = None
) -> EncodedToken:
    """Creates an access token containing a given username."""
    # Main data is username.
    claims: dict[str, Union[str, int]] = {SUBJECT_CLAIM_KEY: username}

    # Calculate expiration time, and add it to claims.
    if expires_delta is None:
        expires_delta = timedelta(minutes=DEFAULT_EXPIRATION_MINS)
    expiration_time = datetime.now(timezone.utc) + expires_delta
    claims.update({EXPIRATION_CLAIM_KEY: int(expiration_time.timestamp())})

    # Encode and sign token, and return it.
    encoded_jwt = jwt.encode(claims, key, algorithm=ALGORITHM)
    token = EncodedToken(
        encoded_token=encoded_jwt, expires_in=int(expires_delta.total_seconds())
    )
    return token


def decode_user_token(encoded_token: str, key: str) -> DecodedToken:
    """Decodes the provided user access token."""
    try:
        payload = jwt.decode(encoded_token, key, algorithms=[ALGORITHM])

        username: str = payload.get(SUBJECT_CLAIM_KEY)
        if username is None:
            raise Exception("No valid user in token")
        exp_timestamp: int = payload.get(EXPIRATION_CLAIM_KEY)
        if exp_timestamp is None:
            raise Exception("No valid expiration time in token")
        expiration_time: datetime = datetime.fromtimestamp(
            exp_timestamp, timezone.utc
        )
        decoded_token = DecodedToken(
            username=username, expiration_time=expiration_time
        )

        return decoded_token
    except JWTError as ex:
        raise Exception(f"Error decoding token: {str(ex)}")


def check_expired_token(token: DecodedToken) -> bool:
    """Checks whether the provided token has expired."""
    return token.expiration_time < datetime.now(timezone.utc)
