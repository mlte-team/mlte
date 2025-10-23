import json

original_dump = json.dump

# The json-fix library is loaded to patch json.dumps so it automatically calls
#  a .__json__ method if defined in a class being serialized.
import json_fix  # type: ignore # noqa

# Patch to use fix from json_fix library that has not been pushed to PyPi yet.
if not hasattr(json.JSONEncoder, "patched"):
    json.dump = lambda obj, *args, **kwargs: original_dump(
        (
            json_fix.object_to_jsonable(obj)
            if isinstance(obj, json_fix.builtin_jsonable)
            else obj
        ),
        *args,
        **dict({"cls": json_fix.PatchedJsonEncoder}, **kwargs),
    )
    json.JSONEncoder.patched = True  # type: ignore # noqa

# Exports json to be used.
__all__ = ["json"]
