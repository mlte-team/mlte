"""Define model policies."""

from typing import Union

from mlte.store.artifact.store_session import ArtifactStoreSession
from mlte.store.user.policy.policy import Policy
from mlte.store.user.policy.policy_store import PolicyStoreService
from mlte.user.model import BasicUser, ResourceType, UserWithPassword


def create_model_policies_if_needed(
    artifact_store: ArtifactStoreSession, policy_store: PolicyStoreService
):
    """
    Function that checks, for all models, if policies have not been created.
    This is for cases where the model may have been created without the API.
    """
    models = artifact_store.model_mapper.list()
    for model_id in models:
        policy = Policy(ResourceType.MODEL, model_id)
        if not policy_store.is_stored(policy):
            policy_store.save_to_store(policy)


def create_model_policy(
    model_id: str,
    current_user: Union[UserWithPassword, BasicUser],
    policy_store: PolicyStoreService,
) -> Union[UserWithPassword, BasicUser]:
    """Create a basic policy for a model for the user, and returns the updated user."""
    policy = Policy(ResourceType.MODEL, model_id)
    policy_store.save_to_store(policy)

    # Also make user have access to CRUD for this model, since they are its creator.
    user = policy.assign_to_user(current_user)

    return user


def remove_model_polcy(model_id: str, policy_store: PolicyStoreService):
    """Removes a basic policy for a model."""
    policy = Policy(ResourceType.MODEL, resource_id=model_id)
    policy_store.remove_from_store(policy)
