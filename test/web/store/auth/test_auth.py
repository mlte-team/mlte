"""
test/web/store/auth/test_auth.py

Test the authentication operations
"""


from mlte.web.store.api.auth import authentication, jwt


def test_token_encode_decode() -> None:
    """Checks that a token can be encoded and decoded properly."""
    username = "myuser"

    new_token = jwt.create_user_token(username)
    decoded_username = jwt.decode_user_token(new_token.encoded_token)

    assert username == decoded_username


# TODO: test expiration claim of a token.


def test_hash_verification() -> None:
    """Checks that password can be hashed and verified."""
    password = "secret"

    hashed_pass = authentication.get_password_hash(password)
    verification_success = authentication._verify_password(
        password, hashed_pass
    )

    assert verification_success
