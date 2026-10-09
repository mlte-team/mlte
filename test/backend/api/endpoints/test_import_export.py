"""Test the API for import and export operations."""

import io
import json
import zipfile

import pytest

from mlte.backend.api import codes
from mlte.backend.core.config import settings
from mlte.user.model import ResourceType, UserWithPassword
from test.backend.fixture import user_generator
from test.backend.fixture.test_api import TestAPI
from test.store.import_export.conftest import ALL_EXPORT_DATA

# -----------------------------------------------------------------------------
# Tests - Import
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_write_permissions(
        ResourceType.STORE,
    ),
)
def test_import(test_api_fixture, api_user: UserWithPassword) -> None:
    """Test an import can be performed."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    # Convert Python object to JSON bytes in memory
    json_bytes = json.dumps(ALL_EXPORT_DATA).encode("utf-8")
    file_payload = {
        "import_data": (
            "import.json",
            io.BytesIO(json_bytes),
            "application/json",
        )
    }

    res = test_client.post(
        f"{settings.API_PREFIX}/store/import",
        files=file_payload,
        data={"force": True},
    )
    assert res.status_code == codes.OK


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_write_permissions(
        ResourceType.STORE,
    ),
)
def test_import_no_permissions(
    test_api_fixture, api_user: UserWithPassword
) -> None:
    """Test that import rejects no permissions."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    json_bytes = json.dumps(ALL_EXPORT_DATA).encode("utf-8")
    file_payload = {
        "import_data": (
            "import.json",
            io.BytesIO(json_bytes),
            "application/json",
        )
    }

    res = test_client.post(
        f"{settings.API_PREFIX}/store/import",
        files=file_payload,
        data={"force": True},
    )
    assert res.status_code == codes.FORBIDDEN


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_write_permissions(
        ResourceType.STORE,
    ),
)
def test_export(test_api_fixture, api_user: UserWithPassword) -> None:
    """Test an export can be performed."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    spec = {
        "models": "*",
        "custom_lists": "*",
        "users": "*",
        "catalogs": "*",
    }
    res = test_client.post(
        f"{settings.API_PREFIX}/store/export",
        json=spec,
    )

    assert res.status_code == codes.OK
    assert res.headers["content-type"] == "application/octet-stream"

    with zipfile.ZipFile(io.BytesIO(res.content)) as zip_file:
        filenames = zip_file.namelist()
        assert len(filenames) > 0


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_write_permissions(
        ResourceType.STORE,
    ),
)
def test_export_no_permissions(
    test_api_fixture, api_user: UserWithPassword
) -> None:
    """Test that export rejects no permissions."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    spec = {
        "models": "*",
        "custom_lists": "*",
        "users": "*",
        "catalogs": "*",
    }
    res = test_client.post(
        f"{settings.API_PREFIX}/store/export",
        json=spec,
    )

    assert res.status_code == codes.FORBIDDEN
