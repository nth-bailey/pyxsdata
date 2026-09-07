import io
import pathlib
from typing import Any
from xml.etree import ElementTree as etree

import pyxsdata_core

from pyxsdata.exceptions import ParserError
from pyxsdata.formats.dataclass.parsers.mixins import XmlHandler


class CoreEventHandler(XmlHandler):
    """An ultra-fast native Rust XML deserialization handler powered by pyxsdata-core."""

    def parse(self, source: Any, ns_map: dict[str | None, str]) -> Any:
        """Parse the source XML document using pyxsdata-core.

        Args:
            source: The xml source, can be a file resource, path, input stream,
                bytes, XML string, or tree/element.
            ns_map: A namespace prefix-URI recorder map.

        Returns:
            An instance of the class type representing the parsed content.

        Raises:
            ParserError: If an XML syntax error or parse failure occurs.
        """
        if hasattr(source, "getroot") and callable(source.getroot):
            source = source.getroot()

        if hasattr(source, "tag") and not isinstance(source, (str, bytes)):
            raw_bytes = etree.tostring(source)
        elif isinstance(source, bytes):
            raw_bytes = source
        elif isinstance(source, str):
            if source.lstrip().startswith("<"):
                raw_bytes = source.encode("utf-8")
            else:
                raw_bytes = pathlib.Path(source).read_bytes()
        elif isinstance(source, pathlib.Path):
            raw_bytes = source.read_bytes()
        elif hasattr(source, "read"):
            data = source.read()
            raw_bytes = data.encode("utf-8") if isinstance(data, str) else data
        else:
            raise ParserError(f"Unsupported source type: {type(source)}")

        clazz = self.clazz
        if clazz is None and hasattr(self.parser, "context"):
            try:
                iterator = etree.iterparse(io.BytesIO(raw_bytes), events=("start",))
                _, elem = next(iter(iterator))
                clazz = self.parser.context.find_type(elem.tag)  # ty: ignore[unresolved-attribute]
            except Exception:
                pass
        if clazz is None:
            target = self.clazz.__name__ if self.clazz else ""
            raise ParserError(f"Failed to create target class `{target}`")

        try:
            return pyxsdata_core.deserialize(raw_bytes, clazz)
        except Exception as e:
            raise ParserError(e) from e
