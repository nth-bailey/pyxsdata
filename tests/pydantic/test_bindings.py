from datetime import datetime
from unittest import TestCase

from pyxsdata.pydantic.bindings import XmlParser, XmlSerializer
from pyxsdata.pydantic.compat import AnyElement, DerivedElement
from tests.pydantic.fixtures.common import TypeC


class BindingsTests(TestCase):
    def setUp(self) -> None:
        self.obj = TypeC(
            one="first",
            two=1.1,
            four=[
                datetime(2002, 1, 1, 12, 1),
                datetime(2003, 2, 5, 13, 5),
            ],
            any=AnyElement(
                children=[
                    AnyElement(qname="foo", text="bar"),
                    DerivedElement(qname="bar", value="1"),
                    DerivedElement(qname="bar", value=2),
                ]
            ),
        )

    def test_xml_bindings(self) -> None:
        serializer = XmlSerializer()
        serializer.config.indent = "  "
        serializer.config.xml_declaration = False
        parser = XmlParser()
        ns_map = {
            "xs": "http://www.w3.org/2001/XMLSchema",
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        }

        expected = (
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
        self.assertEqual(expected, serializer.render(self.obj, ns_map))
        self.assertEqual(self.obj, parser.from_string(expected))

    def test_core_xml_parser(self) -> None:
        from pyxsdata.pydantic.bindings import CoreXmlParser
        from tests.pydantic.fixtures.common import TypeA

        xml = "<TypeA><one>first</one><two>1.1</two></TypeA>"
        parser = CoreXmlParser()
        result = parser.from_string(xml, TypeA)
        self.assertIsInstance(result, TypeA)
        self.assertEqual("first", result.one)
        self.assertEqual(1.1, result.two)
