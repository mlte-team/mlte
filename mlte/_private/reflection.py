from __future__ import annotations

import importlib
import importlib.resources
import json
import os
from types import ModuleType
from typing import Any, Generator, Type


def load_class(class_path: str) -> Type[Any]:
    """
    Returns a class type of the given class name/path.
    :param class_path: A path to a class to use, including absolute package/module path and class name.
    """
    # Split into package/module and class name.
    parts = class_path.rsplit(".", 1)
    module_name = parts[0]
    class_name = parts[1]

    try:
        loaded_module = importlib.import_module(module_name)
    except Exception:
        raise RuntimeError(f"Module {module_name} not found")
    try:
        class_type: Type[Any] = getattr(loaded_module, class_name)
    except Exception:
        raise RuntimeError(
            f"Class {class_name} in module {module_name} not found"
        )

    return class_type


def get_json_resources(package: ModuleType) -> Generator[Any, None, None]:
    """Load set of json files represented as a module and return a generator of their data."""
    resources = importlib.resources.files(package)
    with importlib.resources.as_file(resources) as resources_path:
        with os.scandir(resources_path) as files:
            for file in files:
                if file.is_file() and file.name.endswith("json"):
                    with open(file.path) as open_file:
                        yield json.load(open_file)
