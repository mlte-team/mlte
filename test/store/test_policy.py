"""Unit tests for the Policy class."""

import pytest

from mlte.context.model import Model
from mlte.store.artifact.store import ArtifactStore, ManagedArtifactSession
from mlte.store.user.policy import Policy, create_model_policies_if_needed
from mlte.store.user.store import UserStore
from mlte.store.user.store_session import ManagedUserSession
from mlte.user.model import BasicUser, MethodType, ResourceType
from test.store.artifact.fixture import artifact_stores
from test.store.artifact.fixture import fs_store as artifact_fs_store  # noqa
from test.store.artifact.fixture import (  # noqa
    http_store as artifact_http_store,
)
from test.store.artifact.fixture import (  # noqa
    memory_store as artifact_memory_store,
)
from test.store.artifact.fixture import (  # noqa
    rdbs_store as artifact_rdbs_store,
)
from test.store.user.fixture import fs_store as user_fs_store  # noqa
from test.store.user.fixture import memory_store as user_memory_store  # noqa
from test.store.user.fixture import rdbs_store as user_rdbs_store  # noqa
from test.store.user.fixture import user_stores


@pytest.mark.parametrize(
    "resource_type", [resource_type for resource_type in ResourceType]
)
@pytest.mark.parametrize("id", [None, "test_id"])
@pytest.mark.parametrize("read", [True, False])
@pytest.mark.parametrize("edit", [True, False])
@pytest.mark.parametrize("create", [True, False])
class TestPolicy:

    @staticmethod
    def test_creation(
        resource_type: ResourceType,
        id: str,
        read: bool,
        edit: bool,
        create: bool,
    ):
        """Tests that policies contain the expected groups and permissions."""
        policy = Policy(resource_type, id, read, edit, create)

        # Check all created permissions are for the given type and ids.
        found_permissions: dict[MethodType, bool] = {
            method_type: False for method_type in MethodType
        }
        for group in policy.groups:
            for permission in group.permissions:
                assert permission.resource_type == resource_type
                assert permission.resource_id == id
                found_permissions[permission.method] = True

        # Check that permissions were created depending on the booleans.
        if read:
            assert found_permissions[MethodType.GET]
        if edit:
            assert found_permissions[MethodType.PUT]
            assert found_permissions[MethodType.DELETE]
        if create and not id:
            assert found_permissions[MethodType.POST]

    @staticmethod
    @pytest.mark.parametrize("store_fixture_name", user_stores())
    def test_save_remove(
        resource_type: ResourceType,
        id: str,
        read: bool,
        edit: bool,
        create: bool,
        store_fixture_name: str,
        request: pytest.FixtureRequest,
    ):
        """Tests that policies can be properly saved and removed."""
        store: UserStore = request.getfixturevalue(f"user_{store_fixture_name}")
        policy = Policy(resource_type, id, read, edit, create)

        with ManagedUserSession(store.session()) as user_store:
            if not id and (create or read or edit):
                # Store is iniitialized with non-id policies with all permissions
                assert Policy.is_stored(policy, user_store)
            elif policy.groups:
                # Only need to save if current policy has any groups.
                assert not policy.is_stored(user_store)
                policy.save_to_store(user_store)

            assert policy.is_stored(user_store)

            # Only test remove if policy has any groups.
            if policy.groups:
                policy.remove_from_store(user_store)
                assert not policy.is_stored(user_store)

    @staticmethod
    def test_assign_to_user(
        resource_type: ResourceType,
        id: str,
        read: bool,
        edit: bool,
        create: bool,
    ):
        """Checks that a policy is properly applied to a user object."""
        policy = Policy(resource_type, id, read, edit, create)
        user = BasicUser(username="test")

        policy.assign_to_user(user)

        for group in policy.groups:
            assert group in user.groups


@pytest.mark.parametrize("art_store_fixture_name", artifact_stores())
@pytest.mark.parametrize("user_store_fixture_name", user_stores())
def test_create_policy_if_needed(
    art_store_fixture_name: str,
    user_store_fixture_name: str,
    request: pytest.FixtureRequest,
):
    """Checks that policies for models created outside of backend are properly updated."""
    model_id = "m1"
    policy = Policy(ResourceType.MODEL, resource_id=model_id)
    artifact_store: ArtifactStore = request.getfixturevalue(
        f"artifact_{art_store_fixture_name}"
    )
    user_store: UserStore = request.getfixturevalue(
        f"user_{user_store_fixture_name}"
    )

    with ManagedArtifactSession(
        artifact_store.session()
    ) as artifact_store_session:
        with ManagedUserSession(user_store.session()) as user_store_session:
            # Create a model which will not have permissions.
            artifact_store_session.create_model(Model(identifier=model_id))

            # Add policies.
            create_model_policies_if_needed(
                artifact_store_session, user_store_session
            )

            # Check policies now exist.
            policy.is_stored(user_store_session)

            # Check we can call create_model_policies again with no issues.
            create_model_policies_if_needed(
                artifact_store_session, user_store_session
            )
