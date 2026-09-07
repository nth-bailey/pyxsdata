import json
from pathlib import Path
from typing import Any


def dump(obj: Any) -> None:
    """Write any object into a dump JSON file.

    For internal troubleshooting purposes only!!!
    """
    with Path.cwd().joinpath("xsdata_dump.json").open("w+") as f:
        json.dump(convert(obj), f, indent=4)


def convert(obj: Any) -> Any:
    """Dump any obj into a readable dictionary."""
    if obj is None:
        return obj

    if isinstance(obj, (list, tuple)):
        return list(map(convert, obj))

    if isinstance(obj, dict):
        return {convert(key): convert(value) for key, value in obj.items()}

    if hasattr(obj, "__slots__") and obj.__slots__:
        return {name: convert(getattr(obj, name)) for name in obj.__slots__}

    if isinstance(obj, type):
        return f"{obj.__module__}.{obj.__qualname__}"

    if isinstance(obj, (str, int, bool, float)):
        return obj

    return repr(obj)
