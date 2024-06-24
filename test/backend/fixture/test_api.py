"""
test/backend/fixture/test_api.py

Test API.
"""

from __future__ import annotations

import typing
from typing import Any, Dict, Optional

import httpx
from fastapi.testclient import TestClient

import mlte.backend.app_factory as app_factory
import test.store.user.fixture as user_store_fixture
from mlte.backend.api import codes
from mlte.backend.core.config import settings
from mlte.backend.state import state
from mlte.model.base_model import BaseModel
from mlte.store.common.http_clients import HttpClientType, OAuthHttpClient
from mlte.store.user.underlying.memory import InMemoryUserStore
from mlte.user.model import BasicUser, User, UserWithPassword
from test.backend.fixture import test_users
from test.store.artifact import artifact_store_creators

TEST_JWT_TOKEN_SECRET = "asdahsjh23423974hdasd"
"""JWT token secret used for signing tokens."""


# -----------------------------------------------------------------------------
# Test HTTP client based on FastAPI's TestClient.
# -----------------------------------------------------------------------------


class FastAPITestHttpClient(OAuthHttpClient):
    """An HTTP client based on FastAPI's TestClient."""

    def __init__(
        self,
        client: TestClient,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> None:
        super().__init__(HttpClientType.TESTCLIENT, username, password)

        self.client = client
        """The underlying client."""

    def get(self, url: str, **kwargs) -> httpx.Response:
        return self.client.get(url, headers=self.headers, **kwargs)

    def post(
        self, url: str, data: Any = None, json: Any = None, **kwargs
    ) -> httpx.Response:
        return self.client.post(
            url, headers=self.headers, data=data, json=json, **kwargs
        )

    def put(
        self, url: str, data: Any = None, json: Any = None, **kwargs
    ) -> httpx.Response:
        return self.client.put(
            url, headers=self.headers, data=data, json=json, **kwargs
        )

    def delete(self, url: str, **kwargs) -> httpx.Response:
        return self.client.delete(url, headers=self.headers, **kwargs)


# -----------------------------------------------------------------------------
# Test Api.
# -----------------------------------------------------------------------------


class TestAPI:
    """An API to be used for testing, using memory stores."""

    def __init__(self) -> None:
        """Setup API, configure to use memory artifact store and create app itself."""
        # Set up API global state.
        state.set_user_store(user_store_fixture.create_memory_store())
        state.set_artifact_store(artifact_store_creators.create_memory_store())
        state.set_token_key(TEST_JWT_TOKEN_SECRET)

        # Create and store app.
        self.app = app_factory.create()

        # Default user.
        self.user: Optional[UserWithPassword] = None

    def set_users(self, user: Optional[UserWithPassword]):
        """Add user and an admin user."""
        user_store = typing.cast(InMemoryUserStore, state.user_store)
        self.user = user
        if user is not None:
            self._set_user_in_mem_store(user, user_store)
        self._set_user_in_mem_store(test_users.build_admin_user(), user_store)

    @staticmethod
    def _set_user_in_mem_store(
        user: UserWithPassword, user_store: InMemoryUserStore
    ):
        # NOTE: Totally ignores interface and does this directly to avoid hashing password each time, to speed up tests.
        # Then edits it to ensure groups are up to date as expected.
        # NOTE: Assumes user is using default test password.
        user_store.storage.users[user.username] = User(
            hashed_password=test_users.TEST_API_HASHED_PASS, **user.model_dump()
        )
        basic_user = BasicUser(
            **user_store.storage.users[user.username].model_dump()
        )
        user_store.session().user_mapper.edit(basic_user)

    def get_test_client(self) -> FastAPITestHttpClient:
        """
        Return a test HTTP client.
        :return: The client
        """
        if self.user is None:
            self.user = test_users.build_test_user()
        return self._get_authenticated_client(self.user)

    def get_test_client_for_admin(self) -> FastAPITestHttpClient:
        """
        Return a test HTTP client for admin user
        :return: The client
        """
        return self._get_authenticated_client(test_users.build_admin_user())

    def _get_authenticated_client(
        self, user: UserWithPassword
    ) -> FastAPITestHttpClient:
        """Returns a client configured for test and authenticated."""
        # Create the test client, and authenticate to get token and allow protected endpoints to work.
        admin_client = FastAPITestHttpClient(TestClient(self.app))
        admin_client.username = user.username
        admin_client.password = user.password
        admin_client.authenticate(f"{settings.API_PREFIX}")
        return admin_client

    def admin_create_entity(
        self,
        entity: BaseModel,
        uri: str,
    ) -> dict[str, Any]:
        """Create the given entity using an admin."""
        admin_client = self.get_test_client_for_admin()
        res = admin_client.post(f"{uri}", json=entity.model_dump())
        assert res.status_code == codes.OK
        return typing.cast(Dict[str, Any], res.json())

    def admin_read_entity(self, entity_id: str, uri: str) -> dict[str, Any]:
        """Get the given entity using an admin."""
        admin_client = self.get_test_client_for_admin()
        res = admin_client.get(f"{uri}/{entity_id}")
        assert res.status_code == codes.OK
        return typing.cast(Dict[str, Any], res.json())
