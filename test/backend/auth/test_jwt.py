"""
test/backend/auth/test_jwt.py

Test JWT functions.
"""

from datetime import datetime, timedelta, timezone

from mlte.backend.api.auth import jwt


def test_token_encode_decode() -> None:
    """Checks that a token can be encoded and decoded properly."""
    username = "myuser"
    expiration_delta = timedelta(minutes=2)
    test_key = "1231414214"

    new_token = jwt.create_user_token(username, test_key, expiration_delta)
    decoded_token = jwt.decode_user_token(new_token.encoded_token, test_key)

    assert username == decoded_token.username
    assert (
        datetime.now(timezone.utc) + expiration_delta
    ) >= decoded_token.expiration_time
