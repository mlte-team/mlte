import importlib
import typing


def load_class(class_path: str) -> typing.Type:
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
    except:
        raise RuntimeError(f"Module {module_name} not found")
    try:
        class_type = getattr(loaded_module, class_name)
    except:
        raise RuntimeError(
            f"Class {class_name} in module {module_name} not found"
        )

    return class_type
