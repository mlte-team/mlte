"""
test/user/test_model.py

Test the user and permission functions.
"""

import pytest

from mlte.user.model import MethodType, Permission, ResourceType


@pytest.mark.parametrize(
    "permission",
    [
        Permission(
            resource_type=ResourceType.MODEL,
            resource_id=None,
            method=MethodType.ANY,
        )
    ],
)
@pytest.mark.parametrize(
    "requested",
    [
        Permission(
            resource_type=ResourceType.MODEL,
            resource_id=None,
            method=MethodType.GET,
        ),
        Permission(
            resource_type=ResourceType.MODEL,
            resource_id="1",
            method=MethodType.POST,
        ),
        Permission(
            resource_type=ResourceType.MODEL,
            resource_id="2",
            method=MethodType.ANY,
        ),
    ],
)
def test_permission_granted_all(
    permission: Permission, requested: Permission
) -> None:
    """Checks that permissions are properly granted for non id-specific cases."""

    permission_granted = permission.grants_access(requested)

    assert permission_granted


@pytest.mark.parametrize(
    "permission",
    [
        Permission(
            resource_type=ResourceType.MODEL,
            resource_id=None,
            method=MethodType.ANY,
        ),
        Permission(
            resource_type=ResourceType.MODEL,
            resource_id="1",
            method=MethodType.GET,
        ),
    ],
)
@pytest.mark.parametrize(
    "requested",
    [
        Permission(
            resource_type=ResourceType.GROUP,
            resource_id=None,
            method=MethodType.GET,
        ),
        Permission(
            resource_type=ResourceType.USER,
            resource_id="1",
            method=MethodType.POST,
        ),
        Permission(
            resource_type=ResourceType.GROUP,
            resource_id="2",
            method=MethodType.ANY,
        ),
    ],
)
def test_permission_not_granted_diff_type(
    permission: Permission, requested: Permission
) -> None:
    """Checks that permissions are not granted for requests with different resource types."""

    permission_granted = permission.grants_access(requested)

    assert not permission_granted


@pytest.mark.parametrize(
    "permission",
    [
        Permission(
            resource_type=ResourceType.MODEL,
            resource_id="3",
            method=MethodType.ANY,
        ),
    ],
)
@pytest.mark.parametrize(
    "requested",
    [
        Permission(
            resource_type=ResourceType.MODEL,
            resource_id=None,
            method=MethodType.GET,
        ),
        Permission(
            resource_type=ResourceType.MODEL,
            resource_id="1",
            method=MethodType.POST,
        ),
        Permission(
            resource_type=ResourceType.MODEL,
            resource_id="2",
            method=MethodType.ANY,
        ),
    ],
)
def test_permission_not_granted_id_vs_all(
    permission: Permission, requested: Permission
) -> None:
    """Checks that permissions are not granted for requests with different resource types."""

    permission_granted = permission.grants_access(requested)

    assert not permission_granted


@pytest.mark.parametrize(
    "permission",
    [
        Permission(
            resource_type=ResourceType.MODEL,
            resource_id="3",
            method=MethodType.ANY,
        ),
    ],
)
@pytest.mark.parametrize(
    "requested",
    [
        Permission(
            resource_type=ResourceType.MODEL,
            resource_id="3",
            method=MethodType.ANY,
        ),
        Permission(
            resource_type=ResourceType.MODEL,
            resource_id="3",
            method=MethodType.POST,
        ),
        Permission(
            resource_type=ResourceType.MODEL,
            resource_id="3",
            method=MethodType.GET,
        ),
    ],
)
def test_permission_granted_id_any(
    permission: Permission, requested: Permission
) -> None:
    """Checks that permissions are granted for any method type."""

    permission_granted = permission.grants_access(requested)

    assert permission_granted


@pytest.mark.parametrize(
    "permission",
    [
        Permission(
            resource_type=ResourceType.MODEL,
            resource_id="3",
            method=MethodType.ANY,
        ),
    ],
)
@pytest.mark.parametrize(
    "requested",
    [
        Permission(
            resource_type=ResourceType.MODEL,
            resource_id="3",
            method=MethodType.ANY,
        ),
        Permission(
            resource_type=ResourceType.MODEL,
            resource_id="3",
            method=MethodType.POST,
        ),
        Permission(
            resource_type=ResourceType.MODEL,
            resource_id="3",
            method=MethodType.GET,
        ),
    ],
)
def test_permission_granted_id_method(
    permission: Permission, requested: Permission
) -> None:
    """Checks that permissions are granted for same id but figgerent methods"""

    permission_granted = permission.grants_access(requested)

    assert permission_granted
