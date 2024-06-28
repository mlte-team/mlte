"""
test/backend/api/endpoint/test_token.py

Test the API for token endpoint
"""

from mlte.backend.api import codes
from mlte.backend.core.config import settings
from test.backend.api.endpoints.test_user import (
    create_sample_user_using_admin,
    get_sample_user,
)
from test.backend.fixture.test_api import TestAPI

TOKEN_ENDPOINT = "/token"
TOKEN_URI = f"{settings.API_PREFIX}{TOKEN_ENDPOINT}"


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


def test_no_data(test_api_fixture) -> None:
    """Request a token with no data"""
    test_api: TestAPI = test_api_fixture()
    test_client = test_api.get_test_client()
    res = test_client.post(f"{TOKEN_URI}")
    assert res.status_code == codes.UNPROCESSABLE_ENTITY


def test_valid_user(test_api_fixture) -> None:
    """Request a token with a valid user"""
    # Create user to use in test.
    test_api: TestAPI = test_api_fixture()
    test_client = test_api.get_test_client()
    user = get_sample_user()
    create_sample_user_using_admin(test_api)

    # Set up form data to get token.
    form_data = test_client._format_oauth_password_payload(
        user.username, user.password
    )

    # Request token.
    res = test_client.post(f"{TOKEN_URI}", data=form_data)

    # Check result.
    assert res.status_code == codes.OK
    assert "access_token" in res.json()


def test_invalid_user(test_api_fixture) -> None:
    """Request a token with an invalid user"""
    # Get but don't create user to use in test.
    test_api: TestAPI = test_api_fixture()
    test_client = test_api.get_test_client()
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
