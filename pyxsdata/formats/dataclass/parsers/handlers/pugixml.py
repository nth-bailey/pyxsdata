import functools
import io
import pathlib
from collections.abc import Iterable
from typing import Any
from xml.etree import ElementInclude as xinclude
from xml.etree import ElementTree as etree

import pygixml

from pyxsdata.exceptions import ParserError, XmlHandlerError
from pyxsdata.formats.dataclass.parsers.handlers.native import (
    get_base_url,
    xinclude_loader,
)
from pyxsdata.formats.dataclass.parsers.mixins import XmlHandler
from pyxsdata.models.enums import EventType

EVENTS = (EventType.START, EventType.END)


class PugixmlEventHandler(XmlHandler):
    """A pugixml event handler powered by pygixml streaming parser."""

    def parse(self, source: Any, ns_map: dict[str | None, str]) -> Any:
        """Parse the source XML document.

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
            source = io.BytesIO(etree.tostring(source))
        elif hasattr(source, "to_string") and callable(source.to_string):
            source = io.BytesIO(source.to_string().encode("utf-8"))
        elif self.parser.config.process_xinclude:
            root = etree.parse(source).getroot()  # nosec
            base_url = get_base_url(self.parser.config.base_url, source)
            loader = functools.partial(xinclude_loader, base_url=base_url)
            xinclude.include(root, loader=loader)  # ty: ignore[invalid-argument-type]
            source = io.BytesIO(etree.tostring(root))
        elif isinstance(source, pathlib.Path):
            source = str(source)
        elif isinstance(source, str) and source.lstrip().startswith("<"):
            source = io.BytesIO(source.encode("utf-8"))
        elif isinstance(source, bytes):
            source = io.BytesIO(source)

        try:
            ctx = pygixml.iterparse(source, events=EVENTS)
            return self.process_context(ctx, ns_map)
        except pygixml.PygiXMLError as e:
            raise ParserError(e) from e

    def process_context(
        self,
        context: Iterable[tuple[str, Any]],
        ns_map: dict[str | None, str],
    ) -> Any:
        """Iterate context and push events to main parser.

        Args:
            context: The iterable XML context.
            ns_map: A namespace prefix-URI recorder map.

        Returns:
            An instance of the class type representing the parsed content.

        Raises:
            XmlHandlerError: If an unhandled event is encountered.
        """
        tag_stack: list[str] = []

        for event, element in context:
            if event == EventType.START:
                raw_attrib: dict[str, str] = getattr(element, "attrib", {})
                if not raw_attrib:
                    merged_ns_map = self.merge_parent_namespaces({})
                    attrs: dict[str, str] = {}
                else:
                    element_ns_map: dict[str | None, str] = {}
                    for key, value in raw_attrib.items():
                        if key == "xmlns":
                            element_ns_map[None] = value
                            self.parser.register_namespace(ns_map, None, value)
                        elif key.startswith("xmlns:"):
                            prefix = key[6:]
                            element_ns_map[prefix] = value
                            self.parser.register_namespace(ns_map, prefix, value)

                    merged_ns_map = self.merge_parent_namespaces(element_ns_map)
                    attrs = {}
                    for key, value in raw_attrib.items():
                        if key == "xmlns" or key.startswith("xmlns:"):
                            continue
                        if ":" in key:
                            prefix, local = key.split(":", 1)
                            uri = merged_ns_map.get(prefix)
                            attr_qname = f"{{{uri}}}{local}" if uri else key
                            attrs[attr_qname] = value
                        else:
                            attrs[key] = value

                raw_tag: str = element.tag
                if ":" in raw_tag:
                    prefix, local = raw_tag.split(":", 1)
                    uri = merged_ns_map.get(prefix)
                    qname = f"{{{uri}}}{local}" if uri else raw_tag
                else:
                    uri = merged_ns_map.get(None)
                    qname = f"{{{uri}}}{raw_tag}" if uri else raw_tag

                tag_stack.append(qname)
                self.parser.start(
                    self.clazz,
                    self.queue,
                    self.objects,
                    qname,
                    attrs,
                    merged_ns_map,
                )
            elif event == EventType.END:
                qname = tag_stack.pop() if tag_stack else element.tag
                self.parser.end(
                    self.queue,
                    self.objects,
                    qname,
                    element.text,
                    element.tail,
                )
                try:
                    element.clear()
                except AttributeError:
                    pass
            else:
                raise XmlHandlerError(f"Unhandled event: `{event}`.")

        return self.objects[-1][1] if self.objects else None

    def merge_parent_namespaces(self, ns_map: dict[str | None, str]) -> dict:
        """Merge the given prefix-URI map with the parent node map.

        Args:
            ns_map: The current element namespace prefix-URI map.

        Returns:
            The new merged namespace prefix-URI map.
        """
        if self.queue:
            parent_ns_map = self.queue[-1].ns_map

            if not ns_map:
                return parent_ns_map

            result = parent_ns_map.copy() if parent_ns_map else {}
        else:
            result = {}

        for prefix, uri in ns_map.items():
            result[prefix] = uri

        return result
