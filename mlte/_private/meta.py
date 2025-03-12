"""
Metaclasses helpers.
"""

from typing import Any, Callable, Union


def has_callable(type: type, name: str) -> bool:
    """Determine if `type` has a callable attribute with the given name."""
    return hasattr(type, name) and callable(getattr(type, name))


def has_callables(type: type, *names: str) -> bool:
    """ "Determine if `type` has callables with the given names."""
    return all(has_callable(type, name) for name in names)


def get_qualified_name(entity: Union[type, Callable[[], Any]]) -> str:
    """
    Returns the full path to the given class or function, including module.

    :param cls: It has to be a class type or a function.
    """
    return f"{entity.__module__}.{entity.__qualname__}"
