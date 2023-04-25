import os


# TODO : Change me. No clue what this static prefix is
STATIC_PREFIX_ENV_VAR = "_MLFLOW_STATIC_PREFIX"

def _add_static_prefix(route):
    prefix = os.environ.get(STATIC_PREFIX_ENV_VAR)
    if prefix:
        return prefix + route
    return route