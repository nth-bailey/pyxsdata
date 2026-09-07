from unittest.case import TestCase
from xml.etree import ElementTree as etree

import pytest

from pyxsdata.exceptions import ParserError, XmlHandlerError
from pyxsdata.formats.dataclass.parsers.bases import RecordParser
from pyxsdata.formats.dataclass.parsers.handlers import PugixmlEventHandler
from pyxsdata.models.enums import EventType
from tests import fixtures_dir
from tests.fixtures.books import BookForm, Books
from tests.fixtures.books.fixtures import books, events, events_default_ns

try:
    import pygixml
except ImportError:
    pygixml = None


class PugixmlEventHandlerTests(TestCase):
    def setUp(self) -> None:
        if pygixml is None:
            raise pytest.skip("pygixml is not installed")
        self.parser = RecordParser(handler=PugixmlEventHandler)

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

    def test_parse_from_string(self) -> None:
        path = fixtures_dir.joinpath("books/books.xml")
        content = path.read_text()
        self.assertEqual(books, self.parser.from_string(content, Books))

    def test_parse_from_bytes(self) -> None:
        path = fixtures_dir.joinpath("books/books.xml")
        content = path.read_bytes()
        self.assertEqual(books, self.parser.from_bytes(content, Books))

    def test_parse_from_stream(self) -> None:
        path = fixtures_dir.joinpath("books/books.xml")
        with path.open("rb") as stream:
            self.assertEqual(books, self.parser.parse(stream, Books))

    def test_parse_with_element_or_tree(self) -> None:
        path = fixtures_dir.joinpath("books/books.xml")
        tree = etree.parse(str(path))

        result = self.parser.parse(tree, Books)
        self.assertEqual(books, result)

        tree = etree.parse(str(path))
        result = self.parser.parse(tree.find(".//book"), BookForm)
        self.assertEqual(books.book[0], result)

    def test_parse_with_pygixml_doc(self) -> None:
        path = fixtures_dir.joinpath("books/books.xml")
        doc = pygixml.parse_string(path.read_text())
        result = self.parser.parse(doc, Books)
        self.assertEqual(books, result)

        # test XMLNode directly
        result_node = self.parser.parse(doc.root, Books)
        self.assertEqual(books, result_node)

    def test_parse_with_path_object(self) -> None:
        path = fixtures_dir.joinpath("books/books.xml")
        self.assertEqual(books, self.parser.parse(path, Books))

    def test_parse_with_raw_bytes(self) -> None:
        path = fixtures_dir.joinpath("books/books.xml")
        self.assertEqual(books, self.parser.parse(path.read_bytes(), Books))

    def test_parse_with_raw_xml_string(self) -> None:
        path = fixtures_dir.joinpath("books/books.xml")
        self.assertEqual(books, self.parser.parse(path.read_text(), Books))

    def test_parse_with_xinclude(self) -> None:
        path = fixtures_dir.joinpath("books/books-xinclude.xml")
        self.parser.config.process_xinclude = True
        self.assertEqual(books, self.parser.from_path(path, Books))

    def test_parse_with_xinclude_from_memory(self) -> None:
        path = fixtures_dir.joinpath("books/books-xinclude.xml")
        self.parser.config.process_xinclude = True
        self.parser.config.base_url = str(path)
        self.assertEqual(books, self.parser.from_string(path.read_text(), Books))

    def test_parse_context_with_unhandled_event(self) -> None:
        handler = PugixmlEventHandler(clazz=Books, parser=self.parser)

        with self.assertRaises(XmlHandlerError) as cm:
            handler.process_context([("reverse", "")], {})

        self.assertEqual("Unhandled event: `reverse`.", str(cm.exception))

    def test_parse_with_xml_syntax_error(self) -> None:
        with self.assertRaises(ParserError):
            self.parser.from_string("<", Books)

    def test_parse_pydantic_model(self) -> None:
        from pyxsdata.pydantic.bindings import XmlParser
        from tests.pydantic.fixtures.common import TypeC

        xml = (
            '<TypeC xmlns:xs="http://www.w3.org/2001/XMLSchema" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n'
            "  <one>first</one>\n"
            "  <two>1.1</two>\n"
            "  <three>true</three>\n"
            "  <four>01 January 2002 12:01</four>\n"
            "  <four>05 February 2003 13:05</four>\n"
            "  <foo>bar</foo>\n"
            '  <bar xsi:type="xs:string">1</bar>\n'
            '  <bar xsi:type="xs:short">2</bar>\n'
            "</TypeC>\n"
        )
        pydantic_parser = XmlParser(handler=PugixmlEventHandler)
        obj = pydantic_parser.from_string(xml, TypeC)
        self.assertEqual("first", obj.one)
        self.assertEqual(1.1, obj.two)
        self.assertTrue(obj.three)

    def test_forward_events_without_clear(self) -> None:
        handler = PugixmlEventHandler(parser=self.parser, clazz=Books)

        class DummyElement:
            tag = "book"
            text = None
            tail = None
            attrib = {}
            prefix = ""

        events = [(EventType.START, DummyElement()), (EventType.END, DummyElement())]
        handler.process_context(events, {})
