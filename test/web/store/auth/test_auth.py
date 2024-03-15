"""
test/web/store/auth/test_auth.py

Test the authentication operations
"""


from mlte.web.store.api.auth import token


def test_token_encode_decode() -> None:
    """Checks that a token can be encoded and decoded properly."""
    username = "myuser"

    new_token = token.create_user_token(username)
    decoded_username = token.decode_user_token(new_token)

    assert username == decoded_username
