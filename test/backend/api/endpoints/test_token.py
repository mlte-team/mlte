"""
test/backend/api/endpoint/test_token.py

Test the API for token endpoint
"""

from mlte.backend.api import codes
from mlte.backend.core.config import settings
from mlte.user.model import UserCreate
from test.backend.fixture.http import (
    FastAPITestHttpClient,
    get_client_for_admin,
)

TOKEN_ENDPOINT = "/token"
TOKEN_URI = f"{settings.API_PREFIX}{TOKEN_ENDPOINT}"

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def get_sample_user() -> UserCreate:
    """Creates a simple test user."""
    username = "user1"
    email = "user1@test.com"
    password = "pass1"
    return UserCreate(username=username, email=email, password=password)


def create_sample_user(test_client: FastAPITestHttpClient) -> None:
    """Create sample user."""
    admin_client = get_client_for_admin(test_client)

    sample_user = get_sample_user()
    res = admin_client.post(
        f"{settings.API_PREFIX}/user", json=sample_user.model_dump()
    )
    assert res.status_code == codes.OK


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


def test_no_data(test_client_fix) -> None:
    """Request a token with no data"""
    test_client: FastAPITestHttpClient = test_client_fix(None)
    res = test_client.post(f"{TOKEN_URI}")
    assert res.status_code == codes.UNPROCESSABLE_ENTITY


def test_valid_user(test_client_fix) -> None:
    """Request a token with a valid user"""
    # Create user to use in test.
    test_client: FastAPITestHttpClient = test_client_fix(None)
    user = get_sample_user()
    create_sample_user(test_client)

    # Set up form data to get token.
    form_data = test_client._format_oauth_password_payload(
        user.username, user.password
    )

    # Request token.
    res = test_client.post(f"{TOKEN_URI}", data=form_data)

    # Check result.
    assert res.status_code == codes.OK
    assert "access_token" in res.json()


def test_invalid_user(test_client_fix) -> None:
    """Request a token with an invalid user"""
    # Get but don't create user to use in test.
    test_client: FastAPITestHttpClient = test_client_fix(None)
    user = get_sample_user()

    # Set up form data to get token.
    form_data = test_client._format_oauth_password_payload(
        user.username, user.password
    )

    # Request token.
    res = test_client.post(f"{TOKEN_URI}", data=form_data)

    # Check result.
    assert res.status_code == codes.BAD_REQUEST
    assert res.json()["error"] == "invalid_grant"
