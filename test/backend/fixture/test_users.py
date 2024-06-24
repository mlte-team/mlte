"""
test/backend/fixture/api.py

Set up for store fixtures in API state.
"""

from __future__ import annotations

from typing import List, Optional

from mlte.store.user.policy import Policy
from mlte.user import passwords
from mlte.user.model import Group, ResourceType, RoleType, UserWithPassword

TEST_ADMIN_USERNAME = "admin_user"
TEST_API_USERNAME = "api_user"
TEST_API_PASS = "api_pass"
TEST_API_HASHED_PASS = passwords.hash_password(TEST_API_PASS)
"""User and passwords added to test the API."""


def build_admin_user() -> UserWithPassword:
    """The default admin user."""
    return build_test_user(username=TEST_ADMIN_USERNAME, role=RoleType.ADMIN)


def build_test_user(
    username: str = TEST_API_USERNAME,
    password: str = TEST_API_PASS,
    role: Optional[RoleType] = None,
    groups: Optional[List[Group]] = None,
) -> UserWithPassword:
    """Creaters a test user."""
    test_user = UserWithPassword(username=username, password=password)
    if role:
        test_user.role = role
    if groups:
        test_user.groups = groups
    return test_user


def get_test_users_with_read_permissions(
    resource_type: ResourceType, resource_id: Optional[str] = None
) -> List[UserWithPassword]:
    """Get a list of users that have permissions to read from different sources."""
    users = [
        build_test_user(role=RoleType.ADMIN),
        build_test_user(groups=Policy.build_groups(resource_type)),
        build_test_user(
            groups=Policy.build_groups(resource_type, build_write_group=False)
        ),
    ]

    # Add user with all permissions for this type/id, and one with only read permissions.
    if resource_id is not None:
        users.append(
            build_test_user(
                groups=Policy.build_groups(resource_type, resource_id)
            )
        )
        users.append(
            build_test_user(
                groups=Policy.build_groups(
                    resource_type, resource_id, build_write_group=False
                )
            )
        )

    return users


def get_test_users_with_write_permissions(
    resource_type: ResourceType, resource_id: Optional[str] = None
) -> List[UserWithPassword]:
    """Get a list of users that have permissions to write from different sources."""
    users = [
        build_test_user(role=RoleType.ADMIN),
        build_test_user(groups=Policy.build_groups(resource_type)),
        build_test_user(
            groups=Policy.build_groups(resource_type, build_read_group=False)
        ),
    ]

    if resource_id is not None:
        users.append(
            build_test_user(
                groups=Policy.build_groups(resource_type, resource_id)
            )
        )
        users.append(
            build_test_user(
                groups=Policy.build_groups(
                    resource_type, resource_id, build_read_group=False
                )
            )
        )

    return users


def get_test_users_with_no_read_permissions(
    resource_type: ResourceType, resource_id: Optional[str] = None
) -> List[UserWithPassword]:
    """Get a list of users that do not have permissions to read from different sources."""
    users = [
        build_test_user(),
        build_test_user(
            groups=Policy.build_groups(resource_type, build_read_group=False)
        ),
    ]

    # Add user with the opposite permission, and with appropriate ones but for wrong id.
    fake_id = "fake_id"
    if resource_id is not None:
        users.append(
            build_test_user(
                groups=Policy.build_groups(
                    resource_type, resource_id, build_read_group=False
                )
            )
        )
        users.append(
            build_test_user(
                groups=Policy.build_groups(resource_type, resource_id=fake_id)
            )
        )

    return users


def get_test_users_with_no_write_permissions(
    resource_type: ResourceType, resource_id: Optional[str] = None
) -> List[UserWithPassword]:
    """Get a list of users that do not have permissions to write from different sources."""
    users = [
        build_test_user(),
        build_test_user(
            groups=Policy.build_groups(resource_type, build_write_group=False)
        ),
    ]

    fake_id = "fake_id"
    if resource_id is not None:
        users.append(
            build_test_user(
                groups=Policy.build_groups(
                    resource_type, resource_id, build_write_group=False
                )
            )
        )
        users.append(
            build_test_user(
                groups=Policy.build_groups(resource_type, resource_id=fake_id)
            )
        )

    return users
