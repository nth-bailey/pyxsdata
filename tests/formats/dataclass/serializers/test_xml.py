from unittest import TestCase

from pyxsdata.formats.dataclass.serializers import XmlSerializer
from pyxsdata.formats.dataclass.serializers.config import SerializerConfig
from tests.fixtures.books.fixtures import books


class XmlSerializerTests(TestCase):
    def setUp(self) -> None:
        config = SerializerConfig(indent="  ")
        self.serializer = XmlSerializer(config=config)
        super().setUp()

    def test_render(self) -> None:
        result = self.serializer.render(books, ns_map={None: "urn:books"})
        expected = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<books xmlns="urn:books">\n'
            '  <book xmlns="" id="bk001" lang="en">\n'
            "    <author>Hightower, Kim</author>\n"
            "    <title>The First Book</title>\n"
            "    <genre>Fiction</genre>\n"
            "    <price>44.95</price>\n"
            "    <pub_date>2000-10-01</pub_date>\n"
            "    <review>An amazing story of nothing.</review>\n"
            "  </book>\n"
            '  <book xmlns="" id="bk002" lang="en">\n'
            "    <author>Nagata, Suanne</author>\n"
            "    <title>Becoming Somebody</title>\n"
            "    <genre>Biography</genre>\n"
            "    <price>33.95</price>\n"
            "    <pub_date>2001-01-10</pub_date>\n"
            "    <review>A masterpiece of the fine art of gossiping.</review>\n"
            "  </book>\n"
            "</books>\n"
        )

        self.assertEqual(expected, result)

    def test_render_choice_with_subclass(self) -> None:
        from tests.fixtures.models import ChoiceType

        class CustomInt(int):
            pass

        obj = ChoiceType(choice=[CustomInt(99)])
        result = self.serializer.render(obj)
        self.assertIn("<int>99</int>", result)

    def test_render_and_parse_newtype(self) -> None:
        from dataclasses import dataclass, field
        from typing import NewType

        from pyxsdata.formats.dataclass.parsers import XmlParser

        UserId = NewType("UserId", int)
        UserName = NewType("UserName", str)

        @dataclass
        class Account:
            id: UserId = field(metadata={"type": "Attribute"})
            name: UserName = field(metadata={"type": "Element"})

        acc = Account(id=UserId(123), name=UserName("alice"))
        xml = self.serializer.render(acc)
        self.assertIn('id="123"', xml)
        self.assertIn("<name>alice</name>", xml)

        parser = XmlParser()
        parsed = parser.from_string(xml, Account)
        self.assertEqual(acc, parsed)
