from __future__ import annotations

import ast
import importlib
import importlib.resources
import inspect
import json
import os
import re
from types import ModuleType
from typing import Any, Generator, Type

import astunparse


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


def get_lambda_code(lambda_func: Any, lambda_pos: int = 0):
    """
    Gets the source code of a lambda function as a string.

    :param lambda_func: The lambda function to inspect.
    :param lambda_pos: If there are multiple lambdas in the line, which one to get. Defaults to 0, first one.
    :returns: A string containing the source code of the lambda function,
        or None if the input is not a lambda function or if the source
        code cannot be retrieved.
    """

    # Get source code lines where lambda was defined.
    try:
        code_string = inspect.getsource(lambda_func).strip()
    except (TypeError, OSError) as e:
        print(f"Error getting source lines: {e}")
        return None

    # Create visitor that will parse the line and find the lambda.
    class LambdaGetter(ast.NodeTransformer):
        def __init__(self):
            super().__init__()
            self.lambda_sources: list[str] = []

        def visit_Lambda(self, node: Any):
            self.lambda_sources.append(astunparse.unparse(node).strip()[1:-1])

        def get(self, code_string: str):
            try:
                tree = ast.parse(code_string)
                self.visit(tree)
            except SyntaxError as e:
                print(f"Error parsing lambda: {e}")

                # If we got an syntax error due to the source code line where
                # the lambda was defined not being a fully parseable line,
                # get the lambda plus any code after it (better than nothing).
                # TODO: see if it's worth to find a smarter solution.
                match = re.search(r"\b(?:lambda)\b.*?:", code_string)
                if match:
                    lambda_start = match.start()
                    lambda_body = code_string[lambda_start:]
                    self.lambda_sources.append(lambda_body)

            return self.lambda_sources

    lambdas = LambdaGetter().get(code_string)

    if len(lambdas) >= 1:
        return lambdas[lambda_pos]
    else:
        return None
