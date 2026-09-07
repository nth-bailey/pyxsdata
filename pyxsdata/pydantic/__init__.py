from typing import Any

from pyxsdata.pydantic.fields import field

__all__ = [
    "DictDecoder",
    "DictEncoder",
    "JsonParser",
    "JsonSerializer",
    "PycodeSerializer",
    "TreeParser",
    "UserXmlParser",
    "XmlContext",
    "XmlParser",
    "XmlSerializer",
    "field",
]


def __getattr__(name: str) -> Any:
    if name in __all__:
        import pyxsdata.pydantic.bindings as bindings

        return getattr(bindings, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
