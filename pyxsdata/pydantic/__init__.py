from typing import Any

__all__ = [
    "CoreXmlParser",
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
    if name == "field":
        from pyxsdata.pydantic.fields import field

        return field
    if name in __all__:
        import pyxsdata.pydantic.bindings as bindings

        return getattr(bindings, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
