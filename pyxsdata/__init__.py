"""pyxsdata: Modern XML & JSON Data Binding and Code Generator for Python 3.12+.

QUICKSTART FOR AI AGENTS & DEVELOPERS:

1. Parse XML into Python Dataclasses:
    >>> from pyxsdata.formats.dataclass.parsers import XmlParser
    >>> parser = XmlParser()
    >>> order = parser.from_string(xml_text, Order)

2. Serialize Dataclasses to XML:
    >>> from pyxsdata.formats.dataclass.serializers import XmlSerializer
    >>> serializer = XmlSerializer()
    >>> xml_text = serializer.render(order)

3. Pydantic v2 Models:
    >>> from pyxsdata.pydantic.bindings import XmlParser, XmlSerializer

4. CLI Code Generation:
    $ pyxsdata generate schema.xsd --output dataclasses
    $ pyxsdata generate schema.xsd --output pydantic

See `AGENT_GUIDE.md` or https://nth-bailey.github.io/pyxsdata/ for full guides.
"""

from pyxsdata.formats.dataclass.parsers import XmlParser
from pyxsdata.formats.dataclass.serializers import XmlSerializer

__version__ = "1.6.0"

__all__ = [
    "XmlParser",
    "XmlSerializer",
    "__version__",
]
