"""
Common functions for file-based stores.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any, Optional

import mlte.store.error as errors
from mlte._private import file
from mlte._private.fixed_json import json
from mlte.store.base import StoreType, StoreURI
from mlte.store.common.storage import Storage


def parse_root_path(uri: StoreURI) -> Path:
    """
    Parse the root path for the backend from the URI.
    :param uri: The URI
    :return: The parsed path
    """
    if uri.type != StoreType.LOCAL_FILESYSTEM:
        raise RuntimeError(f"Not a valid file system URI: {uri.uri}")

    return Path(uri.path)


class JsonFileFS:
    """A simple wrapper for common functions dealing with JSON files and folders."""

    JSON_EXT = ".json"

    @staticmethod
    def create_folder(path: Path) -> None:
        Path.mkdir(path, parents=True)

    @staticmethod
    def list_folders(path: Path) -> list[Path]:
        return [x for x in sorted(path.iterdir()) if x.is_dir()]

    @staticmethod
    def delete_folder(path: Path) -> None:
        shutil.rmtree(path)

    @staticmethod
    def list_json_files(path: Path) -> list[Path]:
        return [
            x
            for x in sorted(path.iterdir())
            if x.is_file() and x.suffix == JsonFileFS.JSON_EXT
        ]

    @staticmethod
    def read_json_file(path: Path) -> dict[str, Any]:
        with path.open("r") as f:
            data: dict[str, Any] = json.load(f)
        return data

    @staticmethod
    def write_json_to_file(path: Path, data: dict[str, Any]) -> None:
        with path.open("w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def delete_file(path: Path) -> None:
        if not path.exists():
            raise RuntimeError(f"Path {path} does not exist.")
        path.unlink()

    @staticmethod
    def add_extension(filename: str) -> Path:
        return Path(filename + JsonFileFS.JSON_EXT)

    @staticmethod
    def get_just_filename(path: Path) -> str:
        return path.stem

    @staticmethod
    def get_last_folder(path: Path) -> str:
        return path.resolve().name


class FileSystemStorage(Storage):
    """A local file system implementation of a storage."""

    def __init__(self, uri: StoreURI, sub_folder: str) -> None:
        super().__init__(uri)

        self.root = parse_root_path(uri)
        """Root folder, that exists, where the storage will be located."""

        if not self.root.exists():
            raise FileNotFoundError(
                f"Root data storage location does not exist: {self.root}."
            )

        self.sub_folder = sub_folder
        """The specific folder for this storage."""

        self.setup_base_path(Path(sub_folder))

    def setup_base_path(self, sub_folder: Path):
        """Sets a base path for this storage based on the root and the given Path."""

        self.base_path = Path(self.root, sub_folder)
        """The the base folder for the file store."""

        try:
            JsonFileFS.create_folder(self.base_path)
        except FileExistsError:
            # If it already existed, we just ignore warning.
            pass

    def clone(self) -> FileSystemStorage:
        clone = FileSystemStorage(self.uri, self.sub_folder)
        return clone

    # -------------------------------------------------------------------------
    # Resource methods.
    # -------------------------------------------------------------------------

    def list_resources(self, base_path: Optional[Path] = None) -> list[str]:
        """Returns a list of resource ids in this storage."""
        base_path = self.base_path if not base_path else base_path
        return [
            self._resource_id(resource_path)
            for resource_path in JsonFileFS.list_json_files(base_path)
        ]

    def read_resource(
        self, resource_id: str, base_path: Optional[Path] = None
    ) -> dict[str, Any]:
        """Reads the given resource as a dict."""
        return JsonFileFS.read_json_file(
            self._resource_path(resource_id, base_path)
        )

    def write_resource(
        self,
        resource_id: str,
        resource_data: dict[str, Any],
        base_path: Optional[Path] = None,
    ) -> None:
        """Writes the given resource to storage."""
        JsonFileFS.write_json_to_file(
            self._resource_path(resource_id, base_path), resource_data
        )

    def delete_resource(
        self, resource_id: str, base_path: Optional[Path] = None
    ) -> None:
        """Deletes the file for the associated resource id."""
        JsonFileFS.delete_file(self._resource_path(resource_id, base_path))

    def ensure_resource_does_not_exist(
        self, resource_id: str, base_path: Optional[Path] = None
    ) -> None:
        """Throws an ErrorAlreadyExists if the given resource does exist."""
        if self._resource_path(resource_id, base_path).exists():
            raise errors.ErrorAlreadyExists(
                f"Resource already exists: {resource_id}"
            )

    def ensure_resource_exists(
        self, resource_id: str, base_path: Optional[Path] = None
    ) -> None:
        """Throws an ErrorNotFound if the given resource does not exist."""
        if not self._resource_path(resource_id, base_path).exists():
            raise errors.ErrorNotFound(f"Resource not found: {resource_id}")

    # -------------------------------------------------------------------------
    # Resource group methods.
    # -------------------------------------------------------------------------

    def create_resource_group(
        self, group_id: str, base_path: Optional[Path] = None
    ) -> None:
        """Creates a resource group (folder)"""
        path = self._resource_group_path(group_id, base_path)
        JsonFileFS.create_folder(path)

    def list_resource_groups(
        self, base_path: Optional[Path] = None
    ) -> list[str]:
        """List the resource groups in a given path, or on the default one."""
        base_path = self.base_path if not base_path else base_path
        return [
            self._resource_group_id(model_path.relative_to(base_path))
            for model_path in JsonFileFS.list_folders(base_path)
        ]

    def exists_resource_group(
        self, group_id: str, base_path: Optional[Path] = None
    ) -> bool:
        """Checks if the given resource group exists."""
        return self._resource_group_path(group_id, base_path).exists()

    def delete_resource_group(
        self, group_id: str, base_path: Optional[Path] = None
    ) -> None:
        """Removes the given resource group."""
        JsonFileFS.delete_folder(self._resource_group_path(group_id, base_path))

    # -------------------------------------------------------------------------
    # Internal helpers.
    # -------------------------------------------------------------------------

    def _resource_path(
        self, resource_id: str, base_path: Optional[Path] = None
    ) -> Path:
        """
        Gets the full filepath for a stored resource.
        :param resource_id: The resource identifier
        :return: The formatted path
        """
        filename = file.make_valid_filename(resource_id)
        base_path = base_path if base_path else self.base_path
        return Path(base_path, JsonFileFS.add_extension(filename))

    def _resource_id(self, resource_path: Path) -> str:
        """
        Gets the name of a resource given a full filepath.
        :param resource_path: The full path
        :return: The resource id
        """
        resource_id = file.revert_valid_filename(
            JsonFileFS.get_just_filename(resource_path)
        )
        return resource_id

    def _resource_group_path(
        self, group_id: str, base_path: Optional[Path] = None
    ) -> Path:
        """
        Gets the full path for a stored resource group (which will be translated into a folder).
        :param group_id: The identifier of the resource group.
        :return: The formatted path
        """
        folder_name = file.make_valid_filename(group_id)
        base_path = base_path if base_path else self.base_path
        return Path(base_path, folder_name)

    def _resource_group_id(self, group_path: Path) -> str:
        """
        Gets the name of a resource group given a full filepath.
        :param group_path: The full path
        :return: The resource group id
        """
        folder_name = JsonFileFS.get_last_folder(group_path)
        group_id = file.revert_valid_filename(folder_name)
        return group_id
