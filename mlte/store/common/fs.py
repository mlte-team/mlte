"""
mlte/store/common/fs.py

Common functions for file-based stores.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Dict, List

from mlte.store.base import StoreURI, StoreURIPrefix


def parse_root_path(uristr: str) -> Path:
    """
    Parse the root path for the backend from the URI.
    :param uristr: The URI
    :return: The parsed path
    """
    assert uristr.startswith(
        tuple(StoreURIPrefix.LOCAL_FILESYSTEM)
    ), "Not a valid file system URI."

    # Remove any of the possible FS prefixes, and return a clean Path.
    path = uristr
    for prefix in tuple(StoreURIPrefix.LOCAL_FILESYSTEM):
        path = path.replace(prefix, "")
    return Path(path)


class JsonFileStorage:
    """A simple JSON storage wrapper for a file system store."""

    JSON_EXT = ".json"

    def create_folder(self, path: Path) -> None:
        Path.mkdir(path, parents=True)

    def list_folders(self, path: Path) -> List[Path]:
        return [x for x in sorted(path.iterdir()) if x.is_dir()]

    def delete_folder(self, path: Path) -> None:
        shutil.rmtree(path)

    def list_json_files(self, path: Path) -> List[Path]:
        return [
            x
            for x in sorted(path.iterdir())
            if x.is_file() and x.suffix == self.JSON_EXT
        ]

    def read_json_file(self, path: Path) -> Dict[str, Any]:
        with path.open("r") as f:
            data: Dict[str, Any] = json.load(f)
        return data

    def write_json_to_file(self, path: Path, data: Dict[str, Any]) -> None:
        with path.open("w") as f:
            json.dump(data, f, indent=4)

    def delete_file(self, path: Path) -> None:
        if not path.exists():
            raise RuntimeError(f"Path {path} does not exist.")
        path.unlink()

    def add_extension(self, filename: str) -> Path:
        return Path(filename + self.JSON_EXT)

    def get_just_filename(self, path: Path) -> str:
        return path.stem


class FileSystemStorage(JsonFileStorage):
    """A local file system implementation of a storage."""

    def __init__(self, uri: StoreURI, sub_folder: str) -> None:
        root = parse_root_path(uri.uri)
        if not root.exists():
            raise FileNotFoundError(
                f"Root data storage location does not exist: {root}."
            )

        self.base_path = Path(root, sub_folder)
        """The the base folder for the file store."""

        try:
            self.create_folder(self.base_path)
        except FileExistsError:
            # If it already existed, we just ignore warning.
            pass
