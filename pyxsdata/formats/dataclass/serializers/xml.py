from dataclasses import dataclass, field
from io import StringIO, TextIOBase
from typing import Any

from pyxsdata.formats.dataclass.serializers.config import SerializerConfig
from pyxsdata.formats.dataclass.serializers.mixins import (
    EventGenerator,
    XmlWriter,
)
from pyxsdata.formats.dataclass.serializers.writers import DEFAULT_XML_WRITER
from pyxsdata.utils import namespaces

try:
    import polyxml
except ImportError:  # pragma: no cover
    polyxml = None  # type: ignore[assignment]


@dataclass
class CoreXmlSerializer:
    """Ultra-fast native XML serializer for data classes powered by PolyXML.

    Args:
        config: The serializer config instance
    """

    config: SerializerConfig = field(default_factory=SerializerConfig)

    def render(self, obj: Any, ns_map: dict | None = None) -> str:
        """Serialize the input model instance to xml string.

        Args:
            obj: The input model instance to serialize
            ns_map: Optional namespace prefix-URI map (not required by native engine)

        Returns:
            The serialized xml string output.
        """
        if polyxml is None:
            raise ImportError(
                "polyxml is required for CoreXmlSerializer. "
                "Install it via `pip install 'pyxsdata[core]'`."
            )
        indent = len(self.config.indent) if self.config.indent else None
        return polyxml.serialize(obj, indent=indent).decode("utf-8")

    def write(self, out: TextIOBase, obj: Any, ns_map: dict | None = None) -> None:
        """Serialize the given object to the output text stream.

        Args:
            out: The output text stream
            obj: The input model instance to serialize
            ns_map: Optional namespace prefix-URI map
        """
        out.write(self.render(obj, ns_map))


@dataclass
class XmlSerializer(EventGenerator):
    """Xml serializer for data classes.

    Args:
        config: The serializer config instance
        context: The models context instance
        writer: The xml writer class
    """

    writer: type[XmlWriter] = field(default=DEFAULT_XML_WRITER)

    def render(self, obj: Any, ns_map: dict | None = None) -> str:
        """Serialize the input model instance to xml string.

        Args:
            obj: The input model instance to serialize
            ns_map: A user defined namespace prefix-URI map

        Returns:
            The serialized xml string output.
        """
        output = StringIO()
        self.write(output, obj, ns_map)
        return output.getvalue()

    def write(self, out: TextIOBase, obj: Any, ns_map: dict | None = None) -> None:
        """Serialize the given object to the output text stream.

        Args:
            out: The output text stream
            obj: The input model instance to serialize
            ns_map: A user defined namespace prefix-URI map
        """
        events = self.generate(obj)
        handler = self.writer(
            config=self.config,
            output=out,
            ns_map=namespaces.clean_prefixes(ns_map) if ns_map else {},
        )
        handler.write(events)
