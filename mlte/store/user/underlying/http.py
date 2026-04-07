"""Implementation of HTTP user store"""

import typing
from typing import Any, List, Optional, Union

from mlte.store.base import ResourceMapper, StoreURI
from mlte.store.common.http_clients import OAuthHttpClient
from mlte.store.common.http_storage import HttpResourceStorage
from mlte.store.user.mappers import (
    GroupMapper,
    PermissionMapper,
    UserMapper,
)
from mlte.store.user.store import UserStore
from mlte.store.user.store_session import UserStoreSession
from mlte.user.model import (
    BasicUser,
    Group,
    Permission,
    ResourceType,
    User,
    UserWithPassword,
)

# -----------------------------------------------------------------------------
# HttpUserStore
# -----------------------------------------------------------------------------


class HttpUserStore(UserStore):
    """A http implementation of the MLTE user store."""

    def __init__(
        self, *, uri: StoreURI, client: Optional[OAuthHttpClient] = None
    ) -> None:
        self.user_storage = HttpResourceStorage(
            uri=uri, resource_type=ResourceType.USER, client=client
        )
        """HTTP user storage."""

        self.group_storage = HttpResourceStorage(
            uri=uri, resource_type=ResourceType.GROUP, client=client
        )
        """HTTP group storage."""

        self.permission_storage = HttpResourceStorage(
            uri=uri, resource_type="groups/permissions", client=client
        )
        """HTTP group storage."""

        # Adding default data is not done for remote stores, since remote ones already did it when they were started.
        super().__init__(uri=uri, add_default_data=False)

    def session(self) -> UserStoreSession:
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return HttpUserStoreSession(
            user_storage=self.user_storage,
            group_storage=self.group_storage,
            permission_storage=self.permission_storage,
        )


# -----------------------------------------------------------------------------
# HttpUserStoreSession
# -----------------------------------------------------------------------------


class HttpUserStoreSession(UserStoreSession):
    """An HTTP implementation of the MLTE user store session."""

    def __init__(
        self,
        *,
        user_storage: HttpResourceStorage,
        group_storage: HttpResourceStorage,
        permission_storage: HttpResourceStorage,
    ) -> None:
        self.user_storage = user_storage
        """HTTP user storage."""

        self.group_storage = group_storage
        """HTTP group storage."""

        self.user_mapper = HttpUserMapper(user_storage)
        """User mapper."""

        self.group_mapper = HttpGroupMapper(group_storage)
        """Group mapper."""

        self.permission_mapper = HttpPermissionMapper(permission_storage)
        """Group mapper."""

    def close(self):
        # No closing needed
        pass


# -----------------------------------------------------------------------------
# HttpUserMapper
# -----------------------------------------------------------------------------


class HttpUserMapper(UserMapper):
    """HTTP mapper for the user resource."""

    def __init__(self, storage: HttpResourceStorage) -> None:
        self.storage = storage
        """The HTTP storage access."""

    def create(self, new_user: UserWithPassword, context: Any = None) -> User:
        response = self.storage.post(json=new_user.to_json())
        return User(**response)

    def read(self, entry_name: str, context: Any = None) -> User:
        response = self.storage.get(id=entry_name)
        return User(**response)

    def list(self, context: Any = None) -> list[str]:
        response = self.storage.get()
        return typing.cast(list[str], response)

    def edit(
        self, user: Union[UserWithPassword, BasicUser], context: Any = None
    ) -> User:
        response = self.storage.put(json=user.to_json())
        return User(**response)

    def delete(self, user_name: str, context: Any = None) -> User:
        response = self.storage.delete(id=user_name)
        return User(**response)


# -----------------------------------------------------------------------------
# HttpGroupMapper
# -----------------------------------------------------------------------------


class HttpGroupMapper(GroupMapper):
    """HTTP mapper for the group resource."""

    def __init__(self, storage: HttpResourceStorage) -> None:
        self.storage = storage
        """The HTTP storage access."""

    def create(self, new_group: Group, context: Any = None) -> Group:
        response = self.storage.post(json=new_group.to_json())
        return Group(**response)

    def read(self, group_name: str, context: Any = None) -> Group:
        response = self.storage.get(id=group_name)
        return Group(**response)

    def list(self, context: Any = None) -> list[str]:
        response = self.storage.get()
        return typing.cast(list[str], response)

    def edit(self, group: Group, context: Any = None) -> Group:
        response = self.storage.put(json=group.to_json())
        return Group(**response)

    def delete(self, group_name: str, context: Any = None) -> Group:
        response = self.storage.delete(id=group_name)
        return Group(**response)


# -------------------------------------------------------------------------
# HttpPermissionMapper
# -------------------------------------------------------------------------


class HttpPermissionMapper(PermissionMapper):
    """HTTP mapper for the permission resource."""

    def __init__(self, storage: HttpResourceStorage) -> None:
        self.storage = storage
        """The HTTP storage access."""

    def list(self, context: Any = None) -> list[str]:
        response = self.storage.get()
        return typing.cast(list[str], response)

    def list_details(
        self,
        context: Any = None,
        limit: int = ResourceMapper.DEFAULT_LIST_LIMIT,
        offset: int = 0,
    ) -> List[Any]:
        """
        Read details of resources within limit and offset.
        :param context: Any additional context needed for this resource.
        :param limit: The limit on resources to read
        :param offset: The offset on resources to read
        :return: The read resources
        """
        response = self.storage.get("s/permissions/details")
        return [permission for permission in response][offset : offset + limit]

    def read(self, permission_str: str, context: Any = None) -> Permission:
        response = self.storage.get(id=f"s/permission/{permission_str}")
        return Permission(**response)
