from collections.abc import Iterable
from typing import Any

from lxml import etree

from pyxsdata.exceptions import XmlHandlerError
from pyxsdata.formats.dataclass.parsers.mixins import XmlHandler
from pyxsdata.models.enums import EventType

EVENTS = (EventType.START, EventType.END, EventType.START_NS)


class LxmlEventHandler(XmlHandler):
    """An lxml event handler."""

    def parse(self, source: Any, ns_map: dict[str | None, str]) -> Any:
        """Parse the source XML document.

        Args:
            source: The xml source, can be a file resource or an input stream,
                or a lxml tree/element.
            ns_map: A namespace prefix-URI recorder map

        Returns:
            An instance of the class type representing the parsed content.
        """
        if isinstance(source, (etree._ElementTree, etree._Element)):
            ctx = etree.iterwalk(source, EVENTS)
        elif self.parser.config.process_xinclude:
            parser = etree.XMLParser(
                resolve_entities=self.parser.config.resolve_entities,
                load_dtd=self.parser.config.load_dtd,
                remove_comments=True,
            )
            tree = etree.parse(
                source, parser=parser, base_url=self.parser.config.base_url
            )  # nosec
            tree.xinclude()
            ctx = etree.iterwalk(tree, EVENTS)
        else:
            ctx = etree.iterparse(  # ty: ignore[no-matching-overload]
                source,
                EVENTS,
                recover=True,
                remove_comments=True,
                resolve_entities=self.parser.config.resolve_entities,
                load_dtd=self.parser.config.load_dtd,
            )

        return self.process_context(ctx, ns_map)  # ty: ignore[invalid-argument-type]

    def process_context(
        self,
        context: Iterable[tuple[str, Any]],
        ns_map: dict[str | None, str],
    ) -> Any:
        """Iterate context and push events to main parser.

        Args:
            context: The iterable lxml context
            ns_map: A namespace prefix-URI recorder map

        Returns:
            An instance of the class type representing the parsed content.
        """
        for event, element in context:
            if event == EventType.START:
                self.parser.start(
                    self.clazz,
                    self.queue,
                    self.objects,
                    element.tag,
                    element.attrib,
                    element.nsmap,
                )
            elif event == EventType.END:
                self.parser.end(
                    self.queue,
                    self.objects,
                    element.tag,
                    element.text,
                    element.tail,
                )
                element.clear()
            elif event == EventType.START_NS:
                prefix, uri = element
                self.parser.register_namespace(ns_map, prefix or None, uri)
            else:
                raise XmlHandlerError(f"Unhandled event: `{event}`.")

        return self.objects[-1][1] if self.objects else None
