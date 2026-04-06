"""Define user policies."""

from typing import Union

from mlte.store.user.policy import Policy
from mlte.store.user.policy.policy_store import PolicyStoreService
from mlte.store.user.store_session import UserStoreSession
from mlte.user.model import BasicUser, ResourceType, RoleType, UserWithPassword


def set_default_user_policies(
    user: UserWithPassword, policy_store: PolicyStoreService
) -> UserWithPassword:
    """Assign a new user the permissions given to all users."""
    # Users with admin role don't need these policies.
    if user.role == RoleType.ADMIN:
        return user

    # Give every new user permissions to create (only) new models.
    model_create_policy = Policy(
        ResourceType.MODEL,
        resource_id=None,
        create_group=True,
        edit_group=False,
        read_group=False,
    )
    model_create_policy.assign_to_user(user)

    # Give every new user permissions to modify all custom lists.
    custom_list_policy = Policy(ResourceType.CUSTOM_LIST, resource_id=None)
    custom_list_policy.assign_to_user(user)

    # Give user permissions to modify its data.
    own_user_policy = Policy(ResourceType.USER, resource_id=user.username)
    policy_store.save_to_store(own_user_policy)
    own_user_policy.assign_to_user(user)

    return user


def remove_new_groups(
    user: Union[UserWithPassword, BasicUser], user_store: UserStoreSession
) -> Union[UserWithPassword, BasicUser]:
    """Removes any groups in the given user that are not in the stored version of this user."""
    current_groups = user_store.user_mapper.read(user.username).groups
    user.groups = current_groups
    return user


def delete_default_user_policies(
    username: str, policy_store: PolicyStoreService
) -> None:
    # Now delete related permissions and groups.
    policy = Policy(ResourceType.USER, resource_id=username)
    policy_store.remove_from_store(policy)
