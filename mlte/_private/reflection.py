import ast
import importlib
import inspect
from typing import Any, Type

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


def get_lambda_code(lambda_expression: Any) -> str:
    """Returns the code for a given lambda expression as a string."""
    code_string = inspect.getsource(lambda_expression).lstrip()

    class LambdaGetter(ast.NodeTransformer):
        def __init__(self):
            super().__init__()
            self.lambda_sources = []

        def visit_Lambda(self, node):
            self.lambda_sources.append(astunparse.unparse(node).strip()[1:-1])

        def get(self, code_string):
            tree = ast.parse(code_string)
            self.visit(tree)
            return self.lambda_sources

    return str(LambdaGetter().get(code_string)[0])
