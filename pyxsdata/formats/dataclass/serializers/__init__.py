from contextlib import suppress

from pyxsdata.formats.dataclass.serializers.code import PycodeSerializer
from pyxsdata.formats.dataclass.serializers.dict import (
    DictEncoder,
    DictFactory,
)
from pyxsdata.formats.dataclass.serializers.json import JsonSerializer
from pyxsdata.formats.dataclass.serializers.xml import (
    CoreXmlSerializer,
    XmlSerializer,
)

__all__ = [
    "CoreXmlSerializer",
    "DictEncoder",
    "DictFactory",
    "JsonSerializer",
    "PycodeSerializer",
    "XmlSerializer",
]

with suppress(ImportError):
    from pyxsdata.formats.dataclass.serializers.tree import (
        TreeSerializer,  # noqa: F401
    )

    __all__.append("TreeSerializer")
