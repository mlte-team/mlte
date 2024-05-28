"""
test/backend/api/endpoint/test_token.py

Test the API for token endpoint
"""

from mlte.backend.api import codes
from mlte.backend.core.config import settings
from mlte.user.model import UserCreate
from test.backend.api.endpoints.test_user import USER_ENDPOINT
from test.backend.fixture.http import FastAPITestHttpClient

TOKEN_ENDPOINT = "/token"


def get_test_user() -> UserCreate:
    """Creates a simple test user."""
    username = "user1"
    email = "user1@test.com"
    password = "pass1"
    return UserCreate(username=username, email=email, password=password)


def test_no_data(test_client: FastAPITestHttpClient) -> None:  # noqa
    """Request a token with no data"""
    res = test_client.post(f"{settings.API_PREFIX}{TOKEN_ENDPOINT}")
    assert res.status_code == codes.UNPROCESSABLE_ENTITY


def test_valid_user(test_client: FastAPITestHttpClient) -> None:  # noqa
    """Request a token with a valid user"""
    # Create user to use in test.
    user = get_test_user()
    res = test_client.post(
        f"{settings.API_PREFIX}{USER_ENDPOINT}", json=user.model_dump()
    )
    print(res.content)
    assert res.status_code == codes.OK

    # Set up form data to get token.
    form_data = test_client._format_oauth_password_payload(
        user.username, user.password
    )

    # Request token.
    res = test_client.post(
        f"{settings.API_PREFIX}{TOKEN_ENDPOINT}", data=form_data
    )

    # Check result.
    assert res.status_code == codes.OK
    assert "access_token" in res.json()


def test_invalid_user(test_client: FastAPITestHttpClient) -> None:  # noqa
    """Request a token with an invalid user"""
    # Get but don't create user to use in test.
    user = get_test_user()

    # Set up form data to get token.
    form_data = test_client._format_oauth_password_payload(
        user.username, user.password
    )

    # Request token.
    res = test_client.post(
        f"{settings.API_PREFIX}{TOKEN_ENDPOINT}", data=form_data
    )

    # Check result.
    assert res.status_code == codes.BAD_REQUEST
    assert res.json()["error"] == "invalid_grant"
