from pyxsdata.formats.dataclass.parsers.handlers.native import XmlEventHandler
from pyxsdata.formats.dataclass.parsers.mixins import XmlHandler

try:
    from pyxsdata.formats.dataclass.parsers.handlers.lxml import LxmlEventHandler

    def default_handler() -> type[XmlHandler]:
        """Return the default xml handler."""
        return LxmlEventHandler

except ImportError:  # pragma: no cover

    def default_handler() -> type[XmlHandler]:
        """Return the default xml handler."""
        return XmlEventHandler


__all__ = [
    "LxmlEventHandler",
    "XmlEventHandler",
    "default_handler",
]
