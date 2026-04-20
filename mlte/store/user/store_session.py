"""MLTE user store session implementation."""

from __future__ import annotations

from typing import cast

from mlte.store.base import ManagedSession, StoreSession
from mlte.store.user.mappers import GroupMapper, PermissionMapper, UserMapper
from mlte.store.user.policy.policy_store_service import PolicyStoreService


class UserStoreSession(StoreSession):
    """The base class for all implementations of the MLTE user store session."""

    user_mapper: UserMapper
    """Mapper for the user resource."""

    group_mapper: GroupMapper
    """Mapper for the group resource."""

    permission_mapper: PermissionMapper
    """Mapper for the permission resource."""

    policy_store: PolicyStoreService
    """A PolicyStore abstraction to handling stored policies (groups+permissions)."""


class ManagedUserSession(ManagedSession):
    """A simple context manager for store sessions."""

    def __enter__(self) -> UserStoreSession:
        return cast(UserStoreSession, self.session)
