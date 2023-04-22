"""
store/backend/backend.py

Generic backend storage interface.
"""

from __future__ import annotations

from typing import Optional, Dict, Any


from mlte.store.backend.backend_uri import BackendURI


# -----------------------------------------------------------------------------
# SessionHandle
# -----------------------------------------------------------------------------


class SessionHandle:
    """Represents an abstract handle on a backend session."""

    def __init__(self):
        """Initialize a SessionHandle instance."""
        pass

    def close(self) -> None:
        """
        Close a Backend instance.
        :return: `None`
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract SessionHandle."
        )

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
        result_tag: Optional[str] = None,
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


# -----------------------------------------------------------------------------
# BackendEngine
# -----------------------------------------------------------------------------


class BackendEngine:
    """
    Represents an abstract backend engine.

    The engine is the "static" part of a backend configuration.
    In contrast, a session handle represents an active session.
    """

    def __init__(self, *, uri: BackendURI):
        """
        Initialize a BackendEngine instance.
        :param uri: The parsed URI
        :type uri: BackendURI
        """
        self.uri = uri

    def handle(self) -> SessionHandle:
        """
        Return a handle to the underlying engine.
        :return: The session handle
        :rtype: SessionHandle
        """
        raise NotImplementedError(
            "Cannot get handle to abstract BackendEngine."
        )

    @staticmethod
    def create(uri: BackendURI) -> BackendEngine:
        """
        Create a new BackendEngine instance.
        :param uri: The backend URI
        :type uri: BackendURI
        :return: The backend engine
        :rtype: BackendEngine
        """
        raise NotImplementedError("Cannot create abstract BackendEngine.")
