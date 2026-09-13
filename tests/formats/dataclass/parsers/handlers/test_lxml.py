from typing import Any
from unittest.case import TestCase

from lxml import etree

from pyxsdata.exceptions import ParserError, XmlHandlerError
from pyxsdata.formats.dataclass.parsers.bases import RecordParser
from pyxsdata.formats.dataclass.parsers.handlers import LxmlEventHandler
from tests import fixtures_dir
from tests.fixtures.books import BookForm, Books
from tests.fixtures.books.fixtures import books, events, events_default_ns


class LxmlEventHandlerTests(TestCase):
    def setUp(self) -> None:
        self.parser = RecordParser(handler=LxmlEventHandler)

    def test_parse(self) -> None:
        path = fixtures_dir.joinpath("books/books.xml")
        self.assertEqual(books, self.parser.from_path(path, Books))
        self.assertEqual({"brk": "urn:books"}, self.parser.ns_map)
        self.assertEqual(events, self.parser.events)

    def test_parse_with_default_ns(self) -> None:
        path = fixtures_dir.joinpath("books/books_default_ns.xml")
        self.assertEqual(books, self.parser.from_path(path, Books))
        self.assertEqual({None: "urn:books"}, self.parser.ns_map)
        self.assertEqual(events_default_ns, self.parser.events)

    def test_parse_with_element_or_tree(self) -> None:
        path = fixtures_dir.joinpath("books/books.xml")
        tree = etree.parse(str(path))

        result = self.parser.parse(tree, Books)
        self.assertEqual(books, result)

        tree = etree.parse(str(path))
        result = self.parser.parse(tree.find(".//book"), BookForm)
        self.assertEqual(books.book[0], result)

    def test_parse_with_xinclude(self) -> None:
        path = fixtures_dir.joinpath("books/books-xinclude.xml")
        ns_map = {"brk": "urn:books", "xi": "http://www.w3.org/2001/XInclude"}

        self.parser.config.process_xinclude = True
        self.assertEqual(books, self.parser.from_path(path, Books))
        self.assertEqual(ns_map, self.parser.ns_map)

    def test_parse_with_xinclude_from_memory(self) -> None:
        path = fixtures_dir.joinpath("books/books-xinclude.xml")
        ns_map = {"brk": "urn:books", "xi": "http://www.w3.org/2001/XInclude"}

        self.parser.config.process_xinclude = True
        self.parser.config.base_url = path.as_uri()
        self.assertEqual(books, self.parser.from_bytes(path.read_bytes(), Books))
        self.assertEqual(ns_map, self.parser.ns_map)

    def test_parse_context_with_unhandled_event(self) -> None:
        handler = LxmlEventHandler(clazz=Books, parser=self.parser)

        with self.assertRaises(XmlHandlerError) as cm:
            handler.process_context([("reverse", "")], {})

        self.assertEqual("Unhandled event: `reverse`.", str(cm.exception))

    def test_parse_with_xml_syntax_error(self) -> None:
        with self.assertRaises(ParserError):
            self.parser.from_string("<", Books)

    def test_parse_blocks_xxe_external_entity(self) -> None:
        xml = b"""<?xml version="1.0"?>
        <!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/hostname">]>
        <Books>
            <book id="1">
                <author>&xxe;</author>
                <title>Title</title>
                <genre>Genre</genre>
                <price>10.0</price>
                <pub_date>2020-01-01</pub_date>
                <review>Review</review>
            </book>
        </Books>"""

        result = self.parser.from_bytes(xml, Books)
        # Verify that the external entity is empty/None and not resolved to file content
        self.assertNotEqual(result.book[0].author, "localhost")
        self.assertFalse(result.book[0].author)

    def test_parse_allows_entity_when_resolve_entities_enabled(self) -> None:
        xml = b"""<?xml version="1.0"?>
        <!DOCTYPE foo [<!ENTITY custom "Resolved Value">]>
        <Books>
            <book id="1">
                <author>&custom;</author>
                <title>Title</title>
                <genre>Genre</genre>
                <price>10.0</price>
                <pub_date>2020-01-01</pub_date>
                <review>Review</review>
            </book>
        </Books>"""

        self.parser.config.resolve_entities = True
        result = self.parser.from_bytes(xml, Books)
        self.assertEqual(result.book[0].author, "Resolved Value")

    def test_parse_allows_entity_with_xinclude_when_resolve_entities_enabled(
        self,
    ) -> None:
        xml = b"""<?xml version="1.0"?>
        <!DOCTYPE foo [<!ENTITY custom "Resolved Value">]>
        <Books>
            <book id="1">
                <author>&custom;</author>
                <title>Title</title>
                <genre>Genre</genre>
                <price>10.0</price>
                <pub_date>2020-01-01</pub_date>
                <review>Review</review>
            </book>
        </Books>"""

        self.parser.config.process_xinclude = True
        self.parser.config.resolve_entities = True
        result = self.parser.from_bytes(xml, Books)
        self.assertEqual(result.book[0].author, "Resolved Value")

    def test_parse_with_custom_resolver(self) -> None:
        """Regression test for tefra/xsdata#1130."""

        class DTDResolver(etree.Resolver):
            def resolve(
                self, system_url: Any, public_id: Any, context: Any
            ) -> Any:
                if system_url == "custom.dtd":
                    return self.resolve_string(
                        b'<!ENTITY resolved_author "External Resolved Author">', context
                    )
                return None

        xml = b"""<?xml version="1.0"?>
        <!DOCTYPE Books SYSTEM "custom.dtd">
        <Books>
            <book id="1">
                <author>&resolved_author;</author>
                <title>Title</title>
                <genre>Genre</genre>
                <price>10.0</price>
                <pub_date>2020-01-01</pub_date>
                <review>Review</review>
            </book>
        </Books>"""

        self.parser.config.load_dtd = True
        self.parser.config.resolve_entities = True
        self.parser.config.resolvers = [DTDResolver()]
        result = self.parser.from_bytes(xml, Books)
        self.assertEqual("External Resolved Author", result.book[0].author)

    def test_parse_with_custom_resolver_and_xinclude(self) -> None:
        """Test custom resolver with xinclude path."""

        class DTDResolver(etree.Resolver):
            def resolve(
                self, system_url: Any, public_id: Any, context: Any
            ) -> Any:
                if system_url == "custom_xi.dtd":
                    return self.resolve_string(
                        b'<!ENTITY resolved_xi_author "External XInclude Author">', context
                    )
                return None

        xml = b"""<?xml version="1.0"?>
        <!DOCTYPE Books SYSTEM "custom_xi.dtd">
        <Books>
            <book id="1">
                <author>&resolved_xi_author;</author>
                <title>Title</title>
                <genre>Genre</genre>
                <price>10.0</price>
                <pub_date>2020-01-01</pub_date>
                <review>Review</review>
            </book>
        </Books>"""

        self.parser.config.load_dtd = True
        self.parser.config.resolve_entities = True
        self.parser.config.process_xinclude = True
        self.parser.config.resolvers = [DTDResolver()]
        result = self.parser.from_bytes(xml, Books)
        self.assertEqual("External XInclude Author", result.book[0].author)
