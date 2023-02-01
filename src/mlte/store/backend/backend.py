"""
Backend storage interface.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional, Dict, Any

# -----------------------------------------------------------------------------
# BackendType
# -----------------------------------------------------------------------------


class BackendType(Enum):
    """Represents the type of backend store."""

    # Use the local filesystem as the backend store
    FS = 0


# -----------------------------------------------------------------------------
# BackendURI
# -----------------------------------------------------------------------------


class BackendURI:
    """Represents the URI for a backend store."""

    def __init__(self, uri: str, type: BackendType):
        """
        Initialize a BackendURI instance.
        :param uri: The URI
        :type uri: str
        :param type: The type of the backend store
        :type type: StoreType
        """
        self.uri = uri
        """The string that represents the URI."""

        self.type = type
        """The type identifier for the URI."""

    @staticmethod
    def from_string(uri: str) -> BackendURI:
        """
        Parse a BackendURI from a string.
        :param uri: The URI
        :type uri: str
        :return: The parsed BackendURI
        :rtype: BackendURI
        """
        if uri.startswith("fs://") or uri.startswith("local://"):
            return BackendURI(uri, BackendType.FS)
        raise RuntimeError(f"Unrecognized backend store URI: {uri}.")


# -----------------------------------------------------------------------------
# Backend
# -----------------------------------------------------------------------------


class Backend:
    """Represents an abstract backend store."""

    def __init__(self, uri: BackendURI):
        """
        Initialize a Backend instance.
        :param uri: The URI that indicates the backend of interest
        :type uri: BackendURI
        """
        self.uri = uri
        """The backend URI."""

    # -------------------------------------------------------------------------
    # Interface: Read Metadata
    # -------------------------------------------------------------------------

    def read_model_metadata(
        self, model_identifier: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Read all existing model identifiers.

        :param model_identifier: The (optional) identifier for the model of interest
        :type model_identifier: Optional[str]

        :return: {"models": [{ ... model document ...} ...]}
        :rtype: Dict[str, Any]
        """
        raise NotImplementedError("Cannot invoke method on abstract Backend.")

    # -------------------------------------------------------------------------
    # Interface: Read Results
    # -------------------------------------------------------------------------

    def read_result(
        self,
        model_identifier: str,
        model_version: str,
        result_identifier: str,
        result_version: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Read an individual result from the backend store.

        :param model_identifier: The identifier for the model of interest
        :type model_identifier: str
        :param model_version: The model version string
        :type model_version: str
        :param result_identifier: The identifier for the result of interest
        :type result_identifier: str
        :param result_version: The (optional) version for the result
        :type result_version: Optional[int]

        :return: {"results": [{ ...  result document ...}]}
        :rtype: Dict[str, Any]
        """
        raise NotImplementedError("Cannot invoke method on abstract Backend.")

    def read_results(
        self, model_identifier: str, model_version: str, tag: Optional[str]
    ) -> Dict[str, Any]:
        """
        Read a collection of results from the backend store.

        :param model_identifier: The identifier for the model of interest
        :type model_identifier: str
        :param model_version: The model version string
        :type model_version: str
        :param tag: The (optional) result tag to limit returned results
        :type tag: Optional[int]

        :return: {"results": [{ ... result document ... } ...]}
        :rtype: Dict[str, Any]
        """
        raise NotImplementedError("Cannot invoke method on abstract Backend.")

    # -------------------------------------------------------------------------
    # Interface: Write Results
    # -------------------------------------------------------------------------

    def write_result(
        self,
        model_identifier: str,
        model_version: str,
        result_identifier: str,
        result_data: Dict[str, Any],
        result_tag: Optional[str],
    ) -> Dict[str, Any]:
        """
        Write an individual result to the backend store.

        :param model_identifier: The identifier for the model of interest
        :type model_identifier: str
        :param model_version: The model version string
        :type model_version: str
        :param result_identifier: The identifier for the result
        :type result_identifier: str
        :param result_data: The result data
        :type result_data: Dict[str, Any]
        :param result_tag: An optional tag for the result
        :type result_tag: Optional[str]

        :return: {"written": <COUNT>}
        :rtype: Dict[str, Any]
        """
        raise NotImplementedError("Cannot invoke method on abstract Backend.")

    # -------------------------------------------------------------------------
    # Interface: Delete Results
    # -------------------------------------------------------------------------

    def delete_result_version(
        self,
        model_identifier: str,
        model_version: str,
        result_identifier: str,
        result_version: int,
    ) -> Dict[str, Any]:
        """
        Delete an individual result version.

        :param model_identifier: The identifier for the model of interest
        :type model_identifier: str
        :param model_version: The model version string
        :type model_version: str
        :param result_identifier: The identifier for the result of interest
        :type result_identifier: str
        :param result_version: The version for the result
        :type result_version: int

        :return: {"deleted": <COUNT>}
        :rtype: Dict[str, Any]
        """
        raise NotImplementedError("Cannot invoke method on abstract Backend.")

    def delete_result(
        self, model_identifier: str, model_version: str, result_identifier: str
    ) -> Dict[str, Any]:
        """
        Delete all versions for a result.

        :param model_identifier: The identifier for the model of interest
        :type model_identifier: str
        :param model_version: The model version string
        :type model_version: str
        :param result_identifier: The identifier for the result of interest
        :type result_identifier: str

        :return: {"deleted": <COUNT>}
        :rtype: Dict[str, Any]
        """
        raise NotImplementedError("Cannot invoke method on abstract Backend.")

    def delete_results(
        self,
        model_identifier: str,
        model_version: str,
        result_tag: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Delete a collection of results.

        :param model_identifier: The identifier for the model of interest
        :type model_identifier: str
        :param model_version: The model version string
        :type model_version: str
        :param result_tag: An (optional) tag to filter results that are deleted
        :type result_tag: Optional[str]

        :return: {"deleted": <COUNT>}
        :rtype: Dict[str, Any]
        """
        raise NotImplementedError("Cannot invoke method on abstract Backend.")

    # -------------------------------------------------------------------------
    # Interface: Binding
    # -------------------------------------------------------------------------

    def read_binding(
        self, model_identifier: str, model_version: str
    ) -> Dict[str, Any]:
        """
        Read a binding for the model context.

        :param model_identifier: The model identifier
        :type model_identifier: str
        :param model_version: The model version
        :type model_version: str

        :return: {"binding": { ... binding document ... }}
        :rtype: Dict[str, Any]
        """
        raise NotImplementedError("Cannot invoke method on abstract Backend.")

    def write_binding(
        self, model_identifier: str, model_version: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Write a binding for the model context.

        :param model_identifier: The model identifier
        :type model_identifier: str
        :param model_version: The model version
        :type model_version: str
        :param data: The binding data
        :type data: Dict[str, Any]

        :return: {"written": <COUNT>}
        :rtype: Dict[str, Any]
        """
        raise NotImplementedError("Cannot invoke method on abstract Backend.")

    # -------------------------------------------------------------------------
    # Interface: Spec
    # -------------------------------------------------------------------------

    def read_spec(
        self, model_identifier: str, model_version: str
    ) -> Dict[str, Any]:
        """
        Read a specification for the model context.

        :param model_identifier: The model identifier
        :type model_identifier: str
        :param model_version: The model version
        :type model_version: str

        :return: {"spec": { ... specification document ...}}
        :rtype: Dict[str, Any]
        """
        raise NotImplementedError("Cannot invoke method on abstract Backend.")

    def write_spec(
        self, model_identifier: str, model_version: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Write a specification for the model context.

        :param model_identifier: The model identifier
        :type model_identifier: str
        :param model_version: The model version
        :type model_version: str
        :param data: The specification data
        :type data: Dict[str, Any]

        :return: {"written": <COUNT>} on success
        :rtype: Dict[str, Any]
        """
        raise NotImplementedError("Cannot invoke method on abstract Backend.")

    # -------------------------------------------------------------------------
    # Interface: BoundSpec
    # -------------------------------------------------------------------------

    def read_boundspec(
        self, model_identifier: str, model_version: str
    ) -> Dict[str, Any]:
        """
        Read a bound specification for the model context.

        :param model_identifier: The model identifier
        :type model_identifier: str
        :param model_version: The model version
        :type model_version: str

        :return: {"boundspec": { ... bound specification document ... }}
        :rtype: Dict[str, Any]
        """
        raise NotImplementedError("Cannot invoke method on abstract Backend.")

    def write_boundspec(
        self, model_identifier: str, model_version: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Write a bound specification for the model context.

        :param model_identifier: The model identifier
        :type model_identifier: str
        :param model_version: The model version
        :type model_version: str
        :param data: The bound specification data
        :type data: Dict[str, Any]

        :return: {"written": <COUNT>}
        :rtype: Dict[str, Any]
        """
        raise NotImplementedError("Cannot invoke method on abstract Backend.")
