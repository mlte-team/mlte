"""MLTE user store mappers interface."""

from __future__ import annotations

from typing import Any, List, Union

from mlte.store.base import ResourceMapper
from mlte.user.model import BasicUser, Group, Permission, User, UserWithPassword


class UserMapper(ResourceMapper):
    """An interface for mapping CRUD actions to store users."""

    def create(self, new_user: UserWithPassword, context: Any = None) -> User:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def edit(
        self,
        updated_user: Union[UserWithPassword, BasicUser],
        context: Any = None,
    ) -> User:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def read(self, user_id: str, context: Any = None) -> User:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def list(self, context: Any = None) -> List[str]:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def delete(self, user_id: str, context: Any = None) -> User:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)


class GroupMapper(ResourceMapper):
    """A interface for mapping CRUD actions to store groups."""

    def create(self, new_group: Group, context: Any = None) -> Group:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def edit(self, updated_group: Group, context: Any = None) -> Group:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def read(self, group_id: str, context: Any = None) -> Group:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def list(self, context: Any = None) -> List[str]:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def delete(self, group_id: str, context: Any = None) -> Group:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)


class PermissionMapper(ResourceMapper):
    """A interface for mapping CRUD actions to store permissions."""

    def create(
        self, new_permission: Permission, context: Any = None
    ) -> Permission:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def edit(
        self, updated_permission: Permission, context: Any = None
    ) -> Permission:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def read(self, permission: str, context: Any = None) -> Permission:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def list(self, context: Any = None) -> List[str]:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def delete(self, permission: str, context: Any = None) -> Permission:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)
