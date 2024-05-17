"""
test/backend/test_token.py

Test the token endpoint
"""

import pytest

from mlte.backend.api import codes
from mlte.backend.core.config import settings
from mlte.user.model import UserCreate
from test.backend.api.endpoints.test_user import USER_ENDPOINT
from test.backend.fixture.http import (  # noqa
    FastAPITestHttpClient,
    clients,
    mem_store_and_test_http_client,
)

TOKEN_ENDPOINT = "/token"


def get_test_user() -> UserCreate:
    """Creates a simple test user."""
    username = "user1"
    email = "user1@test.com"
    password = "pass1"
    return UserCreate(username=username, email=email, password=password)


@pytest.mark.parametrize("client_fixture", clients())
def test_no_data(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Request a token with no data"""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    res = client.post(f"{settings.API_PREFIX}{TOKEN_ENDPOINT}")
    assert res.status_code == codes.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("client_fixture", clients())
def test_valid_user(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Request a token with a valid user"""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    # Create user to use in test.
    user = get_test_user()
    res = client.post(
        f"{settings.API_PREFIX}{USER_ENDPOINT}", json=user.model_dump()
    )
    print(res.content)
    assert res.status_code == codes.OK

    # Set up form data to get token.
    form_data = client._format_oauth_password_payload(
        user.username, user.password
    )

    # Request token.
    res = client.post(f"{settings.API_PREFIX}{TOKEN_ENDPOINT}", data=form_data)

    # Check result.
    assert res.status_code == codes.OK
    assert "access_token" in res.json()


@pytest.mark.parametrize("client_fixture", clients())
def test_invalid_user(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Request a token with an invalid user"""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    # Get but don't create user to use in test.
    user = get_test_user()

    # Set up form data to get token.
    form_data = client._format_oauth_password_payload(
        user.username, user.password
    )

    # Request token.
    res = client.post(f"{settings.API_PREFIX}{TOKEN_ENDPOINT}", data=form_data)

    # Check result.
    assert res.status_code == codes.BAD_REQUEST
    assert res.json()["error"] == "invalid_grant"
