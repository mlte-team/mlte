"""Unit tests for the Policy class."""

import pytest

from mlte.context.model import Model
from mlte.store.artifact.store import ArtifactStore
from mlte.store.artifact.store_session import ManagedArtifactSession
from mlte.store.user.policy import Policy
from mlte.store.user.policy.model_policy import create_model_policies_if_needed
from mlte.store.user.store import UserStore
from mlte.store.user.store_session import ManagedUserSession
from mlte.user.model import BasicUser, MethodType, ResourceType
from test.store.artifact.fixture import create_test_artifact_store  # noqa
from test.store.user.conftest import create_test_user_store  # noqa
from test.store.utils import store_types  # noqa


@pytest.mark.parametrize(
    "resource_type", [resource_type for resource_type in ResourceType]
)
@pytest.mark.parametrize("id", [None, "test-1"])
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
    @pytest.mark.parametrize("store_type", store_types())
    def test_save_remove(
        resource_type: ResourceType,
        id: str,
        read: bool,
        edit: bool,
        create: bool,
        store_type: str,
        request: pytest.FixtureRequest,
        create_test_user_store,  # noqa
    ):
        """Tests that policies can be properly saved and removed."""
        store: UserStore = create_test_user_store(store_type)
        policy = Policy(resource_type, id, read, edit, create)

        with ManagedUserSession(store.session()) as user_store:
            if not id and (create or read or edit):
                # Store is iniitialized with non-id policies with all permissions
                assert user_store.policy_store.is_stored(policy)
            elif policy.groups:
                # Only need to save if current policy has any groups.
                assert not user_store.policy_store.is_stored(policy)
                user_store.policy_store.save_to_store(policy)

            assert user_store.policy_store.is_stored(policy)

            # Only test remove if policy has any groups.
            if policy.groups:
                user_store.policy_store.remove_from_store(policy)
                assert not user_store.policy_store.is_stored(policy)

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


@pytest.mark.parametrize("store_type", store_types())
def test_create_policy_if_needed(
    store_type: str,
    create_test_artifact_store,  # noqa
    create_test_user_store,  # noqa
):
    """Checks that policies for models created outside of backend are properly updated."""
    model_id = "m1"
    policy = Policy(ResourceType.MODEL, resource_id=model_id)
    artifact_store: ArtifactStore = create_test_artifact_store(store_type)
    user_store: UserStore = create_test_user_store(store_type)

    with ManagedArtifactSession(
        artifact_store.session()
    ) as artifact_store_session:
        with ManagedUserSession(user_store.session()) as user_store_session:
            # Create a model which will not have permissions.
            artifact_store_session.model_mapper.create(
                Model(identifier=model_id)
            )

            # Add policies.
            create_model_policies_if_needed(
                artifact_store_session, user_store_session.policy_store
            )

            # Check policies now exist.
            assert user_store_session.policy_store.is_stored(policy)

            # Check we can call create_model_policies again with no issues.
            create_model_policies_if_needed(
                artifact_store_session, user_store_session.policy_store
            )
