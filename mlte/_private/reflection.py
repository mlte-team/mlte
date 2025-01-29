import importlib
import inspect
from typing import Any, Type


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


def get_lambda_code(lambda_var: str, lambda_expression: Any) -> str:
    """Returns the code for a given lambda expression as a string."""
    code_string = inspect.getsource(lambda_expression).lstrip()
    start = code_string.find(f"{lambda_var}=") + len(f"{lambda_var}=")
    end = code_string.find(",", start)
    return code_string[start:end]
