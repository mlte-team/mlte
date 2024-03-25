"""
test/backend/auth/test_jwt.py

Test JWT functions.
"""


from mlte.backend.api.auth import jwt


def test_token_encode_decode() -> None:
    """Checks that a token can be encoded and decoded properly."""
    username = "myuser"
    test_key = "1231414214"

    new_token = jwt.create_user_token(username, test_key)
    decoded_username = jwt.decode_user_token(new_token.encoded_token, test_key)

    assert username == decoded_username


# TODO: test expiration claim of a token.
