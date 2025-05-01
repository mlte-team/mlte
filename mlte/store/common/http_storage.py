"""
Base class for HTTP based stores.
"""

from __future__ import annotations

from typing import Any, Optional, OrderedDict
from urllib import parse as url_parse

from mlte._private import url as url_utils
from mlte.backend.core.config import settings
from mlte.store.base import StoreURI
from mlte.store.common.http_clients import OAuthHttpClient, RequestsClient
from mlte.store.common.storage import Storage
from mlte.user.model import MethodType, ResourceType

API_PREFIX = settings.API_PREFIX
"""API URL prefix."""


class HttpStorage(Storage):
    """An HTTP base storage for a given resource type."""

    def __init__(
        self,
        uri: StoreURI,
        resource_type: ResourceType,
        client: Optional[OAuthHttpClient] = None,
    ) -> None:
        super().__init__(uri)

        if client is None:
            client = RequestsClient()
        self.client = client
        """The client for requests."""

        # Get credentials, if any, from the uri and into the client.
        uri.uri = self.client.process_credentials(uri.uri)
        self.clean_url = uri.uri
        """Store the clean URL without credentials."""

        self.resource_url = self.build_resource_url(resource_type.value)
        """Set the base URL for all calls to this resource."""

    def build_resource_url(self, resource: str) -> str:
        return f"{self.clean_url}{API_PREFIX}/{resource}"

    def start_session(self):
        """Perform authentication."""
        self.client.authenticate(f"{self.clean_url}{API_PREFIX}")

    def post(
        self, json: Any, groups: OrderedDict[str, str] = OrderedDict()
    ) -> Any:
        """Post method, to create resource."""
        return self.send_command(MethodType.POST, json=json, groups=groups)

    def put(
        self, json: Any, groups: OrderedDict[str, str] = OrderedDict()
    ) -> Any:
        """Put method, to update resource."""
        return self.send_command(MethodType.PUT, json=json, groups=groups)

    def get(
        self,
        id: Optional[str] = None,
        groups: OrderedDict[str, str] = OrderedDict(),
        query_args: dict[str, str] = {},
    ) -> Any:
        """Get method, to read resource."""
        return self.send_command(
            MethodType.GET, id=id, groups=groups, query_args=query_args
        )

    def delete(
        self, id: str, groups: OrderedDict[str, str] = OrderedDict()
    ) -> Any:
        """Delete method, to remove resource."""
        return self.send_command(MethodType.DELETE, id=id, groups=groups)

    def send_command(
        self,
        method: MethodType,
        groups: OrderedDict[str, str] = OrderedDict(),
        id: Optional[str] = None,
        query_args: dict[str, str] = {},
        json: Optional[Any] = None,
        resource_type: Optional[str] = None,
    ) -> Any:
        """
        Sends an HTTP command request to the backend API, and returns a JSON response from it. Commonly not used directly, as it is expected
        for callers to use the post(), put(), read() and delete() method, but can be used when a non-standard command, which does not properly
        match the arguments of the previous 4 methods, needs to be sent.

        :param method: what HTTP method to use, from MethodType
        :param groups: a dict of groups to prepend to the request path, where the key is the id of the given group, and the value is the string used to denote
        the beginning of the next nested level (e.g., {"model1": "version"}, with model1 being a model id, and "version" being the keyword for the next level).
        :param id: the id of a given resource.
        :param query_args: dictionary of query args to append.
        :param json: json payload to send, only for POST and PUT commands.
        :param resource_type: optional param to overwride the default resource type set up when creating this storage;
        string to be used as the first item in the URL's path.
        """
        path_url = ""

        # Add groups to path.
        for group_id, subgroup_name in groups.items():
            path_url += f"/{url_utils.make_valid_url_part(group_id)}/{url_utils.make_valid_url_part(subgroup_name)}"

        # Add id to path, if any.
        if id:
            path_url += f"/{url_utils.make_valid_url_part(id)}"

        # Add query args.
        query = ""
        link_char = "?"
        for arg_name, arg_value in query_args.items():
            query += f"{link_char}{url_utils.make_valid_url_part(arg_name)}={url_utils.make_valid_url_part(arg_value)}"
            link_char = "&"

        # Allow changing the resource part of the base resource URL, if needed.
        base_url = self.resource_url
        if resource_type:
            base_url = self.build_resource_url(resource_type)

        url = f"{base_url}{url_parse.quote(path_url)}{query}"
        if method == MethodType.POST:
            res = self.client.post(url, json=json)
        elif method == MethodType.PUT:
            res = self.client.put(url, json=json)
        elif method == MethodType.GET:
            res = self.client.get(url)
        elif method == MethodType.DELETE:
            res = self.client.delete(url)
        else:
            raise RuntimeError(f"Invalid method type: {method}")

        self.client.raise_for_response(res)
        return res.json()
