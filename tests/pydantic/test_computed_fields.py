from unittest import TestCase

from pydantic import BaseModel, computed_field

from pyxsdata.pydantic.bindings import (
    DictDecoder,
    DictEncoder,
    JsonParser,
    JsonSerializer,
    XmlParser,
    XmlSerializer,
)


class User(BaseModel):
    first_name: str
    last_name: str

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Product(BaseModel):
    unit_price: float
    quantity: int

    @computed_field(alias="TotalPrice")
    @property
    def total(self) -> float:
        return round(self.unit_price * self.quantity, 2)


class ComputedFieldsTests(TestCase):
    def test_computed_field_xml_serialization_and_parsing(self) -> None:
        user = User(first_name="Jane", last_name="Doe")
        serializer = XmlSerializer()
        serializer.config.xml_declaration = False
        xml = serializer.render(user)

        expected = "<User><first_name>Jane</first_name><last_name>Doe</last_name><full_name>Jane Doe</full_name></User>"
        self.assertEqual(expected, xml)

        parser = XmlParser()
        parsed = parser.from_string(xml, User)
        self.assertEqual("Jane", parsed.first_name)
        self.assertEqual("Doe", parsed.last_name)
        self.assertEqual("Jane Doe", parsed.full_name)

    def test_computed_field_alias_xml_serialization(self) -> None:
        prod = Product(unit_price=12.50, quantity=4)
        serializer = XmlSerializer()
        serializer.config.xml_declaration = False
        xml = serializer.render(prod)

        expected = "<Product><unit_price>12.5</unit_price><quantity>4</quantity><TotalPrice>50.0</TotalPrice></Product>"
        self.assertEqual(expected, xml)

        parser = XmlParser()
        parsed = parser.from_string(xml, Product)
        self.assertEqual(12.50, parsed.unit_price)
        self.assertEqual(4, parsed.quantity)
        self.assertEqual(50.0, parsed.total)

    def test_computed_field_dict_and_json(self) -> None:
        user = User(first_name="Alice", last_name="Smith")
        encoder = DictEncoder()
        d = encoder.encode(user)
        self.assertEqual(
            {"first_name": "Alice", "last_name": "Smith", "full_name": "Alice Smith"},
            d,
        )

        decoder = DictDecoder()
        decoded = decoder.decode(d, User)
        self.assertEqual("Alice Smith", decoded.full_name)

        json_serializer = JsonSerializer()
        json_str = json_serializer.render(user)
        self.assertIn('"full_name": "Alice Smith"', json_str)

        json_parser = JsonParser()
        parsed_json = json_parser.from_string(json_str, User)
        self.assertEqual("Alice Smith", parsed_json.full_name)

    def test_computed_field_json_schema_extra_and_untyped(self) -> None:
        class ExtraModel(BaseModel):
            val: int

            @computed_field(
                json_schema_extra={
                    "metadata": {"type": "Attribute", "name": "custom_attr"}
                }
            )
            @property
            def attr_val(self) -> int:
                return self.val * 2

            @computed_field
            @property
            def extra_prop(self) -> str:
                return "hello"

        model = ExtraModel(val=5)
        serializer = XmlSerializer()
        serializer.config.xml_declaration = False
        xml = serializer.render(model)
        expected = '<ExtraModel custom_attr="10"><val>5</val><extra_prop>hello</extra_prop></ExtraModel>'
        self.assertEqual(expected, xml)
