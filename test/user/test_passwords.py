"""
test/backend/auth/test_auth.py

Test the authentication operations
"""


from mlte.user import passwords


def test_hash_verification() -> None:
    """Checks that password can be hashed and verified."""
    password = "secret"

    hashed_pass = passwords.get_password_hash(password)
    verification_success = passwords.verify_password(password, hashed_pass)

    assert verification_success
