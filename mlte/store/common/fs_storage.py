"""
mlte/store/common/fs.py

Common functions for file-based stores.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Dict, List

import mlte.store.error as errors
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


class JsonFileStorage:
    """A simple JSON storage wrapper for a file system store."""

    JSON_EXT = ".json"

    @staticmethod
    def create_folder(path: Path) -> None:
        Path.mkdir(path, parents=True)

    @staticmethod
    def list_folders(path: Path) -> List[Path]:
        return [x for x in sorted(path.iterdir()) if x.is_dir()]

    @staticmethod
    def delete_folder(path: Path) -> None:
        shutil.rmtree(path)

    @staticmethod
    def list_json_files(path: Path) -> List[Path]:
        return [
            x
            for x in sorted(path.iterdir())
            if x.is_file() and x.suffix == JsonFileStorage.JSON_EXT
        ]

    @staticmethod
    def read_json_file(path: Path) -> Dict[str, Any]:
        with path.open("r") as f:
            data: Dict[str, Any] = json.load(f)
        return data

    @staticmethod
    def write_json_to_file(path: Path, data: Dict[str, Any]) -> None:
        with path.open("w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def delete_file(path: Path) -> None:
        if not path.exists():
            raise RuntimeError(f"Path {path} does not exist.")
        path.unlink()

    @staticmethod
    def add_extension(filename: str) -> Path:
        return Path(filename + JsonFileStorage.JSON_EXT)

    @staticmethod
    def get_just_filename(path: Path) -> str:
        return path.stem


class FileSystemStorage(Storage, JsonFileStorage):
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

        self.set_base_path(Path(sub_folder))

    def set_base_path(self, sub_folder: Path):
        """Sets a base path for this storage based on the root and the given Path"""

        self.base_path = Path(self.root, sub_folder)
        """The the base folder for the file store."""

        try:
            JsonFileStorage.create_folder(self.base_path)
        except FileExistsError:
            # If it already existed, we just ignore warning.
            pass

    def clone(self) -> FileSystemStorage:
        clone = FileSystemStorage(self.uri, self.sub_folder)
        return clone

    # -------------------------------------------------------------------------
    # Resource methods.
    # -------------------------------------------------------------------------

    def list_resources(self) -> List[str]:
        """Returns a list of resource ids in this storage."""
        return [
            self._resource_id(resource_path)
            for resource_path in JsonFileStorage.list_json_files(self.base_path)
        ]

    def read_resource(self, resource_id: str) -> Dict[str, Any]:
        """Reads the given resource as a dict."""
        return JsonFileStorage.read_json_file(self._resource_path(resource_id))

    def write_resource(
        self, resource_id: str, resource_data: Dict[str, Any]
    ) -> None:
        """Writes the given resource to storage."""
        JsonFileStorage.write_json_to_file(
            self._resource_path(resource_id), resource_data
        )

    def delete_resource(self, resource_id: str) -> None:
        """Deletes the file for the associated resource id."""
        JsonFileStorage.delete_file(self._resource_path(resource_id))

    def ensure_resource_does_not_exist(self, resource_id: str) -> None:
        """Throws an ErrorAlreadyExists if the given resource does exist."""
        if self._resource_path(resource_id).exists():
            raise errors.ErrorAlreadyExists(
                f"Resource already exists: {resource_id}"
            )

    def ensure_resource_exists(self, resource_id: str) -> None:
        """Throws an ErrorNotFound if the given resource does not exist."""
        if not self._resource_path(resource_id).exists():
            raise errors.ErrorNotFound(f"Resource not found: {resource_id}")

    # -------------------------------------------------------------------------
    # Internal helpers.
    # -------------------------------------------------------------------------

    def _resource_path(self, resource_id: str) -> Path:
        """
        Gets the full filepath for a stored resource.
        :param resource_id: The resource identifier
        :return: The formatted path
        """
        return Path(self.base_path, JsonFileStorage.add_extension(resource_id))

    def _resource_id(self, resource_path: Path) -> str:
        """
        Gets the name of a resource given a full filepath.
        :param resource_path: The full path
        :return: The resource id
        """
        return JsonFileStorage.get_just_filename(resource_path)
