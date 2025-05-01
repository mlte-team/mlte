import json

# The json-fix library is loaded to patch json.dumps so it automatically calls
#  a .__json__ method if defined in a class being serialized.
import json_fix  # type: ignore # noqa

# Exports json to be used.
__all__ = ["json"]
