from pyxsdata.formats.dataclass.parsers.handlers.native import XmlEventHandler
from pyxsdata.formats.dataclass.parsers.mixins import XmlHandler

try:
    from pyxsdata.formats.dataclass.parsers.handlers.lxml import (
        LxmlEventHandler,
    )

    def default_handler() -> type[XmlHandler]:
        """Return the default xml handler."""
        return LxmlEventHandler

except ImportError:  # pragma: no cover

    def default_handler() -> type[XmlHandler]:
        """Return the default xml handler."""
        return XmlEventHandler


try:
    from pyxsdata.formats.dataclass.parsers.handlers.pugixml import (
        PugixmlEventHandler,
    )
except ImportError:  # pragma: no cover
    PugixmlEventHandler = None  # type: ignore[assignment,misc]

try:
    from pyxsdata.formats.dataclass.parsers.handlers.core import (
        CoreEventHandler,
    )
except ImportError:  # pragma: no cover
    CoreEventHandler = None  # type: ignore[assignment,misc]


__all__ = [
    "CoreEventHandler",
    "LxmlEventHandler",
    "PugixmlEventHandler",
    "XmlEventHandler",
    "default_handler",
]
