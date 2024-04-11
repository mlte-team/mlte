"""
test/backend/auth/test_authorization.py

Test the authorization operations
"""

from mlte.backend.api.auth import authorization, jwt


def test_get_username_from_token_success():
    """Checks for properly getting username from a token."""
    username = "user1"
    test_key = "asdadsd78"
    token = jwt.create_user_token(username, test_key)

    decoded_username = authorization.get_username_from_token(
        token.encoded_token, test_key
    )

    assert decoded_username == username
