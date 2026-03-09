"""Define user policies."""

from typing import Union

from mlte.store.user.policy import Policy
from mlte.store.user.store_session import UserStoreSession
from mlte.user.model import BasicUser, ResourceType, RoleType, UserWithPassword


def assing_default_user_policies(
    user: UserWithPassword, user_store: UserStoreSession
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
    own_user_policy.save_to_store(user_store)
    own_user_policy.assign_to_user(user)

    return user


def ignore_new_groups(
    user: Union[UserWithPassword, BasicUser], user_store: UserStoreSession
) -> Union[UserWithPassword, BasicUser]:
    """Ignore changes to user's groups."""
    # If not admin, keep current groups and ignore the new ones, if any.
    current_groups = user_store.user_mapper.read(user.username).groups
    user.groups = current_groups

    return user


def delete_default_user_policies(
    username: str, user_store: UserStoreSession
) -> None:
    # Now delete related permissions and groups.
    policy = Policy(ResourceType.USER, resource_id=username)
    policy.remove_from_store(user_store)
