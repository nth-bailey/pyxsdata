import io
from unittest.case import TestCase
from xml.etree import ElementTree as etree

import pytest

from pyxsdata.exceptions import ParserError
from pyxsdata.formats.dataclass.context import XmlContext
from pyxsdata.formats.dataclass.parsers import CoreXmlParser
from pyxsdata.formats.dataclass.parsers.handlers import CoreEventHandler
from pyxsdata.formats.dataclass.serializers import CoreXmlSerializer
from pyxsdata.formats.dataclass.serializers.config import SerializerConfig
from tests import fixtures_dir
from tests.fixtures.books import Books
from tests.fixtures.books.fixtures import books

try:
    import polyxml
except ImportError:
    polyxml = None


class CoreEventHandlerTests(TestCase):
    def setUp(self) -> None:
        if polyxml is None:
            raise pytest.skip("polyxml is not installed")
        self.parser = CoreXmlParser()
        self.serializer = CoreXmlSerializer()

    def test_parse_from_path(self) -> None:
        path = fixtures_dir.joinpath("books/books.xml")
        result = self.parser.from_path(path, Books)
        self.assertEqual(books, result)

    def test_parse_from_bytes(self) -> None:
        path = fixtures_dir.joinpath("books/books.xml")
        content = path.read_bytes()
        result = self.parser.from_bytes(content, Books)
        self.assertEqual(books, result)

    def test_parse_from_string(self) -> None:
        path = fixtures_dir.joinpath("books/books.xml")
        content = path.read_text()
        result = self.parser.from_string(content, Books)
        self.assertEqual(books, result)

    def test_parse_from_path_string(self) -> None:
        path = str(fixtures_dir.joinpath("books/books.xml"))
        result = self.parser.parse(path, Books)
        self.assertEqual(books, result)

    def test_parse_from_stream(self) -> None:
        path = fixtures_dir.joinpath("books/books.xml")
        with path.open("rb") as stream:
            result = self.parser.parse(stream, Books)
        self.assertEqual(books, result)

    def test_parse_from_string_stream(self) -> None:
        path = fixtures_dir.joinpath("books/books.xml")
        stream = io.StringIO(path.read_text())
        result = self.parser.parse(stream, Books)
        self.assertEqual(books, result)

    def test_parse_from_element_tree(self) -> None:
        path = fixtures_dir.joinpath("books/books.xml")
        tree = etree.parse(str(path))
        result = self.parser.parse(tree, Books)
        self.assertEqual(books, result)

    def test_parse_with_auto_locate_clazz(self) -> None:
        context = XmlContext()
        context.build(Books)
        parser = CoreXmlParser(context=context)
        path = fixtures_dir.joinpath("books/books.xml")
        result = parser.from_bytes(path.read_bytes())
        self.assertEqual(books, result)

    def test_parse_auto_locate_failure(self) -> None:
        context = XmlContext()
        parser = CoreXmlParser(context=context)
        with self.assertRaises(ParserError) as cm:
            parser.from_bytes(b"<UnknownRoot><foo>bar</foo></UnknownRoot>")
        self.assertIn("Failed to create target class", str(cm.exception))

    def test_parse_direct_bytes(self) -> None:
        path = fixtures_dir.joinpath("books/books.xml")
        handler = CoreEventHandler(parser=self.parser, clazz=Books)
        result = handler.parse(path.read_bytes(), {})
        self.assertEqual(books, result)

    def test_parse_direct_xml_string(self) -> None:
        path = fixtures_dir.joinpath("books/books.xml")
        handler = CoreEventHandler(parser=self.parser, clazz=Books)
        result = handler.parse(path.read_text(), {})
        self.assertEqual(books, result)

    def test_parse_direct_path(self) -> None:
        path = fixtures_dir.joinpath("books/books.xml")
        handler = CoreEventHandler(parser=self.parser, clazz=Books)
        result = handler.parse(path, {})
        self.assertEqual(books, result)

    def test_parse_element_tree_wrapper(self) -> None:
        class TreeWrapper:
            def __init__(self, root: etree.Element) -> None:
                self._root = root

            def getroot(self) -> etree.Element:
                return self._root

        path = fixtures_dir.joinpath("books/books.xml")
        root = etree.parse(str(path)).getroot()
        wrapper = TreeWrapper(root)
        result = self.parser.parse(wrapper, Books)
        self.assertEqual(books, result)

    def test_parse_auto_locate_corrupt_xml(self) -> None:
        context = XmlContext()
        parser = CoreXmlParser(context=context)
        with self.assertRaises(ParserError):
            parser.parse(b"not-xml-at-all")

    def test_parse_auto_locate_without_context(self) -> None:
        class DummyParser:
            pass

        handler = CoreEventHandler(parser=DummyParser(), clazz=None)  # type: ignore[arg-type]
        with self.assertRaises(ParserError):
            handler.parse(b"<foo></foo>", {})

    def test_parse_unsupported_source_type(self) -> None:
        handler = CoreEventHandler(parser=self.parser, clazz=Books)
        with self.assertRaises(ParserError) as cm:
            handler.parse(12345, {})
        self.assertIn("Unsupported source type", str(cm.exception))

    def test_parse_syntax_error(self) -> None:
        with self.assertRaises(ParserError):
            self.parser.from_bytes(b"<books><unclosed>", Books)

    def test_serialize_render(self) -> None:
        xml_str = self.serializer.render(books)
        self.assertIn('<book id="bk001" lang="en">', xml_str)
        self.assertIn("<author>Hightower, Kim</author>", xml_str)

    def test_serialize_write_and_roundtrip(self) -> None:
        serializer = CoreXmlSerializer(config=SerializerConfig(indent="  "))
        stream = io.StringIO()
        serializer.write(stream, books)
        xml_output = stream.getvalue()
        self.assertIn("  <book", xml_output)

        # Roundtrip back through CoreXmlParser
        parsed = self.parser.from_string(xml_output, Books)
        self.assertEqual(books, parsed)


    def test_serializer_without_polyxml(self) -> None:
        import pyxsdata.formats.dataclass.serializers.xml as xml_mod

        orig = xml_mod.polyxml
        try:
            xml_mod.polyxml = None
            serializer = CoreXmlSerializer()
            with self.assertRaises(ImportError) as cm:
                serializer.render(books)
            self.assertIn("polyxml is required", str(cm.exception))
        finally:
            xml_mod.polyxml = orig
